import unittest
from pygeppetto.managers import geppetto_manager
from pygeppetto.local_data_model import LocalGeppettoProject, LocalUser, LocalUserGroup, UserPrivileges
from pygeppetto.model.types import ImportType
from pygeppetto.model.values import ImportValue
from .mocks import MockModelInterpreter
import pygeppetto.model.utils.pointer_utility as PointerUtility
from pygeppetto.model.services.model_interpreter import add_model_interpreter

class ImportValueTest(unittest.TestCase):


    def setUp(self):
        group = LocalUserGroup(name='TestGroup',
                               privileges=(UserPrivileges.READ_PROJECT,))

        self.model_interpreter = MockModelInterpreter()
        self.geppetto_model = self.model_interpreter.importType(library='mocklibrary')
        self.geppettoProject = LocalGeppettoProject(name='TestProject', experiments=None, geppetto_model=self.geppetto_model, id_=None,
                                                    url_base=None)
        self.geppettoProject.volatile = True
        self.geppettomanager = geppetto_manager.GeppettoManager()
        self.geppettomanager.user = LocalUser(id=1, name='TestUser', projects=(self.geppettoProject,),
                                 group=group)
        self.geppettomanager.load_project(self.geppettoProject)

        self.experiment = object()
        add_model_interpreter('mocklibrary', self.model_interpreter)



    def test_importvalue(self):


        self.assertEqual(ImportValue, type(PointerUtility.findVariable(type_=self.geppetto_model, variablename='v1').initialValues[0].value))
        self.assertEqual(1, PointerUtility.findVariable(type_=self.geppetto_model, variablename='v2').initialValues[0].value.value[0])


        model = self.geppettomanager.resolve_import_value(path='v1', geppetto_project=self.geppettoProject, experiment=None)
        self.assertIsNotNone(model)
        self.assertFalse(PointerUtility.findVariable(type_=model, variablename= 'v1').synched)
        self.assertTrue(PointerUtility.findVariable(type_=model, variablename= 'v2').synched)
        self.assertTrue(PointerUtility.findVariable(type_=model, variablename= 'v3').synched)
        self.assertEqual(4, PointerUtility.findVariable(type_=model, variablename= 'v1').initialValues[0].value.value[0])