import pytest
from pygeppetto.constants import UserPrivileges
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, \
    LocalUserGroup, \
    LocalExperiment
from pygeppetto.managers import GeppettoManager
from pygeppetto.managers.geppetto_manager import GeppettoExecutionException, \
    GeppettoAccessException, Scope
from pygeppetto.model import GeppettoModel


@pytest.fixture
def manager():
    GeppettoManager._instances = {}
    return GeppettoManager()


@pytest.fixture
def mock__model():
    return GeppettoModel(name='fake_model')


def test__geppettomanager_user_reaffectation(manager, mock__model):
    user1 = LocalUser(id=1, name='user1', group=None)
    user2 = LocalUser(id=2, name='user2', group=None)
    manager.user = user1

    with pytest.raises(GeppettoExecutionException):
        manager.user = user2


def test__geppettomanager_load_project(manager, mock__model):
    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=True)
    project.volatile = True

    assert manager.is_project_open(project) is False
    manager.load_project(project)
    assert manager.is_project_open(project) is True

    # with pytest.raises(GeppettoExecutionException):
    #     manager.load_project(project)

    project = LocalGeppettoProject(name='TestProject2', id=2, geppetto_model=mock__model, volatile=True)
    manager.scope = Scope.RUN
    manager.load_project(project)
    assert manager.is_project_open(project) is True


def test__geppettomanager_load_project_access_rights(manager, mock__model):
    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=False)

    with pytest.raises(GeppettoAccessException):
        manager.load_project(project)

    group = LocalUserGroup(name='TestGroup',
                           privileges=(UserPrivileges.READ_PROJECT,))
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=group)
    manager.load_project(project)
    assert manager.is_project_open(project)


def test__geppettomanager_load_access_no_rights(manager, mock__model):
    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=False)

    group = LocalUserGroup(name='TestGroup')
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=group)
    with pytest.raises(GeppettoAccessException):
        manager.load_project(project)

    group.privileges.append(UserPrivileges.READ_PROJECT)
    del manager.user.projects[0]
    with pytest.raises(GeppettoAccessException):
        manager.load_project(project)


def test__geppettomanager_get_runtime_project(manager, mock__model):
    manager.scope = Scope.RUN

    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=True)
    manager.load_project(project)
    runtime = manager.get_runtime_project(project)
    assert runtime.project is project
    assert project in manager.opened_projects

    project = LocalGeppettoProject(name='TestProject2', id=2, geppetto_model=mock__model, volatile=True)
    runtime = manager.get_runtime_project(project)
    assert runtime.project is project
    assert project in manager.opened_projects

    with pytest.raises(GeppettoExecutionException):
        project = LocalGeppettoProject(name='TestProject3', id=3, geppetto_model=mock__model, volatile=False)
        manager.scope = Scope.CONNECTION
        manager.get_runtime_project(project)


def test__geppettomanager_is_user_project(manager, mock__model):
    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=True)
    project.id = 123456789
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=LocalUserGroup('TestGroup'))

    assert manager.is_user_project(project) is True
    assert manager.is_user_project(project.id) is True

    project = LocalGeppettoProject(name='TestProject2', id=2, geppetto_model=mock__model, volatile=True)
    project.id = 456789123
    assert manager.is_user_project(project) is False
    assert manager.is_user_project(project.id) is False


def test__geppettomanager_close_project(manager, mock__model):
    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=True)
    project.volatile = True

    manager.load_project(project)
    assert manager.is_project_open(project) is True

    manager.close_project(project)
    assert manager.is_project_open(project) is False

    project = LocalGeppettoProject(name='TestProject2', id=2, geppetto_model=mock__model, volatile=True)
    with pytest.raises(GeppettoExecutionException):
        manager.close_project(project)


def test__geppettomanager_load_experiment(manager, mock__model):
    project = LocalGeppettoProject(name='TestProject', id=1, geppetto_model=mock__model, volatile=True)
    experiment = LocalExperiment(name='TestExperiment', project=project)

    group = LocalUserGroup(name='TestGroup')
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=group)

    with pytest.raises(GeppettoAccessException):
        manager.load_experiment(experiment)

    group.privileges.append(UserPrivileges.READ_PROJECT)

    with pytest.raises(GeppettoExecutionException):
        manager.load_experiment(experiment)

    manager.load_project(project)
    state = manager.load_experiment(experiment)

    assert state is not None

def test_geppettomanager_scopes():

    assert GeppettoManager.get_instance(1) is GeppettoManager.get_instance(1), 'Expected same instance for same scope'

    m3 = GeppettoManager.get_instance(3)
    assert GeppettoManager.get_instance(1) is not m3, 'Expected different instances for different scopes'
    m1 = GeppettoManager.get_instance(1)
    GeppettoManager.cleanup_instance(1)
    m1_new = GeppettoManager.get_instance(1)
    assert m1 is not m1_new, 'After cleanup, a new instance should be provided for the scope'
    GeppettoManager.replace_instance(old_scope_id=1, new_scope_id=3)
    assert GeppettoManager.get_instance(3) is m1_new, 'After replace, the scoped instances should me merged into one'
    assert GeppettoManager.get_instance(1) is not m1_new, 'After replace, the old scope should be deleted, then replaced'

