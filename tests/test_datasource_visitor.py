# pylint: disable=redefined-outer-name
import pytest
import responses
from pygeppetto.model import GeppettoLibrary, Variable
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.datasources.datasources import QueryResults, QueryResult
from pygeppetto.model.datasources.datasources import SimpleQuery, CompoundQuery
from pygeppetto.model.datasources.datasources import QueryMatchingCriteria, DataSource

from pygeppetto.visitors.data_source_visitors import ExecuteQueryVisitor
from pygeppetto.model.utils.datasource import query_check

from pygeppetto.services.model_interpreter import add_model_interpreter
from pygeppetto.model.types import CompositeVisualType, VisualType
from pygeppetto.services.data_source.neo4j import Neo4jDataSourceService

from .mocks import MockModelInterpreter, neo4j_response as mock_neo4j_response

URL = "http://localhost:7474/db/data/transaction/commit"

def create_result(iden):
    return (iden, f"Result number {iden}")

def create_query_result(iden):
    return QueryResult(values=create_result(iden))

def model_access():
    model_interpreter = MockModelInterpreter()
    model_library = GeppettoLibrary(name='mocklibrary', id='mocklibrary')
    geppetto_model = model_interpreter.create_model(library=model_library)
    add_model_interpreter(model_library.id, model_interpreter)
    return GeppettoModelAccess(geppetto_model)


@pytest.fixture
def visitor():
    return ExecuteQueryVisitor(variable=Variable(id="visitor", types=(CompositeVisualType(), )),
                               geppetto_model_access=model_access(),
                               count_only=False,
                               processing_output_map=None)

def test_visitor_merge_results(visitor):
    header = ["ID", "content"]

    assert visitor.results is None

    initial_results = [create_query_result(i) for i in range(2)]

    query_results = QueryResults(id="initial", header=header, results=initial_results)
    visitor.merge_results(query_results)
    assert len(visitor.results.results) == 2
    assert all([result.values[1] == f"Result number {index}" \
                                for index, result in enumerate(visitor.results.results)])

    new_results = [create_query_result(i+2) for i in range(3)]
    query_results = QueryResults(id="new", header=header, results=new_results)
    visitor.merge_results(query_results)

    assert len(visitor.results.results) == 5
    assert all([result.values[1] == f"Result number {index}" \
                                for index, result in enumerate(visitor.results.results)])

    modified_results = [QueryResult(values=(0, "Result number 0 modified"))]
    query_results = QueryResults(id="modified", header=header, results=modified_results)

    visitor.merge_results(query_results)

    assert len(visitor.results.results) == 5
    assert visitor.results.results[0].values[2] == 'Result number 0 modified'

@responses.activate
def test_simple_query_case(visitor):

    responses.add(responses.POST, URL, json=mock_neo4j_response(), status=200, stream=True)

    v_type = VisualType()
    match_crit = QueryMatchingCriteria(type=(v_type,))
    query = SimpleQuery(query="\"statement\": \"MATCH(n) RETURN id(n) as ID, n;\"",
                        matchingCriteria=(match_crit,))

    DataSource(url=URL, queries=(query,), dataSourceService=Neo4jDataSourceService.__name__)

    visitor.do_switch(query)

    assert len(visitor.results.results) == 2
    assert visitor.results.results[0].values == ['0', '{"title": "The Matrix", "released": 1999}']


@responses.activate
def test_compound_query_case(visitor):
    responses.add(responses.POST, URL, json=mock_neo4j_response(), status=200, stream=True)

    v_type = VisualType()
    match_crit = QueryMatchingCriteria(type=(v_type,))
    query = SimpleQuery(query="\"statement\": \"MATCH(n) RETURN id(n) as ID, n;\"",
                        matchingCriteria=(match_crit,))

    compound_query = CompoundQuery(queryChain=[query, query])

    DataSource(url=URL, queries=(compound_query,),
               dataSourceService=Neo4jDataSourceService.__name__)

    visitor.do_switch(compound_query)

    assert len(visitor.results.results) == 2
    assert visitor.results.results[0].values == ['0', '{"title": "The Matrix", "released": 1999}']


def test_query_check():
    vtype = VisualType()
    comp_vtype = CompositeVisualType()

    var1 = Variable(id="var2", types=(vtype,))
    var2 = Variable(id="var3", anonymousTypes=(comp_vtype,))

    mc1 = QueryMatchingCriteria(type=(vtype,))
    mc2 = QueryMatchingCriteria(type=(comp_vtype,))

    query1 = SimpleQuery(query="dummy query;", matchingCriteria=(mc1,))
    query2 = SimpleQuery(query="dummy query;", matchingCriteria=(mc2,))

    assert not query_check(query=query1, variable=var1)
    assert query_check(query=query1, variable=var2)
    assert not query_check(query=query2, variable=var1)
