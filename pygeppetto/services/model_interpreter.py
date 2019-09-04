class ModelInterpreter():

    def __init__(self):
        pass

    def importType(self, url, typeName, library, commonLibraryAccess):
        raise NotImplemented(
            "{} not implemented in class {}".format(ModelInterpreter.importType.__name__, self.__class__.__name__))

    def importValue(self, importValue):
        raise NotImplemented(
            "{} not implemented in class {}".format(ModelInterpreter.importValue.__name__, self.__class__.__name__))

    def downloadModel(self, pointer, format, aspectConfiguration):
        raise NotImplemented(
            "{} not implemented in class {}".format(ModelInterpreter.downloadModel.__name__, self.__class__.__name__))

    def getSupportedOutputs(self, pointer):
        raise NotImplemented(
            "{} not implemented in class {}".format(ModelInterpreter.getSupportedOutputs.__name__,
                                                    self.__class__.__name__))

    def getName(self):
        raise NotImplemented(
            "{} not implemented in class {}".format(ModelInterpreter.getName.__name__, self.__class__.__name__))

    def getDependentModels(self):
        raise NotImplemented(
            "{} not implemented in class {}".format(ModelInterpreter.getDependentModels.__name__,
                                                    self.__class__.__name__))


# Here we resemble the CreateModelInterpreterServicesVisitor

_model_interpreters = {}


def add_model_interpreter(library, model_interpreter):
    _model_interpreters[library] = model_interpreter


def get_model_interpreter(library_id) -> ModelInterpreter:
    return get_model_interpreter_from_library(library_id)


def get_model_interpreter_from_library(library) -> ModelInterpreter:
    library_id = library.id
    if library_id not in _model_interpreters:
        raise ModelInterpreterNotFound("No interpreter found for library {}".format(library_id))
    return _model_interpreters[library_id]


class ModelInterpreterNotFound(Exception): pass


def get_model_interpreter_from_type(geppetto_model_type) -> ModelInterpreter:
    '''

    :param geppetto_model_type: EObject
    :return:
    '''
    library = geppetto_model_type.eContainer().id
    return get_model_interpreter_from_library(library)
