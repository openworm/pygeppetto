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
    InboundMessages.RESOLVE_IMPORT_VALUE: OutboundMessages.IMPORT_VALUE_RESOLVED
}


def lookup_return_msg_type(msg_type):
    if msg_type in in_out_msg_lookup:
        return in_out_msg_lookup[msg_type]
    raise RuntimeError("{} not defined into in_out_msg_lookup".format(msg_type))


class GeppettoMessageHandler:
    '''
    Generic message handler: can be subclassed to implement with websocket or other bidirectional means.
    '''
    connection_id = 0
    CLIENT_ID = 'Connection1'

    PRIVILEGES = json.dumps({
        "userName": "Python User",
        "loggedIn": True,
        "hasPersistence": False,
        "privileges": list(up.value for up in UserPrivileges)
    })

    simulationServerConfig = None

    def __init__(self):
        self.geppettoManager = GeppettoManager()
        self.geppettoProject = None

    def sendPrivileges(self):
        self.send_message(None, OutboundMessages.USER_PRIVILEGES, self.PRIVILEGES)

    def sendClientId(self):
        self.send_message(None, OutboundMessages.CLIENT_ID, self.CLIENT_ID)

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
        msg_type = gmsg['type'].lower()
        try:
            if msg_type == InboundMessages.GEPPETTO_VERSION:
                msg_data = self.getVersionNumber(requestID)

            elif msg_type == InboundMessages.RESOLVE_IMPORT_VALUE:
                receivedObject = json.loads(gmsg['data'])
                msg_data = self.resolveImportValue(requestID, receivedObject['projectId'],
                                                   receivedObject['experimentId'],
                                                   receivedObject['path'])

            elif msg_type == InboundMessages.RESOLVE_IMPORT_TYPE:
                receivedObject = gmsg['data']
                msg_data = self.resolveImportType(requestID, receivedObject.projectId,
                                                  receivedObject.paths)
            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_CONTENT:
                self.loadProjectFromContent(requestID, gmsg['data'])
            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_URL:
                msg_data = self.loadProjectFromUrl(requestID, gmsg['data'])

            # TODO From here on, implementation is not complete: just bare porting from Java
            elif msg_type == InboundMessages.USER_PRIVILEGES:
                msg_data = self.checkUserPrivileges(requestID)
            elif msg_type == InboundMessages.NEW_EXPERIMENT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.newExperiment(requestID, projectId)
            elif msg_type == InboundMessages.NEW_EXPERIMENT_BATCH:
                receivedObject = gmsg['data']
                msg_data = self.newExperimentBatch(requestID, receivedObject.projectId, receivedObject)
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
                receivedObject = gmsg['data']
                msg_data = self.saveProjectProperties(requestID, receivedObject.projectId,
                                                      receivedObject.properties)
            elif msg_type == InboundMessages.SAVE_EXPERIMENT_PROPERTIES:
                receivedObject = gmsg['data']
                msg_data = self.saveExperimentProperties(requestID, receivedObject.projectId,
                                                         receivedObject.experimentId,
                                                         receivedObject.properties)
            elif msg_type == InboundMessages.LOAD_EXPERIMENT:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                msg_data = self.loadExperiment(requestID, experimentId, projectId)
            elif msg_type == InboundMessages.GET_SCRIPT:
                receivedObject = gmsg['data']
                msg_data = self.sendScriptData(requestID, receivedObject.projectId,
                                               receivedObject.scriptURL,
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
                receivedObject = gmsg['data']
                msg_data = self.getExperimentState(requestID, receivedObject.experimentId,
                                                   receivedObject.projectId,
                                                   receivedObject.variables)
            elif msg_type == InboundMessages.DELETE_EXPERIMENT:
                receivedObject = gmsg['data']
                msg_data = self.deleteExperiment(requestID, receivedObject.experimentId,
                                                 receivedObject.projectId)
            elif msg_type == InboundMessages.RUN_EXPERIMENT:
                receivedObject = gmsg['data']
                msg_data = self.runExperiment(requestID, receivedObject.experimentId,
                                              receivedObject.projectId)
            elif msg_type == InboundMessages.SET_WATCHED_VARIABLES:
                receivedObject = gmsg['data']
                try:
                    msg_data = self.setWatchedVariables(requestID, receivedObject.variables,
                                                        receivedObject.experimentId,
                                                        receivedObject.projectId,
                                                        receivedObject.watch)
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
                receivedObject = gmsg['data']
                msg_data = self.setParameters(requestID, receivedObject.modelParameters,
                                              receivedObject.projectId,
                                              receivedObject.experimentId)
            elif msg_type == InboundMessages.SET_EXPERIMENT_VIEW:
                receivedObject = gmsg['data']
                msg_data = self.setExperimentView(requestID, receivedObject.view,
                                                  receivedObject.projectId,
                                                  receivedObject.experimentId)
            elif msg_type == InboundMessages.LINK_DROPBOX:
                parameters = gmsg['data']
                key = parameters.get("key")
                msg_data = self.linkDropBox(requestID, key)
            elif msg_type == InboundMessages.GET_DROPBOX_TOKEN:
                # ReceivedObject receivedObject = new gmsg['data'], ReceivedObject.class);
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
            elif msg_type == InboundMessages.FETCH_VARIABLE:
                receivedObject = gmsg['data']
                msg_data = self.fetchVariable(requestID, receivedObject.projectId,
                                              receivedObject.dataSourceId,
                                              receivedObject.variableId)

            elif msg_type == InboundMessages.RUN_QUERY:
                receivedObject = gmsg['data']
                msg_data = self.runQuery(requestID, receivedObject.projectId,
                                         self.convertRunnableQueriesDataTransferModel(
                                             receivedObject.runnableQueries))
            elif msg_type == InboundMessages.RUN_QUERY_COUNT:
                receivedObject = gmsg['data']
                msg_data = self.runQueryCount(requestID, receivedObject.projectId,
                                              self.convertRunnableQueriesDataTransferModel(
                                                  receivedObject.runnableQueries))
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

    def send_message(self, requestID, return_msg_type, msg_data):
        msg_data = TransportMessageFactory.getTransportMessage(requestID=requestID, type_=return_msg_type,
                                                               update=msg_data).__dict__
        self.send_message_data(msg_data)

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
            if self.geppettoProject == None:
                raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT,
                                                    "Project not found")
            else:
                self.loadGeppettoProject(requestID, self.geppettoProject, experimentId)
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

        raise GeppettoHandlerTypedException(OutboundMessages.ERROR, error)

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
        """ generated source for method convertRunnableQueriesDataTransferModel """
        runnableQueriesEMF = EList('')
        from pygeppetto.model.datasources.datasources import RunnableQuery
        for dt in runnableQueries:
            rqEMF = RunnableQuery(targetVariablePath=dt.targetVariablePath, queryPath=dt.queryPath)
            runnableQueriesEMF.append(rqEMF)
        return runnableQueriesEMF
