class ModelInterpreter():

    def __init__(self):
        pass

    def importType(self, url, typeName, library, commonLibraryAccess):
        pass

    def importValue(self, importValue):
        pass

    def downloadModel(self, pointer, format, aspectConfiguration):
        pass

    def getSupportedOutputs(self, pointer):
        pass

    def getName(self):
        pass

    def getDependentModels(self):
        pass



# Here we resemble the CreateModelInterpreterServicesVisitor

_model_interpreters = {}

def add_model_interpreter(library, model_interpreter):
    _model_interpreters[library] = model_interpreter

def get_model_interpreter_from_library(library_id):
    if library_id not in _model_interpreters:
        raise ModelInterpreterNotFound("No interpreter found for library {}".format(library_id))
    return _model_interpreters[library_id]

class ModelInterpreterNotFound(Exception): pass

def get_model_interpreter_from_type(geppetto_model_type):
    '''

    :param geppetto_model_type: EObject
    :return:
    '''
    library = geppetto_model_type.eContainer().getId()
    return get_model_interpreter_from_library(library)