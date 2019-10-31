import pytest

from pyecore.resources import ResourceSet, URI
from pygeppetto.model import GeppettoModel, model_utility

from .test_xmi import filepath

@pytest.fixture
def model() -> GeppettoModel:
    rset = ResourceSet()
    resource = rset.get_resource(URI(filepath('model_with_queries.xmi')))
    return resource.contents[0]


def test_get_query(model):
    query = model_utility.get_query('mockDataSource.mock_query', model)

    assert query.name == "A mock compound query"

    with pytest.raises(model_utility.QueryNotFoundException):
        model_utility.get_query('mockDataSource', model)
