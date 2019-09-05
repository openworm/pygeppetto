import pytest
import pygeppetto.model.utils.pointer_utility as pointer_utility
from pygeppetto.constants import UserPrivileges
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, LocalUserGroup
from pygeppetto.managers.geppetto_manager import GeppettoManager
from pygeppetto.model import GeppettoLibrary, CompositeType
from pygeppetto.model.types import ImportType
from pygeppetto.model.values import ImportValue
from pygeppetto.services.model_interpreter import add_model_interpreter

from .mocks import MockModelInterpreter
from pygeppetto.model.model_serializer import GeppettoModelSerializer


def create_geppetto_model():
    model_interpreter = MockModelInterpreter()
    model_library = GeppettoLibrary(name='mocklibrary', id='mocklibrary')
    geppetto_model = model_interpreter.create_model(library=model_library)
    add_model_interpreter(model_library.id, model_interpreter)
    return geppetto_model


@pytest.fixture
def geppetto_project():
    geppetto_model = create_geppetto_model()
    geppetto_project = LocalGeppettoProject(name='TestProject', experiments=None,
                                            geppetto_model=geppetto_model, id=None)
    geppetto_project.volatile = True
    return geppetto_project


geppetto_manager = None


def create_geppetto_manager():
    global geppetto_manager
    if geppetto_manager is None:
        geppetto_manager = GeppettoManager()

        group = LocalUserGroup('testgroup', privileges=[e for e in UserPrivileges])

        geppetto_manager.user = LocalUser(id=1, name='TestUser', projects=(geppetto_project,), group=group)

    return geppetto_manager


def test_import_value(geppetto_project):
    geppetto_model = geppetto_project.geppettoModel
    geppetto_manager = create_geppetto_manager()
    geppetto_manager.load_project(geppetto_project)
    assert ImportValue == type(pointer_utility.find_variable_from_path(geppetto_model, 'v3.v31').initialValues[0].value)

    GeppettoModelSerializer.serialize(geppetto_model, True)  # now the model is in sync
    model = geppetto_manager.resolve_import_value(path='v3.v31', geppetto_project=geppetto_project,
                                                  experiment=None)
    assert model is not None

    # assert not pointer_utility.find_variable_from_path(model=model, path='v3').eContainer().synched
    # print(GeppettoModelSerializer.serialize(model, True))
    assert not pointer_utility.find_variable_from_path(model=model, path='v3.v31').synched
    assert pointer_utility.find_variable_from_path(model=model, path='v1').synched
    assert pointer_utility.find_variable_from_path(model=model, path='v2').synched
    assert 4 == pointer_utility.find_variable_from_path(model=model, path='v3.v31').initialValues[0].value.value[0]

    # print(GeppettoModelSerializer.serialize(model, True))


def test_import_type(geppetto_project):
    geppetto_model = geppetto_project.geppettoModel

    geppetto_manager = create_geppetto_manager()
    geppetto_manager.load_project(geppetto_project)
    assert ImportType == type(
        pointer_utility.find_variable_from_path(geppetto_model, 'v4').types[0])  # autoresolve = False
    assert CompositeType == type(
        pointer_utility.find_variable_from_path(geppetto_model, 'v5').types[0])  # autoresolve = True

    GeppettoModelSerializer.serialize(geppetto_model, True)  # now the model is in sync
    model = geppetto_manager.resolve_import_type(type_paths=['mocklibrary.v4'], geppetto_project=geppetto_project)
    assert model is not None

    # assert not pointer_utility.find_variable_from_path(model=model, path='v3').eContainer().synched
    # print(GeppettoModelSerializer.serialize(model, True))
    assert pointer_utility.find_variable_from_path(model=model, path='v3.v31').synched
    assert pointer_utility.find_variable_from_path(model=model, path='v1').synched
    assert pointer_utility.find_variable_from_path(model=model, path='v2').synched
    assert pointer_utility.find_variable_from_path(model=model, path='v5').synched

    imported_type = pointer_utility.find_variable_from_path(model=model, path='v4').types[0]
    assert not imported_type.synched
    assert 'ct2' == imported_type.id
    assert 1 == len(imported_type.variables)
    assert imported_type.variables[0].initialValues[0].value.text == 'imported!!!'
    # assert GeppettoModelAccess().get_value('v4.vi') ==
