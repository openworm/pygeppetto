
class GeppettoProject(object):

    #TODO remove getters and setters. We still need them here while porting code from Java
    def getName(self): return self.name

    def setName(self, name): self.name = name

    def getExperiments(self): return self.experiments

    def getActiveExperimentId(self): pass

    def setActiveExperimentId(self, experimentId): pass

    def getGeppettoModel(self): return self.geppetto_model

    def isVolatile(self): return self.volatile

    def setVolatile(self, is_project_volatile): self.volatile = is_project_volatile

    def isPublic(self): return self.public

    def setView(self, view): self.view = view

    def getView(self): return self.view

    def getBaseURL(self): return self.url_base

    def setBaseURL(self, base_url): self.url_base = base_url