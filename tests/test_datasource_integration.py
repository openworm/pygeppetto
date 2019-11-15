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
from .mocks import neo4j_response, MockFetchQueryProcessor, MockDataManager, MockDataSourceService





@pytest.fixture
def message_handler():
    return GeppettoMessageHandler()





DataManagerHelper.setDataManager(MockDataManager())


def load_project(message_handler):
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
                                                              None).__class__==MockDataSourceService
    return runtime_project, messages


@responses.activate
def test_run_query(message_handler):
    runtime_project, messages = load_project(message_handler)

    URL = "http://my-neo4j/db/data/transaction"

    responses.add(responses.POST, URL, json=neo4j_response(), status=200)
    msg_data = json.dumps({
        "projectId": 'mock',
        "runnableQueries": [
            {
                "queryPath": "mockDataSource.mock_query",
                "targetVariablePath": "v"
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


@responses.activate
def test_fetch_variable(message_handler):
    runtime_project, messages = load_project(message_handler)

    URL = "http://my-neo4j/db/data/transaction"

    responses.add(responses.POST, URL, json=neo4j_response(), status=200)
    msg_data = json.dumps({
        "projectId": 'mock',
        "dataSourceId": "mockDataSource",
        "variableId": ["myvar"],
    })

    run_query_msg = {"requestID": "Connection23-5", "type": InboundMessages.FETCH_VARIABLE,
                     "data": msg_data}
    message_handler.handle_message(run_query_msg)

    assert message_handler.send_message_data.call_count == 3

    variable = next(var for var in runtime_project.model.worlds[0].variables if var.id == 'myvar')

    assert variable.name == MockFetchQueryProcessor.variable_name

    variable_container = variable.eContainer()
    assert variable_container.id
    assert variable.id
    assert "myvar" in messages[2]['data']


@responses.activate
def test_fetch(message_handler):
    runtime_project, messages = load_project(message_handler)

    URL = "http://my-neo4j/db/data/transaction"

    responses.add(responses.POST, URL, json=neo4j_response(), status=200)
    msg_data = json.dumps({
        "projectId": 'mock',
        "dataSourceId": "mockDataSource",
        "variables": ["myvar"],
        "instances": ["myinst"],
        "worldId": "w"
    })

    run_query_msg = {"requestID": "Connection23-5", "type": InboundMessages.FETCH,
                     "data": msg_data}
    message_handler.handle_message(run_query_msg)

    assert message_handler.send_message_data.call_count == 3

    variable = next(var for var in runtime_project.model.worlds[0].variables if var.id == 'myvar')

    assert variable.name == MockFetchQueryProcessor.variable_name

    variable_container = variable.eContainer()
    assert variable_container.id
    assert variable.id
    assert "myvar" in messages[2]['data']

    instance = next(inst for inst in runtime_project.model.worlds[0].instances if inst.id == 'myinst')
    assert instance.name == MockFetchQueryProcessor.variable_name
    assert "myinst" in messages[2]['data']
