import pytest
from pygeppetto.managers import GeppettoManager, GeppettoExecutionException, \
                                GeppettoAccessException, Scope
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, \
                                        LocalUserGroup, UserPrivileges


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
