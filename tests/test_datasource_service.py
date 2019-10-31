import pytest

from pygeppetto.model import GeppettoLibrary
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.datasources.datasources import DataSource, QueryResults, QueryResult
from pygeppetto.model.datasources import BooleanOperator
from pygeppetto.services.data_source_service import DataSourceService
from pygeppetto.services.model_interpreter import add_model_interpreter

from .mocks import MockModelInterpreter


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

    results = {}
    assert len(data_source_service.get_results(results).results) == 0

    # OR [0, 1]  == [0, 1]
    query_results = [ create_query_result(i) for i in range(2) ]
    query_results = QueryResults(id="1", header=header, results=query_results)
    results[query_results] = BooleanOperator.OR

    assert len(data_source_service.get_results(results).results) == 2

    # OR [1, 2, 3] == [0, 1, 2, 3]
    query_results = [ create_query_result(i+1) for i in range(3) ]
    query_results = QueryResults(id="2", header=header, results=query_results)
    results[query_results] = BooleanOperator.OR

    assert len(data_source_service.get_results(results).results) == 4

    # AND [0, 1]  ==  [0, 1]
    query_results = [ create_query_result(i) for i in range(2) ]
    query_results = QueryResults(id="3", header=header, results=query_results)
    results[query_results] = BooleanOperator.AND

    assert len(data_source_service.get_results(results).results) == 2

    # NAND [0] == [1]
    query_results = [ create_query_result(0) ]
    query_results = QueryResults(id="4", header=header, results=query_results)
    results[query_results] = BooleanOperator.NAND

    assert len(data_source_service.get_results(results).results) == 1
    assert data_source_service.get_results(results).results[0].values[1] == "Result number 1"