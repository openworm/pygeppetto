import pytest
from pygeppetto.managers import GeppettoManager, GeppettoExecutionException, \
                                GeppettoAccessException, Scope
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, \
                                        LocalUserGroup, UserPrivileges, \
                                        LocalExperiment


def test__geppettomanager_load_project():
    project = LocalGeppettoProject(name='TestProject')
    project.volatile = True
    manager = GeppettoManager()

    assert manager.is_project_open(project) is False
    manager.load_project(project)
    assert manager.is_project_open(project) is True

    with pytest.raises(GeppettoExecutionException):
        manager.load_project(project)

    project = LocalGeppettoProject(name='TestProject2')
    manager.scope = Scope.RUN
    manager.load_project(project)
    assert manager.is_project_open(project) is True


def test__geppettomanager_load_project_access_rights():
    project = LocalGeppettoProject(name='TestProject')

    manager = GeppettoManager()
    with pytest.raises(GeppettoAccessException):
        manager.load_project(project)

    group = LocalUserGroup(name='TestGroup',
                           privileges=(UserPrivileges.READ_PROJECT,))
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=group)
    manager.load_project(project)
    assert manager.is_project_open(project)


def test__geppettomanager_load_access_no_rights():
    project = LocalGeppettoProject(name='TestProject')

    manager = GeppettoManager()
    group = LocalUserGroup(name='TestGroup')
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=group)
    with pytest.raises(GeppettoAccessException):
        manager.load_project(project)

    group.privileges.append(UserPrivileges.READ_PROJECT)
    del manager.user.projects[0]
    with pytest.raises(GeppettoAccessException):
        manager.load_project(project)


def test__geppettomanager_get_runtime_project():
    manager = GeppettoManager()
    manager.scope = Scope.RUN

    project = LocalGeppettoProject(name='TestProject')
    manager.load_project(project)
    runtime = manager.get_runtime_project(project)
    assert runtime.project is project
    assert project in manager.opened_projects

    project = LocalGeppettoProject(name='TestProject2')
    runtime = manager.get_runtime_project(project)
    assert runtime.project is project
    assert project in manager.opened_projects

    with pytest.raises(GeppettoExecutionException):
        project = LocalGeppettoProject(name='TestProject3')
        manager.scope = Scope.CONNECTION
        manager.get_runtime_project(project)


def test__geppettomanager_is_user_project():
    manager = GeppettoManager()

    project = LocalGeppettoProject(name='TestProject')
    project.id = 123456789
    manager.user = LocalUser(id=1, name='TestUser', projects=(project,),
                             group=LocalUserGroup('TestGroup'))

    assert manager.is_user_project(project) is True
    assert manager.is_user_project(project.id) is True

    project = LocalGeppettoProject(name='TestProject2')
    project.id = 456789123
    assert manager.is_user_project(project) is False
    assert manager.is_user_project(project.id) is False


def test__geppettomanager_close_project():
    manager = GeppettoManager()

    project = LocalGeppettoProject(name='TestProject')
    project.volatile = True

    manager.load_project(project)
    assert manager.is_project_open(project) is True

    manager.close_project(project)
    assert manager.is_project_open(project) is False

    project = LocalGeppettoProject(name='TestProject2')
    with pytest.raises(GeppettoExecutionException):
        manager.close_project(project)


def test__geppettomanager_load_experiment():
    manager = GeppettoManager()

    project = LocalGeppettoProject(name='TestProject')
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
