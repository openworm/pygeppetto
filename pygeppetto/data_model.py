
class GeppettoProject(object):

    def __init__(self, id, name, geppetto_model, volatile, base_url=None, public=False, experiments=None, view=None):
        self.id = id
        self.name = name
        self.geppettoModel = geppetto_model  # Beware must use the camelCase here otherwise we cannot import from JSON
        self.baseUrl = base_url
        self.experiments = list(experiments) if experiments is not None else []
        self.activeExperimentId = -1 if not experiments else 0
        self.volatile = volatile
        self.view = view
        self.isPublic = public


    #TODO remove getters and setters. We still need them here while porting code from Java
    def getName(self): return self.name

    def setName(self, name): self.name = name

    def getExperiments(self): return self.experiments

    def getActiveExperimentId(self): pass

    def setActiveExperimentId(self, experimentId): pass

    def getGeppettoModel(self): return self.geppettoModel

    def isVolatile(self): return self.volatile

    def setVolatile(self, is_project_volatile): self.volatile = is_project_volatile

    def isPublic(self): return self.isPublic

    def setView(self, view): self.view = view

    def getView(self): return self.view

    def getBaseURL(self): return self.baseUrl

    def setBaseURL(self, base_url): self.baseUrl = base_url
