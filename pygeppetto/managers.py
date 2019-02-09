from .model import ExperimentState
from .local_data_model import UserPrivileges, ExperimentStatus
from enum import Enum, unique
import abc


# Creates a Python 2 and 3 compatible base class
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class GeppettoExecutionException(Exception):
    pass


class GeppettoAccessException(Exception):
    pass


@unique
class Scope(Enum):
    RUN = 0
    CONNECTION = 1


class ProjectManager(object):
    pass


class ExperimentManager(object):
    pass


class ExperimentRunManager(object):
    @classmethod
    def queueExperiment(cls, user, experiment):
        pass


class RuntimeTreeManager(object):
    pass


class DataSourceManager(object):
    pass


class DownloadManager(object):
    pass


class RuntimeProject(object):
    def __init__(self, project, manager):
        self.manager = manager
        self.project = project
        self.experiments = {}
        self.active_experiment = None

    def release(self):
        pass

    def open_experiment(self, experiment):
        self.experiments[experiment] = RuntimeExperiment(self, experiment)
        self.active_experiment = experiment

    def get_runtime_experiment(self, experiment):
        return self.experiments[experiment]


    def __getitem__(self, item):
        return self.get_runtime_experiment(item)


class RuntimeExperiment(object):
    def __init__(self, project, experiment):
        self.projet = project
        self.experiment = experiment
        self.state = ExperimentState()

    def get_experiment_state(self, variables, url_base):
        pass


class GeppettoManager(object):
    def __init__(self, manager=None):
        self.opened_projects = {}
        if manager:
            self.opened_projects.update(manager.opened_projects)
        self.scope = Scope.CONNECTION
        self.user = None

    def is_project_open(self, project):
        return project in self.opened_projects

    def is_user_project(self, project):
        project_id = project
        if hasattr(project, 'id'):
            project_id = project.id
        if self.user:
            return any(p.id == project_id for p in self.user.projects)
        return False

    def load_project(self, project):
        if self.scope is not Scope.RUN:
            if self.user and \
               UserPrivileges.READ_PROJECT not in self.user.group.privileges:
                raise GeppettoAccessException("Insufficient access rights to"
                                              "load project")
            is_user_project = (project.volatile or project.public
                               or self.is_user_project(project.id))
            if not is_user_project:
                raise GeppettoAccessException('Project not found for the '
                                              'current user')

        if self.is_project_open(project):
            raise GeppettoExecutionException('Cannot load two instances of '
                                             'the same project')
        runtime = RuntimeProject(project, self)
        self.opened_projects[project] = runtime
        return runtime

    def close_project(self, project):
        if not self.is_project_open(project):
            raise GeppettoExecutionException('A project without a runtime '
                                             'project cannot be closed')
        # try:
        #     PathConfig.delete_project_tmp_folder(self.scope, project.id)
        # except Exception:
        #     raise GeppettoExecutionException()
        self.opened_projects[project].release()
        del self.opened_projects[project]

    def get_runtime_project(self, project):
        if not self.is_project_open(project):
            try:
                return self.load_project(project)
            except Exception:
                raise GeppettoExecutionException()
        return self.opened_projects[project]

    def load_experiment(self, experiment):
        if self.scope is not Scope.RUN and UserPrivileges.READ_PROJECT not in self.user.group.privileges:
            raise GeppettoAccessException('Insufficient access right to load experiment')

        project = experiment.parent_project
        if not self.is_project_open(project) or self.opened_projects[project] is None:
            raise GeppettoExecutionException('Cannot load an experiment for '
                                             'a project that was not loaded')

        runtime_project = self.get_runtime_project(project)
        try:
            runtime_project.open_experiment(experiment)
        except Exception as e:
            raise GeppettoExecutionException(e)

        return runtime_project[experiment].state

    def run_experiment(self, experiment):
        if self.scope is not Scope.RUN and UserPrivileges.RUN_EXPERIMENT not in self.user.group.privileges:
            raise GeppettoAccessException('Insufficient access right to load experiment')

        if experiment.status is ExperimentStatus.DESIGN:
            ExperimentRunManager.queueExperiment(self.user, experiment)
        else:
            raise GeppettoExecutionException('Cannot run an experiment whose '
                                             'status is not design')


    def get_experiment_state(self, experiment, variables):
        if UserPrivileges.READ_PROJECT not in self.user.group.privileges:
            raise GeppettoAccessException('Insufficient access rights to play '
                                          'experiment');

        if experiment.status is ExperimentStatus.COMPLETED:
            project = experiment.parent_project
            url_base = project.url_base
            return self.get_runtime_project(project)[experiment].get_experiment_state(variables, url_base)
        else:
            raise GeppettoExecutionException('Cannot play an experiment whose status is not completed')
