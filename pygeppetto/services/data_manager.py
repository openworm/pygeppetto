import json

from pygeppetto.utils import Singleton

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace


class GeppettoDataManager(object, metaclass=Singleton):
    """ generated source for interface IGeppettoDataManager """

    def __init__(self):
        self.projects = {}

    def getName(self):
        raise NotImplemented('Operation not defined yet in default data manager')

    def isDefault(self):
        return True

    def getUserByLogin(self, login):
        raise NotImplemented('Operation not defined yet in default data manager')

    def getUserGroupById(self, id):
        raise NotImplemented('Operation not defined yet in default data manager')

    def getGeppettoProjectById(self, project_id):
        return self.projects.get(project_id, None)

    def getAllUsers(self):
        raise NotImplemented('Operation not defined yet in default data manager')

    def getAllGeppettoProjects(self):
        raise NotImplemented('Operation not defined yet in default data manager')

    def getGeppettoProjectsForUser(self, login):
        raise NotImplemented('Operation not defined yet in default data manager')

    def getProjectFromJson(self, json_str):
        project = json.loads(json_str, object_hook=lambda d: Namespace(**d))
        project.volatile = True
        project.id = hash(json_str)
        self.projects[project.id] = project
        return project

    def getExperimentsForProject(self, projectId):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newSimulationResult(self, parameterPath, results, format):
        raise NotImplemented('Operation not defined yet in default data manager')

    def addWatchedVariable(self, found, instancePath):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newPersistedData(self, url, type_):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newParameter(self, parameterPath, value):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newExperiment(self, name, description, project):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newView(self, view, project):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newView_0(self, view, experiment):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newUser(self, name, password, persistent, group):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newUserGroup(self, name, privileges, spaceAllowance, timeAllowance):
        raise NotImplemented('Operation not defined yet in default data manager')

    def updateUser(self, user, password):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newAspectConfiguration(self, experiment, instancePath, simulatorConfiguration):
        raise NotImplemented('Operation not defined yet in default data manager')

    def newSimulatorConfiguration(self, simulator, conversionService, timestep, length, parameters):
        raise NotImplemented('Operation not defined yet in default data manager')

    def addGeppettoProject(self, project, user):
        raise NotImplemented('Operation not defined yet in default data manager')

    def makeGeppettoProjectPublic(self, projectId, isPublic):
        raise NotImplemented('Operation not defined yet in default data manager')

    def deleteGeppettoProject(self, id, user):
        raise NotImplemented('Operation not defined yet in default data manager')

    def deleteExperiment(self, experiment):
        raise NotImplemented('Operation not defined yet in default data manager')

    def clearWatchedVariables(self, aspectConfig):
        raise NotImplemented('Operation not defined yet in default data manager')

    def saveEntity(self, entity):
        raise NotImplemented('Operation not defined yet in default data manager')

    def saveEntity_0(self, entity):
        raise NotImplemented('Operation not defined yet in default data manager')

    def saveEntity_1(self, entity):
        raise NotImplemented('Operation not defined yet in default data manager')

    def cloneExperiment(self, name, description, project, originalExperiment):
        raise NotImplemented('Operation not defined yet in default data manager')

    def get_project_from_url(self, urlString):
        with open(urlString) as json_file:
            return self.getProjectFromJson(json_file.read())


class DataManagerHelper:
    __data_manager = GeppettoDataManager()

    def __init__(self):
        raise NotImplementedError("DataManagerHelper cannot be instantiated. Call class methods directly instead")

    @classmethod
    def getDataManager(cls) -> GeppettoDataManager:
        return cls.__data_manager

    @classmethod
    def setDataManager(cls, data_manager: GeppettoDataManager):
        cls.__data_manager = data_manager


set_data_manager = DataManagerHelper.setDataManager
get_data_manager = DataManagerHelper.getDataManager
