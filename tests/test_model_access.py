import pytest
import pygeppetto.model.utils.pointer_utility as pointer_utility
from pygeppetto.constants import UserPrivileges
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, LocalUserGroup
from pygeppetto.managers.geppetto_manager import GeppettoManager
from pygeppetto.model import GeppettoLibrary, CompositeType, StateVariableType
from pygeppetto.model.exceptions import GeppettoModelException
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.types import ImportType
from pygeppetto.model.values import ImportValue
from pygeppetto.services.model_interpreter import add_model_interpreter

from .mocks import MockModelInterpreter
from pygeppetto.model.model_serializer import GeppettoModelSerializer


@pytest.fixture
def model_access():
    model_interpreter = MockModelInterpreter()
    model_library = GeppettoLibrary(name='mocklibrary', id='mocklibrary')
    geppetto_model = model_interpreter.create_model(library=model_library)
    add_model_interpreter(model_library.id, model_interpreter)
    return GeppettoModelAccess(geppetto_model)


def test_access(model_access):
    assert CompositeType == type(model_access.get_type('mocklibrary.ct1'))
    assert StateVariableType == type(model_access.get_type('common.StateVariable'))
    assert model_access.get_variable('v3').id == 'v3'
    assert model_access.get_variable('v3.v31').id == 'v31'
    assert model_access.get_variable('v3.v32').id == 'v32'
    with pytest.raises(GeppettoModelException):
        assert model_access.get_value('v3') is None
    assert ImportValue == type(model_access.get_value('v3.v31'))


def test_swap_type(model_access):
    model = model_access.geppetto_model
    GeppettoModelSerializer.serialize(model, True)
    assert model_access.get_variable('v1').synched == True
    assert model_access.get_variable('v3.v31').synched == True

    # Change the state variable to a composite
    model_access.swap_type(model_access.get_type('common.StateVariable'), model_access.get_type('mocklibrary.ct1'))

    assert model_access.get_variable('v1.v32').id == 'v32'
    assert model_access.get_variable('v1').synched == False
    assert model_access.get_variable('v1.v31').synched == False
    assert model_access.get_variable('v3').synched == True
    model_access.get_type('mocklibrary.ct1').synched = False
