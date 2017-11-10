import os.path

class GeppettoManager():

    def __init__(self):
        pass

    def loadProject(self, project):
        pass

    def closeProject(self, project):
        pass

    def deleteProject(self, project):
        pass

    def persistProject(self, project):
        pass

    def checkExperimentsStatus(self, project):
        pass
	
    def makeProjectPublic(self, project, isPublic):
        pass

    def loadExperiment(self, experiment):
        pass

    def newExperiment(self, project):
        pass

    def runExperiment(self, experiment):
        pass
        
    def getExperimentState(self, experiment, filters):
        pass

    def deleteExperiment(self, experiment):
        pass
    
    def cancelExperimentRun(self, experiment):
        pass

    def setExperimentView(self, experiment, project):
        pass
    
    def cloneExperiment(self, project, originalExperiment):
        pass

    def setModelParameters(self, parameters, experiment, project):
        pass

    def setWatchedVariables(self, watchedVariables, experiment, project, watch):
        pass
	
    def resolveImportType(self, typePaths, geppettoProject):
        pass
	
    def resolveImportValue(self, path, experiment, geppettoProject):
        pass


	