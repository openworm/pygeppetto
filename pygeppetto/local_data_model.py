from enum import Enum, unique


@unique
class UserPrivileges(Enum):
    READ_PROJECT = 'READ_PROJECT'
    WRITE_PROJECT = 'WRITE_PROJECT'
    RUN_EXPERIMENT = 'RUN_EXPERIMENT'
    DROPBOX_INTEGRATION = 'DROPBOX_INTEGRATION'
    DOWNLOAD = 'DOWNLOAD'
    ADMIN = 'ADMIN'


@unique
class ExperimentStatus(Enum):
    DESIGN = 'DESIGN'
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    COMPLETED = 'COMPLETED'
    DELETED = 'DELETED'
    CANCELED = 'CANCELED'



class LocalUser(object):
    def __init__(self, id, group, login=None, password=None, name=None,
                 projects=None):
        self.id = id
        self.login = login
        self.password = password
        self.name = name
        self.projects = []
        if projects:
            self.projects.extend(projects)
        self.group = group


class LocalGeppettoProject(object):
    def __init__(self, name, experiments=None, geppetto_model=None, id_=None,
                 url_base=None):
        self.id = id_
        self.active_experiment_id = None
        self.volatile = False
        self.public = False
        self.view = None
        self.model_references = []
        self.name = name
        self.experiments = []
        if experiments:
            self.experiments.extend(experiments)
        self.geppetto_model = geppetto_model
        self.url_base = url_base

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

class LocalUserGroup(object):
    def __init__(self, name, privileges=None, space_allowance=None,
                 time_allowance=None):
        self.id = None
        self.name = name
        self.privileges = []
        if privileges:
            self.privileges.extend(privileges)
        self.space_allowance = space_allowance
        self.simulation_time_allowance = time_allowance


class LocalExperiment(object):
    def __init__(self, name, project, description=None,
                 status=ExperimentStatus.DESIGN, simulation_results=None,
                 script=None, view=None):
        self.id = None
        self.name = name
        self.parent_project = project
        self.description = description
        self.status = status
        self.simulation_results = []
        if simulation_results:
            self.simulation_results.extend(simulation_results)
        self.script = script
        self.view = view
        self.creation_date = None
        self.last_modified = None
        self.start_date = None
        self.last_ran = None
    #
    #
    # private List<LocalAspectConfiguration> aspectConfigurations;
    #
    #
    #
	# private Date creationDate;
    #
	# private Date lastModified;
    #
    #
	# private Date startDate;
    #
	# private Date endDate;
    #
	# private Date lastRan;
