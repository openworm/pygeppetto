#!/usr/bin/env python
""" generated source for module WebsocketConnection """
from __future__ import print_function

import json
import logging

from pyecore.valuecontainer import EList
from pygeppetto.api.messaging import TransportMessageFactory
from pygeppetto.constants import UserPrivileges, GeppettoErrorCodes
from pygeppetto.managers import GeppettoManager
from pygeppetto.model.exceptions import GeppettoExecutionException, GeppettoInitializationException
from pygeppetto.model.model_serializer import GeppettoSerializer
from pygeppetto.services.data_manager import DataManagerHelper

from . import inbound_messages as InboundMessages
from . import outbound_messages as OutboundMessages


class GeppettoHandlerTypedException(Exception):
    def __init__(self, msg_type=OutboundMessages.ERROR, msg='Error not specified', exc=None):
        Exception.__init__(self, str(msg))
        self.payload = msg.__dict__ if hasattr(msg, '__dict__') else {"error": str(msg)}
        self.exc = exc
        self.msg_type = msg_type


class Error(object):
    """ generated source for class Error """

    def __init__(self, errorCode, errorMessage, jsonExceptionMsg, id):
        """ generated source for method __init__ """
        self.error_code = errorCode.__str__()
        self.message = json.dumps(errorMessage)
        self.exception = jsonExceptionMsg
        self.id = id


in_out_msg_lookup = {
    InboundMessages.GEPPETTO_VERSION: OutboundMessages.GEPPETTO_VERSION,
    InboundMessages.RESOLVE_IMPORT_TYPE: OutboundMessages.IMPORT_TYPE_RESOLVED,
    InboundMessages.RESOLVE_IMPORT_VALUE: OutboundMessages.IMPORT_VALUE_RESOLVED,
    InboundMessages.RUN_QUERY: OutboundMessages.RETURN_QUERY,
    InboundMessages.RUN_QUERY_COUNT: OutboundMessages.RETURN_QUERY_COUNT,
    InboundMessages.FETCH_VARIABLE: OutboundMessages.VARIABLE_FETCHED,
    InboundMessages.FETCH: OutboundMessages.FETCHED
}


def lookup_return_msg_type(msg_type):
    if msg_type in in_out_msg_lookup:
        return in_out_msg_lookup[msg_type]
    raise RuntimeError("{} not defined into in_out_msg_lookup".format(msg_type))


