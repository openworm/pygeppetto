import abc
import functools
from enum import Enum, unique

from pygeppetto.constants import UserPrivileges, ExperimentStatus
from pygeppetto.managers.runtime_project import RuntimeProject



from .experiment_run_manager import ExperimentRunManager

# Creates a Python 2 and 3 compatible base class
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

from pygeppetto.model.exceptions import GeppettoAccessException, GeppettoExecutionException, ModelInterpreterException
import logging


@unique
class Scope(Enum):
    RUN = 0
    CONNECTION = 1


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

    __instances = {}

    @classmethod
    def has_instance(cls, scope_id):
        return scope_id in cls.__instances

    @classmethod
    def replace_instance(cls, old_scope_id, new_scope_id):
        cls.__instances[new_scope_id] = cls.__instances[old_scope_id]
        cls.cleanup_instance(old_scope_id)

    @classmethod
    def cleanup_instance(cls, client_id):
        if client_id in cls.__instances:
            del cls.__instances[client_id]

    @classmethod
    def get_instance(cls, scope_id, scope=Scope.CONNECTION):
        if scope_id not in cls.__instances:
            cls.__instances[scope_id] = GeppettoManager(scope=scope)
        return cls.__instances[scope_id]

    def __init__(self, manager=None, scope=Scope.CONNECTION):
        self.opened_projects = {}
        if manager:
            self.opened_projects.update(manager.opened_projects)
        self.scope = scope
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
            if self.user and UserPrivileges.READ_PROJECT not in self.user.group.privileges:
                raise GeppettoAccessException("Insufficient access rights to"
                                              "load project")
            is_user_project = (project.volatile or project.is_public
                               or self.is_user_project(project.id))
            if not is_user_project:
                raise GeppettoAccessException('Project not found for the '
                                              'current user')

        if self.is_project_open(project):
            logging.warning('Project was already opened: {}'.format(project))
            del self.opened_projects[project]
            # return self.get_runtime_project(project)
            # raise GeppettoExecutionException('Cannot load two instances of the same project')
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

    def get_runtime_project(self, project) -> RuntimeProject:
        if not self.is_project_open(project):
            try:
                return self.load_project(project)
            except Exception as e:
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

    # @ensure(rights=[UserPrivileges.WRITE_PROJECT], message='import value')
    def resolve_import_value(self, path, geppetto_project, experiment=None):
        return self.get_runtime_project(geppetto_project).resolve_import_value(path)

    # @ensure(rights=[UserPrivileges.WRITE_PROJECT], message='import type')
    def resolve_import_type(self, type_paths, geppetto_project):
        return self.get_runtime_project(geppetto_project).resolve_import_type(type_paths)

    def run_query(self, runnable_queries, geppetto_project):
        return self.get_runtime_project(geppetto_project).run_query(runnable_queries)

    def fetch_variable(self, data_source_id, variable_ids, geppetto_project):
        return self.get_runtime_project(geppetto_project).fetch_variable(data_source_id, variable_ids)

    def fetch(self, data_source_id, variable_ids, instance_ids, geppetto_project):
        return self.get_runtime_project(geppetto_project).fetch(data_source_id, variable_ids, instance_ids)




