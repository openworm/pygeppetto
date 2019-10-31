import pytest
from unittest.mock import Mock
import json

import responses

from pyecore.resources import ResourceSet, URI
from pygeppetto.api.inbound_messages import InboundMessages
from pygeppetto.api.message_handler import GeppettoMessageHandler
from pygeppetto.data_model import GeppettoProject
from pygeppetto.model import GeppettoModel, QueryResults
from pygeppetto.model.datasources import QueryResult
from pygeppetto.services.data_manager import GeppettoDataManager, DataManagerHelper
from pygeppetto.services.data_source_service import DataSourceService, ServiceCreator

from .test_xmi import filepath
from .mocks import neo4j_response


def model() -> GeppettoModel:
    rset = ResourceSet()
    resource = rset.get_resource(URI(filepath('model_with_queries.xmi')))
    return resource.contents[0]


@pytest.fixture
def message_handler():
    return GeppettoMessageHandler()


class MockDataSourceService(DataSourceService):
    def get_template(self):
        return '{"statement":"$QUERY"}'

    def get_connection_type(self):
        return 'POST'

    def process_response(self, response):
        response = json.loads(response[0])['results'][0]
        qr = QueryResults()
        qr.header.extend(response['columns'])
        qr.results.extend(QueryResult(values=r) for r in response['data'])

        return qr

class MockDataManager(GeppettoDataManager):

    def get_project_from_url(self, url=None):
        project = GeppettoProject(id='mock', name='mock', geppetto_model=model())
        self.projects[project.id] = project
        return project


DataManagerHelper.setDataManager(MockDataManager())




@responses.activate
def test_run_query(message_handler):
    messages = []
    def mock_send_message(message):
        print(message)
        messages.append(message)
        assert not 'error' in message['type']
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
    assert ServiceCreator.get_new_datasource_service_instance(runtime_project.model.dataSources[0],
                                                              None).__class__ == MockDataSourceService

    URL = "http://mg-neo4j/db/data/transaction"

    responses.add(responses.POST, URL, json=neo4j_response(), status=200)
    msg_data = json.dumps({
        "projectId": 'mock',
        "runnableQueries": [
            {
                "queryPath": "mockDataSource.mock_query"
            }
        ]
    })
    run_query_msg = {"requestID": "Connection23-5", "type": InboundMessages.RUN_QUERY,
                     "data": msg_data}
    message_handler.handle_message(run_query_msg)

    assert message_handler.send_message_data.call_count == 3

    result = json.loads(messages[2]['data'])
    model = json.loads(result['return_query'])
    assert model['eClass'] == QueryResults.__name__