class GeppettoMessageHandler:
    '''
    Generic message handler: can be subclassed to implement with websocket or other bidirectional means.
    '''

    PRIVILEGES = json.dumps({
        "userName": "Python User",
        "loggedIn": True,
        "hasPersistence": False,
        "privileges": list(up.value for up in UserPrivileges)
    })

    simulationServerConfig = None

    def __init__(self):
        scope_id = id(self)
        self.scope_id = scope_id
        self.geppettoManager = GeppettoManager.get_instance(scope_id)

    def sendPrivileges(self):
        self.send_message(None, OutboundMessages.USER_PRIVILEGES, self.PRIVILEGES)

    def sendClientId(self):
        self.send_message(None, OutboundMessages.CLIENT_ID, self.scope_id)

    def send_message_data(self, msg_data):
        raise NotImplemented

    def handle_message(self, payload):
        '''
        Handles a message coming from the client
        :param payload: a dictionary
        :return:
        '''

        assert 'type' in payload, 'Websocket without type received: {}'.format(payload)

        logging.info('Websocket message received: {}'.format(payload['type']))

        experimentId = -1
        #  de-serialize JSON
        gmsg = payload
        requestID = gmsg['requestID']
        msg_data = None
        #  switch on messages type
        #  NOTE: each messages handler knows how to interpret the GeppettoMessage data field
        msg_type = self.get_message_type(gmsg)
        try:
            if msg_type == InboundMessages.GEPPETTO_VERSION:
                msg_data = self.getVersionNumber(requestID)

            elif msg_type == InboundMessages.RESOLVE_IMPORT_VALUE:
                received_object = json.loads(gmsg['data'])
                msg_data = self.resolveImportValue(requestID, received_object['projectId'],
                                                   received_object['experimentId'],
                                                   received_object['path'])

            elif msg_type == InboundMessages.RESOLVE_IMPORT_TYPE:
                received_object = gmsg['data']
                msg_data = self.resolveImportType(requestID, received_object.projectId,
                                                  received_object.paths)
            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_CONTENT:
                self.loadProjectFromContent(requestID, gmsg['data'])
            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_URL:
                self.loadProjectFromUrl(requestID, gmsg['data'])
            elif msg_type == InboundMessages.RUN_QUERY:
                received_object = json.loads(gmsg['data'])
                msg_data = self.run_query(received_object)
            elif msg_type == InboundMessages.FETCH_VARIABLE:
                received_object = json.loads(gmsg['data'])
                msg_data = self.fetch_variable(received_object)
            elif msg_type == InboundMessages.FETCH:
                received_object = json.loads(gmsg['data'])
                msg_data = self.fetch(received_object)


            # TODO Complete API. From here on, implementation is not complete: just bare porting from Java
            elif msg_type == InboundMessages.USER_PRIVILEGES:
                msg_data = self.checkUserPrivileges(requestID)
            elif msg_type == InboundMessages.NEW_EXPERIMENT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.newExperiment(requestID, projectId)
            elif msg_type == InboundMessages.NEW_EXPERIMENT_BATCH:
                received_object = gmsg['data']
                msg_data = self.newExperimentBatch(requestID, received_object.projectId, received_object)
            elif msg_type == InboundMessages.CLONE_EXPERIMENT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                experimentId = int(parameters.get("experimentId"))
                msg_data = self.cloneExperiment(requestID, projectId, experimentId)

            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_ID:
                parameters = gmsg['data']
                if parameters.containsKey("experimentId"):
                    experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                self.loadProjectFromId(requestID, projectId, experimentId)

            elif msg_type == InboundMessages.PERSIST_PROJECT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.persistProject(requestID, projectId)
            elif msg_type == InboundMessages.MAKE_PROJECT_PUBLIC:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                isPublic = bool(parameters.get("isPublic"))
                msg_data = self.makeProjectPublic(requestID, projectId, isPublic)
            elif msg_type == InboundMessages.DOWNLOAD_PROJECT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.downloadProject(requestID, projectId)
            elif msg_type == InboundMessages.SAVE_PROJECT_PROPERTIES:
                received_object = gmsg['data']
                msg_data = self.saveProjectProperties(requestID, received_object.projectId,
                                                      received_object.properties)
            elif msg_type == InboundMessages.SAVE_EXPERIMENT_PROPERTIES:
                received_object = gmsg['data']
                msg_data = self.saveExperimentProperties(requestID, received_object.projectId,
                                                         received_object.experimentId,
                                                         received_object.properties)
            elif msg_type == InboundMessages.LOAD_EXPERIMENT:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                msg_data = self.loadExperiment(requestID, experimentId, projectId)
            elif msg_type == InboundMessages.GET_SCRIPT:
                received_object = gmsg['data']
                msg_data = self.sendScriptData(requestID, received_object.projectId,
                                               received_object.scriptURL,
                                               self.websocketConnection)
            elif msg_type == InboundMessages.GET_DATA_SOURCE_RESULTS:
                url = None
                dataSourceName = None
                try:
                    parameters = gmsg['data']
                    url = parameters.get("url")
                    dataSourceName = parameters.get("data_source_name")
                    # TODO: use self.websocketConnection when it is implemented
                    msg_data = self.sendDataSourceResults(requestID, dataSourceName, url,
                                                          'self.websocketConnection')
                except IOError as e:
                    self.send_message(requestID, OutboundMessages.ERROR_READING_SCRIPT, "")
            elif msg_type == InboundMessages.GET_EXPERIMENT_STATE:
                received_object = gmsg['data']
                msg_data = self.getExperimentState(requestID, received_object.experimentId,
                                                   received_object.projectId,
                                                   received_object.variables)
            elif msg_type == InboundMessages.DELETE_EXPERIMENT:
                received_object = gmsg['data']
                msg_data = self.deleteExperiment(requestID, received_object.experimentId,
                                                 received_object.projectId)
            elif msg_type == InboundMessages.RUN_EXPERIMENT:
                received_object = gmsg['data']
                msg_data = self.runExperiment(requestID, received_object.experimentId,
                                              received_object.projectId)
            elif msg_type == InboundMessages.SET_WATCHED_VARIABLES:
                received_object = gmsg['data']
                try:
                    msg_data = self.setWatchedVariables(requestID, received_object.variables,
                                                        received_object.experimentId,
                                                        received_object.projectId,
                                                        received_object.watch)
                except GeppettoExecutionException as e:
                    self.send_message(requestID, OutboundMessages.ERROR_SETTING_WATCHED_VARIABLES, "")
                except GeppettoInitializationException as e:
                    self.send_message(requestID, OutboundMessages.ERROR_SETTING_WATCHED_VARIABLES, "")
            elif msg_type == InboundMessages.GET_SUPPORTED_OUTPUTS:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                instancePath = parameters.get("instancePath")
                msg_data = self.getSupportedOuputs(requestID, instancePath, experimentId, projectId)
            elif msg_type == InboundMessages.DOWNLOAD_MODEL:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                instancePath = parameters.get("instancePath")
                format = parameters.get("format")
                msg_data = self.downloadModel(requestID, instancePath, format, experimentId, projectId)
            elif msg_type == InboundMessages.SET_PARAMETERS:
                received_object = gmsg['data']
                msg_data = self.setParameters(requestID, received_object.modelParameters,
                                              received_object.projectId,
                                              received_object.experimentId)
            elif msg_type == InboundMessages.SET_EXPERIMENT_VIEW:
                received_object = gmsg['data']
                msg_data = self.setExperimentView(requestID, received_object.view,
                                                  received_object.projectId,
                                                  received_object.experimentId)
            elif msg_type == InboundMessages.LINK_DROPBOX:
                parameters = gmsg['data']
                key = parameters.get("key")
                msg_data = self.linkDropBox(requestID, key)
            elif msg_type == InboundMessages.GET_DROPBOX_TOKEN:
                # ReceivedObject received_object = new gmsg['data'], ReceivedObject.class);
                msg_data = self.getDropboxToken(requestID)
            elif msg_type == InboundMessages.UNLINK_DROPBOX:
                parameters = gmsg['data']
                key = parameters.get("key")
                msg_data = self.unLinkDropBox(requestID, key)
            elif msg_type == InboundMessages.UPLOAD_MODEL:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                format = parameters.get("format")
                aspectPath = parameters.get("aspectPath")
                msg_data = self.uploadModel(aspectPath, projectId, experimentId, format)
            elif msg_type == InboundMessages.UPLOAD_RESULTS:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                format = parameters.get("format")
                aspectPath = parameters.get("aspectPath")
                msg_data = self.uploadResults(aspectPath, projectId, experimentId, format)
            elif msg_type == InboundMessages.DOWNLOAD_RESULTS:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                format = parameters.get("format")
                aspectPath = parameters.get("aspectPath")
                msg_data = self.downloadResults(requestID, aspectPath, projectId, experimentId, format)
            elif msg_type == InboundMessages.EXPERIMENT_STATUS:
                msg_data = self.checkExperimentStatus(requestID, gmsg['data'])



            elif msg_type == InboundMessages.RUN_QUERY_COUNT:
                received_object = gmsg['data']
                msg_data = self.runQueryCount(requestID, received_object.projectId,
                                              self.convertRunnableQueriesDataTransferModel(
                                                  received_object.runnableQueries))
            else:
                pass

        except GeppettoHandlerTypedException as e:
            logging.error('Error occurred during message {} handling'.format(msg_type), exc_info=True)
            self.send_message(requestID, e.msg_type, e.payload)

        except Exception as e:
            logging.error('Unexpected error occurred during message {} handling'.format(msg_type), exc_info=True)
            self.send_message(requestID, OutboundMessages.ERROR, {"error": str(e)})

        if msg_data is not None:
            return_msg_type = lookup_return_msg_type(msg_type)
            self.send_message(requestID, return_msg_type, msg_data)

    @staticmethod
    def get_message_type(gmsg):
        return gmsg['type'].lower()

    def run_query(self, received_object):

        geppetto_project = self.retrieveGeppettoProject(received_object['projectId'])
        runnable_queries = self.convertRunnableQueriesDataTransferModel(received_object['runnableQueries'])
        results = self.geppettoManager.run_query(runnable_queries, geppetto_project)
        msg_data = GeppettoSerializer.serialize(results, True)
        return msg_data

    def fetch_variable(self, received_object):
        try:

            geppetto_project = self.retrieveGeppettoProject(received_object['projectId'])
            results = self.geppettoManager.fetch_variable(received_object['dataSourceId'],
                                                          received_object['variableId'],
                                                          geppetto_project)
            return GeppettoSerializer.serialize(results, True)
        except Exception as e:
            self.error(e, "Error fetching variable " + str(received_object['variableId']))

    def fetch(self, received_object):
        try:
            geppetto_project = self.retrieveGeppettoProject(received_object['projectId'])
            results = self.geppettoManager.fetch(received_object['dataSourceId'],
                                                 received_object['variables'] if 'variables' in received_object else [],
                                                 received_object['instances'] if 'instances' in received_object else [],
                                                 geppetto_project)
            return GeppettoSerializer.serialize(results, True)
        except Exception as e:
            self.error(e, "Error fetching" + str(received_object))

    def send_message(self, requestID, return_msg_type, msg_data):
        msg_data = TransportMessageFactory.getTransportMessage(requestID=requestID, type_=return_msg_type,
                                                               update=msg_data).__dict__
        self.send_message_data(msg_data)
        logging.debug('Send message: %s', return_msg_type)

    def loadProjectFromUrl(self, requestID, urlString):
        data_manager = DataManagerHelper.getDataManager()
        try:
            geppettoProject = data_manager.get_project_from_url(urlString)
        except Exception as e:
            raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT,
                                                f"Error while loading project from url: {urlString}: {e}")
        if geppettoProject == None:
            raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT,
                                                "Project not found")
        else:
            return self.loadGeppettoProject(requestID, geppettoProject, -1)

    def loadProjectFromContent(self, requestID, projectContentJSON):
        dataManager = DataManagerHelper.getDataManager()

        geppettoProject = dataManager.getProjectFromJson(projectContentJSON)
        self.loadGeppettoProject(requestID, geppettoProject, -1)

    def loadGeppettoProject(self, requestID, geppettoProject, experimentId):

        try:
            readOnly = geppettoProject.volatile  # TODO implement logic related to user projects which are not readonly

            self.geppettoManager.load_project(geppettoProject)
            # Here the project is loaded: a runtime project is created with its model

            geppettoProject.geppettoModel = {
                'id': geppettoProject.geppettoModel.id,
                'type': 'MODEL'
            }  # There is something odd here: we are  sending the project without the model, although the model is there. It's the same in Java anyway, we are just having a PersistedData placeholder there. Why not serialize the model together with the project?

            project_message_update = json.dumps({
                'persisted': not geppettoProject.volatile,
                'project': geppettoProject.__dict__,
                'isReadOnly': readOnly
            })
            self.send_message(requestID, OutboundMessages.PROJECT_LOADED, project_message_update)

            runtime_project = self.geppettoManager.get_runtime_project(geppettoProject)

            geppettoModelJSON = GeppettoSerializer.serialize(
                runtime_project.model, False)
            self.send_message(requestID, OutboundMessages.GEPPETTO_MODEL_LOADED, geppettoModelJSON)

            GeppettoSerializer.serialize(
                runtime_project.model, True)  # This is setting synched to true on the model objects

            # TODO handle experiment
        except Exception as e:
            self.error(e, "Could not load geppetto project")

    def loadProjectFromId(self, requestID, projectId, experimentId):
        """ generated source for method loadProjectFromId """
        dataManager = DataManagerHelper.getDataManager()
        try:
            geppettoProject = dataManager.getGeppettoProjectById(projectId)
            if geppettoProject == None:
                raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT,
                                                    "Project not found")
            else:
                self.loadGeppettoProject(requestID, geppettoProject, experimentId)
        except Exception as e:
            raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT, str(e), e)

    def resolveImportType(self, requestID, projectId, typePaths):
        """ generated source for method resolveImportType """
        geppettoProject = self.retrieveGeppettoProject(projectId)
        try:
            geppettoModel = self.geppettoManager.resolve_import_type(typePaths, geppettoProject)
            return GeppettoSerializer.serializeToJSON(geppettoModel, True)
        except IOError as e:
            self.error(e, "Error importing type " + typePaths)
        except GeppettoExecutionException as e:
            self.error(e, "Error importing type " + typePaths)

    def resolveImportValue(self, requestID, projectId, experimentId, path):
        """ generated source for method resolveImportValue """
        geppettoProject = self.retrieveGeppettoProject(projectId)
        experiment = self.retrieveExperiment(experimentId, geppettoProject)
        try:
            geppettoModel = self.geppettoManager.resolve_import_value(path, geppettoProject, experiment)
            return GeppettoSerializer.serialize(geppettoModel, True)
        except IOError as e:
            self.error(e, "Error importing value " + path)
        except GeppettoExecutionException as e:
            self.error(e, "Error importing value " + path)

    def retrieveExperiment(self, experimentID, geppettoProject):
        """ generated source for method retrieveExperiment """
        theExperiment = None
        #  Look for experiment that matches id passed
        for e in geppettoProject.experiments:
            if e.getId() == experimentID:
                #  The experiment is found
                theExperiment = e
                break
        return theExperiment

    def retrieveGeppettoProject(self, projectId):
        """ generated source for method retrieveGeppettoProject """
        dataManager = DataManagerHelper.getDataManager()
        return dataManager.getGeppettoProjectById(projectId)

    def error(self, exception: Exception, errorMessage):
        """ generated source for method error """
        exceptionMessage = ""
        if exception != None:
            exceptionMessage = str(exception)
        error = Error(GeppettoErrorCodes.EXCEPTION, errorMessage, exceptionMessage, 0)
        logging.error(errorMessage, exception)

        raise GeppettoHandlerTypedException(OutboundMessages.ERROR, errorMessage) from exception

    def info(self, requestID, message):
        """ generated source for method info """
        logging.info(message)
        raise GeppettoHandlerTypedException(OutboundMessages.INFO_MESSAGE, message)

    def setConnectionProject(self, geppettoProject):
        """ generated source for method setConnectionProject """
        if self.geppettoProject != None:
            self.geppettoManager.close_project(self.geppettoProject)
        self.geppettoProject = geppettoProject

    def getVersionNumber(self, requestID):
        import pkg_resources  # part of setuptools
        return pkg_resources.require("pygeppetto")[0].version

    def convertRunnableQueriesDataTransferModel(self, runnableQueries):
        from pygeppetto.model.datasources.datasources import RunnableQuery
        return [RunnableQuery(**dt) for dt in runnableQueries]
