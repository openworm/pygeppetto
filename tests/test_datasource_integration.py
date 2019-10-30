import pytest
from unittest.mock import patch, Mock
import os
import json

from pyecore.resources import ResourceSet, URI
from pygeppetto.api.inbound_messages import InboundMessages
from pygeppetto.api.message_handler import GeppettoMessageHandler
from pygeppetto.data_model import GeppettoProject
from pygeppetto.model import GeppettoModel, QueryResults
from pygeppetto.services.data_manager import GeppettoDataManager, DataManagerHelper
from pygeppetto.services.data_source_service import DataSourceService, ServiceCreator

from .test_xmi import filepath


def model() -> GeppettoModel:
    rset = ResourceSet()
    resource = rset.get_resource(URI(filepath('model_with_queries.xmi')))
    return resource.contents[0]


@pytest.fixture
def message_handler():
    return GeppettoMessageHandler()


class MockDataSourceService(DataSourceService):
    pass


class MockDataManager(GeppettoDataManager):

    def get_project_from_url(self, url=None):
        project = GeppettoProject(id='mock', name='mock', geppetto_model=model())
        self.projects[project.id] = project
        return project


DataManagerHelper.setDataManager(MockDataManager())


def mock_send_message(message):
    print(message)
    assert not 'error' in message['type']

def test_run_query(message_handler):
    # 1 preparation: first we need a RuntimeProject active and model loaded
    message_handler.send_message_data = Mock(side_effect=mock_send_message)
    message_handler.handle_message(
        dict(type=InboundMessages.LOAD_PROJECT_FROM_URL, requestID='whatever', data='this will be ignored'))

    assert message_handler.send_message_data.call_count == 2
    geppetto_manager = message_handler.geppettoManager
    project = message_handler.retrieveGeppettoProject('mock')
    assert project.id == 'mock'

    runtime_project = geppetto_manager.get_runtime_project(project)
    assert len(runtime_project.model.dataSources) == 1
    configured_data_source_service = runtime_project.model.dataSources[0].dataSourceService
    assert configured_data_source_service == MockDataSourceService.__name__
    assert ServiceCreator.get_new_service_instance(runtime_project.model.dataSources[0],
                                                   None).__class__ == MockDataSourceService

    with patch('pygeppetto.services.data_source_service.ExecuteQueryVisitor') as vis:
        from pygeppetto.services.data_source_service import ExecuteQueryVisitor
        assert ExecuteQueryVisitor is vis
        vis.do_switch.return_value = QueryResults()

        assert isinstance(vis.do_switch(), QueryResults)
        msg_data = json.dumps({"projectId":'mock',"runnableQueries":[{"targetVariablePath":"WHATEVER","queryPath":"mock_query"}]})
        run_query_msg = {"requestID": "Connection23-5", "type": InboundMessages.RUN_QUERY,
         "data": msg_data}
        message_handler.handle_message(run_query_msg)

        assert message_handler.send_message_data.call_count == 3

        assert vis.do_switch.call_count == 1
