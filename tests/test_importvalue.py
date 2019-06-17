import pygeppetto.model.utils.pointer_utility as pointer_utility
from pygeppetto.constants import UserPrivileges
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, LocalUserGroup
from pygeppetto.managers import geppetto_manager
from pygeppetto.model.values import ImportValue
from pygeppetto.services.model_interpreter import add_model_interpreter

from .mocks import MockModelInterpreter

model_interpreter = MockModelInterpreter()
geppetto_model = model_interpreter.create_model(library='mocklibrary')
geppetto_project = LocalGeppettoProject(name='TestProject', experiments=None,
                                        geppetto_model=geppetto_model, id=None)
geppetto_project.volatile = True
geppetto_manager = geppetto_manager.GeppettoManager()

group = LocalUserGroup('testgroup', privileges=[e for e in UserPrivileges])

geppetto_manager.user = LocalUser(id=1, name='TestUser', projects=(geppetto_project,),
                                  group=group)
geppetto_manager.load_project(geppetto_project)

add_model_interpreter('mocklibrary', model_interpreter)
from pygeppetto.model.model_serializer import GeppettoModelSerializer


def test_importvalue():
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

    print(GeppettoModelSerializer.serialize(model, True))
