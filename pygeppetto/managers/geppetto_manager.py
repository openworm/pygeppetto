from ..model import ExperimentState
from ..local_data_model import UserPrivileges, ExperimentStatus
from .experiment_run_manager import ExperimentRunManager
from enum import Enum, unique
from ..model.utils.pointer_utility import PointerUtility
import functools
import abc
from ..model.types import StateVariableType
from ..model.services import model_interpreter

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


class RuntimeProject(object):
    def __init__(self, project, manager):
        '''

        :param project: pygeppetto.data_model.GeppettoProject
        :param manager: GeppettoManager
        '''
        self.manager = manager
        self.project = project
        self.experiments = {}
        self.active_experiment = None
        self.model = model_interpreter.get_model_interpreter_from_library(project.getModel())

    def release(self):
        pass

    def open_experiment(self, experiment):
        self.experiments[experiment] = RuntimeExperiment(self, experiment)
        self.active_experiment = experiment

    def get_runtime_experiment(self, experiment):
        return self.experiments[experiment]

    def get_model(self):
        return self.model

    def __getitem__(self, item):
        return self.get_runtime_experiment(item)

    def resolve_import_value(self, path):
        return PointerUtility.get_value(self.model, path, StateVariableType)


class RuntimeExperiment(object):
    def __init__(self, project, experiment):
        self.projet = project
        self.experiment = experiment
        self.state = ExperimentState()

    def get_experiment_state(self, variables, url_base):
        pass


def ensure(rights=None, not_scope=None, message="perform the required action"):
    def inner_user_needs_rights(func):
        @functools.wraps(func)
        def manager_function(self, *args, **kwargs):
            has_wrong_scope = not_scope is None or not_scope is not self.scope
            for right in rights:
                if has_wrong_scope and right not in self.user.group.privileges:
                    raise GeppettoAccessException("Insufficient access rights to "
                                                  + message)
            return func(self, *args, **kwargs)
        return manager_function
    return inner_user_needs_rights


class GeppettoManager(object):
    def __init__(self, manager=None):
        self.opened_projects = {}
        if manager:
            self.opened_projects.update(manager.opened_projects)
        self.scope = Scope.CONNECTION
        self._user = None

    def is_project_open(self, project):
        return project in self.opened_projects

    def is_user_project(self, project):
        project_id = project
        if hasattr(project, 'id'):
            project_id = project.id
        if self.user:
            return any(p.id == project_id for p in self.user.projects)
        return False

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if self._user is not None:
            message = """A GeppettoManager is being reused, an user was already set and the user attribute is beeing set again.
Current user: {}, attempted new user: {}""".format(self._user.name, value.name)
            raise GeppettoExecutionException(message)
        self._user = value

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

    @ensure(not_scope=Scope.RUN, rights=[UserPrivileges.READ_PROJECT],
            message='load experiment')
    def load_experiment(self, experiment):
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

    @ensure(not_scope=Scope.RUN, rights=[UserPrivileges.RUN_EXPERIMENT],
            message='run experiment')
    def run_experiment(self, experiment):
        if experiment.status is ExperimentStatus.DESIGN:
            ExperimentRunManager.queueExperiment(self.user, experiment)
        else:
            raise GeppettoExecutionException('Cannot run an experiment whose '
                                             'status is not design')

    @ensure(rights=[UserPrivileges.READ_PROJECT], message='play experiment')
    def get_experiment_state(self, experiment, variables):
        if experiment.status is ExperimentStatus.COMPLETED:
            project = experiment.parent_project
            url_base = project.url_base
            return self.get_runtime_project(project)[experiment].get_experiment_state(variables, url_base)
        else:
            raise GeppettoExecutionException('Cannot play an experiment whose status is not completed')

    # Not yet tested
    @ensure(rights=[UserPrivileges.WRITE_PROJECT], message='create new experiment')
    def new_experiment(self, project):
        experiment = None  # must implement DataManagerHelper
        try:
            self.get_runtime_project(project).populate_new_experiment(experiment)
        except Exception as e:
            raise GeppettoExecutionException(e)
        return experiment

    @ensure(rights=[UserPrivileges.READ_PROJECT], message='import value')
    def resolve_import_value(self, path, geppetto_project):
        return self.get_runtime_project(geppetto_project).resolve_import_value(path)