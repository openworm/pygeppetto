from pygeppetto.constants import ExperimentStatus

from .data_model import GeppettoProject


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


class LocalGeppettoProject(GeppettoProject):
    pass


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
