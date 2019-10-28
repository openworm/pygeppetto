import pytest

from pygeppetto.model import GeppettoModel, GeppettoLibrary, Variable
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.datasources.datasources import QueryResults, QueryResult, SimpleQuery, QueryMatchingCriteria

from pygeppetto.visitors.data_source_visitors import ExecuteQueryVisitor, QueryChecker

from pygeppetto.services.model_interpreter import add_model_interpreter
from pygeppetto.model.types import CompositeVisualType, VisualType, SimpleType
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
def visitor():
    return ExecuteQueryVisitor(variable=Variable(id="visitor"),
                        geppetto_model_access=model_access(),
                        count_only=False,
                        processing_output_map=None)

def test_visitor_merge_results(visitor):
    header = ["ID", "content"]
    
    assert visitor.results == None
    assert len(visitor.merged_results.results) == 0

    initial_results = [ create_query_result(i) for i in range(2) ]

    query_results = QueryResults(id="initial", header=header, results=initial_results)
    visitor.merge_results(query_results)
    assert len(visitor.results.results) == 2
    # assert len(visitor.merged_results.results) == 0
    assert all([result.values[1] == f"Result number {index}" for index, result in enumerate(visitor.results.results)])
    
    new_results = [ create_query_result(i+2) for i in range(3) ]
    query_results = QueryResults(id="new", header=header, results=new_results)
    visitor.merge_results(query_results)

    # assert len(visitor.merged_results.results) == 5
    assert all([result.values[1] == f"Result number {index}" for index, result in enumerate(visitor.results.results)])
    

    modified_results = [QueryResult(values=(0, "Result number 0 modified"))]
    query_results = QueryResults(id="modified", header=header, results=modified_results)
    
    visitor.merge_results(query_results)
    
    assert len(visitor.results.results) == 5
    assert visitor.results.results[0].values[2] == 'Result number 0 modified'


def test_query_check():
    
    vt = VisualType()
    cvt = CompositeVisualType()
    
    var1 = Variable(id="var2", types=(vt,))
    var2 = Variable(id="var3", anonymousTypes=(cvt,))
    
    mc1 = QueryMatchingCriteria(type=(vt,))
    mc2 = QueryMatchingCriteria(type=(cvt,))

    q1 = SimpleQuery(query="MATCH (x) RETURN (x);", matchingCriteria=(mc1,))
    q2 = SimpleQuery(query="MATCH (x) RETURN (x);", matchingCriteria=(mc2,))
    
    assert not QueryChecker.check(query=q1, variable=var1)
    assert QueryChecker.check(query=q1, variable=var2)
    assert not QueryChecker.check(query=q2, variable=var1)