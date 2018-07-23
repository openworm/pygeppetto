from enum import Enum, unique


@unique
class UserPrivileges(Enum):
    READ_PROJECT = 'READ_PROJECT'
    WRITE_PROJECT = 'WRITE_PROJECT'
    RUN_EXPERIMENT = 'RUN_EXPERIMENT'
    DROPBOX_INTEGRATION = 'DROPBOX_INTEGRATION'
    DOWNLOAD = 'DOWNLOAD'
    ADMIN = 'ADMIN'


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
    def __init__(self, name, experiments=None, geppetto_model=None, id_=None):
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
