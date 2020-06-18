import json
import pytest

from pygeppetto.model import GeppettoLibrary
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.datasources.datasources import DataSource, QueryResults, QueryResult
from pygeppetto.model.datasources import BooleanOperator
from pygeppetto.services.data_source_service import DataSourceService
from pygeppetto.services.model_interpreter import add_model_interpreter
from pygeppetto.services.data_source.neo4j import Neo4jDataSourceService
from .mocks import MockModelInterpreter, neo4j_response as mock_neo4j_response


def create_result(id):
    return (id, f"Result number {id}")


def create_query_result(id):
    return QueryResult(values=create_result(id))


def model_access():
    model_interpreter = MockModelInterpreter()
    model_library = GeppettoLibrary(name='mocklibrary', id='mocklibrary')
    geppetto_model = model_interpreter.create_model(library=model_library)
    add_model_interpreter(model_library.id, model_interpreter)
    return GeppettoModelAccess(geppetto_model)


@pytest.fixture
def data_source_service():
    return DataSourceService(configuration=DataSource(),
                             model_access=model_access())


def test_datasource_service_get_results(data_source_service):
    header = ["ID", "content"]

    query_result_dict = {}
    assert len(data_source_service.get_results(query_result_dict).results) == 0

    # OR [0, 1]  == [0, 1]
    query_results = [create_query_result(i) for i in range(2)]
    query_results = QueryResults(id="1", header=header, results=query_results)
    query_result_dict[query_results] = BooleanOperator.OR

    get_results = data_source_service.get_results(query_result_dict)
    assert len(get_results.results) == 2

    # OR [0, 1]  [1, 2, 3] == [0, 1, 2, 3]
    query_results = [create_query_result(i) for i in range(1, 4)]
    query_results = QueryResults(id="2", header=header, results=query_results)
    query_result_dict = {get_results: BooleanOperator.OR, query_results: BooleanOperator.OR}
    merged_results = data_source_service.get_results(query_result_dict)
    assert len(merged_results.results) == 4

    # AND [0, 1, 2, 3] [0, 1] ==  [0, 1]
    query_results = [create_query_result(i) for i in range(2)]
    query_results = QueryResults(id="3", header=header, results=query_results)
    query_result_dict = {merged_results: BooleanOperator.OR, query_results: BooleanOperator.AND}
    merged_results = data_source_service.get_results(query_result_dict)
    assert len(merged_results.results) == 2
    assert merged_results.results[0].values[0] == 0
    assert merged_results.results[1].values[0] == 1

    # NAND  [0, 1] [0] == [1]
    query_results = [create_query_result(0)]
    query_results = QueryResults(id="4", header=header, results=query_results)
    query_result_dict = {merged_results: BooleanOperator.OR, query_results: BooleanOperator.NAND}
    nand_results = data_source_service.get_results(query_result_dict)
    assert len(nand_results.results) == 1
    assert nand_results.results[0].values[1] == "Result number 1"


def test_neo4j_datasource_service():
    neo4j_response = json.dumps(mock_neo4j_response())

    dss = Neo4jDataSourceService(configuration=DataSource(), model_access=model_access())

    query_results = dss.process_response([neo4j_response])

    assert query_results.header == ["ID", "n"]
    assert len(query_results.results) == 2
    assert query_results.results[0].values == ['0', '{"title": "The Matrix", "released": 1999}']
