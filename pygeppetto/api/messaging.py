import json

from .outbound_messages import *


class Resources:
    ERROR_LOADING_PROJECT_MESSAGE = "Invalid project file. Double check the information you have entered and try again."

    ERROR_DOWNLOADING_MODEL = "Format not supported"

    UNSUPPORTED_OPERATION = "This deployment of Geppetto doesn't support this operation. Contact info@geppetto.org for more information."

    VOLATILE_PROJECT = "The operation cannot be executed on a volatile project. If you wish to persist the project press the star icon at the top."


class GeppettoTransportMessage:

    def __init__(self, requestID, type_, data):
        self.requestID = requestID
        self.type = type_
        self.data = data


class TransportMessageFactory(object):
    """ generated source for class TransportMessageFactory """
    EMPTY_STRING = ""

    #
    # 	 * Create JSON object with appropriate message for its type
    # 	 * @param id
    # 	 *
    # 	 * @param type - Type of message of requested
    # 	 * @return
    #
    @classmethod
    def getTransportMessage(cls, requestID, type_, update):
        """ generated source for method getTransportMessage """
        messageType = type_

        payload = update if type(update) == dict else {}
        if type_ == ERROR:
            if (type(update) == dict):
                payload.update(update)
            else:
                payload.update({'message': update})
        elif type_ == INFO_MESSAGE:
            payload.update({'message': update})
        elif type_ == ERROR_LOADING_PROJECT:
            payload.update({"message": Resources.ERROR_LOADING_PROJECT_MESSAGE})
        elif type_ == ERROR_DOWNLOADING_MODEL:
            payload.update({"message": Resources.ERROR_DOWNLOADING_MODEL})
        elif type_ == ERROR_DOWNLOADING_RESULTS:
            payload.update({"message": Resources.ERROR_DOWNLOADING_MODEL})
        elif type_ == READ_URL_PARAMETERS:
            pass
        elif type_ == USER_PRIVILEGES:
            payload.update(
                {OutboundMessages.USER_PRIVILEGES: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == PROJECT_LOADED:
            payload.update({OutboundMessages.PROJECT_LOADED: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == GEPPETTO_MODEL_LOADED:
            payload.update(
                {OutboundMessages.GEPPETTO_MODEL_LOADED: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == VARIABLE_FETCHED:
            payload.update(
                {OutboundMessages.VARIABLE_FETCHED: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == FETCHED:
            payload.update(
                {OutboundMessages.FETCHED: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == IMPORT_TYPE_RESOLVED:
            payload.update(
                {OutboundMessages.IMPORT_TYPE_RESOLVED: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == SIMULATION_OVER:
            payload.update(
                {OutboundMessages.SIMULATION_OVER: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == FIRE_SIM_SCRIPTS:
            payload.update({OutboundMessages.GET_SCRIPTS: update if (update != None) else cls.EMPTY_STRING})
        elif type_ == EXPERIMENT_RUNNING:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == EXPERIMENT_STATUS:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == DOWNLOAD_MODEL:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == DOWNLOAD_PROJECT:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == GET_EXPERIMENT_STATE:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == DELETE_EXPERIMENT:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == SIMULATION_CONFIGURATION:
            payload.update({"configuration": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == CLIENT_ID:
            payload.update({"clientID": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == PROJECT_PERSISTED:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == PROJECT_MADE_PUBLIC:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == PROJECT_PROPS_SAVED:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == EXPERIMENT_PROPS_SAVED:
            payload.update({"update": update if (update != None) else cls.EMPTY_STRING})
        elif type_ == DROPBOX_LINKED:
            payload.update({OutboundMessages.DROPBOX_LINKED, update if (update != None) else cls.EMPTY_STRING})
        elif type_ == DROPBOX_UNLINKED:
            payload.update(
                {OutboundMessages.DROPBOX_UNLINKED, update if (update != None) else cls.EMPTY_STRING})
        elif type_ == RESULTS_UPLOADED:
            payload.update(
                {OutboundMessages.RESULTS_UPLOADED, update if (update != None) else cls.EMPTY_STRING})
        elif type_ == MODEL_UPLOADED:
            payload.update({OutboundMessages.MODEL_UPLOADED, update if (update != None) else cls.EMPTY_STRING})
        else:
            payload.update({type_: update if (update != None) else cls.EMPTY_STRING})
        return cls.createTransportMessage(requestID, messageType, json.dumps(payload))

    #
    # 	 * Create JSON object with type and parameters
    # 	 *
    # 	 * @param type - Type of message
    # 	 * @param params - list of name-value pairs representing parameter names and values
    # 	 * @return
    #
    @classmethod
    def createTransportMessage(cls, requestID, type_, data):
        return GeppettoTransportMessage(requestID=requestID, type_=type_, data=data)
