class GeppettoDataManager(object):
    """ generated source for interface IGeppettoDataManager """

    def getName(self):
        raise NotImplemented('No DataManager was defined')

    def isDefault(self):
        return True

    def getUserByLogin(self, login):
        raise NotImplemented('No DataManager was defined')

    def getUserGroupById(self, id):
        raise NotImplemented('No DataManager was defined')

    def getGeppettoProjectById(self, id):
        raise NotImplemented('No DataManager was defined')

    def getAllUsers(self):
        raise NotImplemented('No DataManager was defined')

    def getAllGeppettoProjects(self):
        raise NotImplemented('No DataManager was defined')

    def getGeppettoProjectsForUser(self, login):
        raise NotImplemented('No DataManager was defined')

    def getProjectFromJson(self, gson, json):
        raise NotImplemented('No DataManager was defined')

    def getProjectFromJson_0(self, gson, json, baseURL):
        raise NotImplemented('No DataManager was defined')

    def getExperimentsForProject(self, projectId):
        raise NotImplemented('No DataManager was defined')

    def newSimulationResult(self, parameterPath, results, format):
        raise NotImplemented('No DataManager was defined')

    def addWatchedVariable(self, found, instancePath):
        raise NotImplemented('No DataManager was defined')

    def newPersistedData(self, url, type_):
        raise NotImplemented('No DataManager was defined')

    def newParameter(self, parameterPath, value):
        raise NotImplemented('No DataManager was defined')

    def newExperiment(self, name, description, project):
        raise NotImplemented('No DataManager was defined')

    def newView(self, view, project):
        raise NotImplemented('No DataManager was defined')

    def newView_0(self, view, experiment):
        raise NotImplemented('No DataManager was defined')

    def newUser(self, name, password, persistent, group):
        raise NotImplemented('No DataManager was defined')

    def newUserGroup(self, name, privileges, spaceAllowance, timeAllowance):
        raise NotImplemented('No DataManager was defined')

    def updateUser(self, user, password):
        raise NotImplemented('No DataManager was defined')

    def newAspectConfiguration(self, experiment, instancePath, simulatorConfiguration):
        raise NotImplemented('No DataManager was defined')

    def newSimulatorConfiguration(self, simulator, conversionService, timestep, length, parameters):
        raise NotImplemented('No DataManager was defined')

    def addGeppettoProject(self, project, user):
        raise NotImplemented('No DataManager was defined')

    def makeGeppettoProjectPublic(self, projectId, isPublic):
        raise NotImplemented('No DataManager was defined')

    def deleteGeppettoProject(self, id, user):
        raise NotImplemented('No DataManager was defined')

    def deleteExperiment(self, experiment):
        raise NotImplemented('No DataManager was defined')

    def clearWatchedVariables(self, aspectConfig):
        raise NotImplemented('No DataManager was defined')

    def saveEntity(self, entity):
        raise NotImplemented('No DataManager was defined')

    def saveEntity_0(self, entity):
        raise NotImplemented('No DataManager was defined')

    def saveEntity_1(self, entity):
        raise NotImplemented('No DataManager was defined')

    def cloneExperiment(self, name, description, project, originalExperiment):
        raise NotImplemented('No DataManager was defined')


# Here we resemble the CreateModelInterpreterServicesVisitor

_data_manager = GeppettoDataManager()


def set_data_manager(data_manager):
    _data_manager = data_manager


def get_data_manager() -> GeppettoDataManager:
    return _data_manager


class DataManagerHelper:

    @staticmethod
    def getDataManager():
        return get_data_manager()
