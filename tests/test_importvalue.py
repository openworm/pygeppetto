import unittest
from pygeppetto import geppetto_manager
from pygeppetto.local_data_model import LocalGeppettoProject
from pygeppetto.model.types import ImportType
from .mocks import TestModelInterpreter

def get_variable(geppetto_type, variablename):
    for var in geppetto_type.variables:
        if var.id == variablename:
            return var
    assert False, 'Variable not found: {}'.format(variablename)

class ImportValueTest(unittest.TestCase):


    def setUp(self):
        self.model_interpreter = TestModelInterpreter()
        self.model = self.model_interpreter.importType()
        self.geppettoProject = LocalGeppettoProject(name='TestProject', experiments=None, geppetto_model=self.model, id_=None,
                                                    url_base=None)
        self.geppettomanager = geppetto_manager.GeppettoManager()
        self.geppettomanager.loadProject(self.geppettoProject)

        self.experiment = object()



    def test_importvalue(self):


        self.assertEqual(ImportType, type(get_variable(self.model, 'v1').initialValues[0].value))
        self.assertEqual(1, get_variable(self.model, 'v2').initialValues[0].value.value[0])


        model = self.geppettomanager.resolveImportValue(path='v1', experiment=self.experiment, geppettoProject=self.geppettoProject)
        self.assertFalse(get_variable(model, 'v1').synched)
        self.assertTrue(get_variable(model, 'v2').synched)
        self.assertTrue(get_variable(model, 'v3').synched)
        self.assertEqual(4, get_variable(model, 'v1').initialValues[0].value.value[0])