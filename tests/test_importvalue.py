import pygeppetto.model.utils.pointer_utility as pointer_utility
from pygeppetto.constants import UserPrivileges
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, LocalUserGroup
from pygeppetto.managers import geppetto_manager
from pygeppetto.model.values import ImportValue
from pygeppetto.services.model_interpreter import add_model_interpreter

from .mocks import MockModelInterpreter


class ImportValueTest(object):

    def __init__(self):
        group = LocalUserGroup(name='TestGroup', privileges=(UserPrivileges.READ_PROJECT,))
        self.model_interpreter = MockModelInterpreter()
        self.geppetto_model = self.model_interpreter.importType(library='mocklibrary')
        self.geppetto_project = LocalGeppettoProject(name='TestProject', experiments=None,
                                                     geppetto_model=self.geppetto_model, id_=None,
                                                     url_base=None)
        self.geppetto_project.volatile = True
        self.geppetto_manager = geppetto_manager.GeppettoManager()
        self.geppetto_manager.user = LocalUser(id=1, name='TestUser', projects=(self.geppetto_project,),
                                               group=group)
        self.geppetto_manager.load_project(self.geppetto_project)

        add_model_interpreter('mocklibrary', self.model_interpreter)

    def test_importvalue(self):
        assert ImportValue == type(
            pointer_utility.findVariable(type_=self.geppetto_model, variablename='v1').initialValues[0].value)
        assert 1 == \
               pointer_utility.findVariable(type_=self.geppetto_model, variablename='v2').initialValues[0].value.value[
                   0]

        model = self.geppetto_manager.resolve_import_value(path='v1', geppetto_project=self.geppetto_project,
                                                           experiment=None)
        assert model is not None
        assert not pointer_utility.findVariable(type_=model, variablename='v1').synched
        assert pointer_utility.findVariable(type_=model, variablename='v2').synched
        assert pointer_utility.findVariable(type_=model, variablename='v3').synched
        assert 4 == pointer_utility.findVariable(type_=model, variablename='v1').initialValues[0].value.value[0]
