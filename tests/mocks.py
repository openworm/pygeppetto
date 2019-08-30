from pygeppetto.model import GeppettoModel, GeppettoLibrary, CompositeType, Variable
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.types import ImportType
from pygeppetto.services.model_interpreter import ModelInterpreter


class MockModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()

    def create_model(self, url=None, typeName='MyGeppettoModel', library=None, commonLibraryAccess=None):
        '''
        Returns a geppetto model with this structure:

        v1 -> StateVariable ImportValue
        v2 -> StateVariable TimeSeries
        v3 -> compositeType ct1
            v31 -> StateVariable ImportValue
            v32 -> StateVariable TimeSeries

        :param url:
        :param typeName:
        :param library:
        :param commonLibraryAccess:
        :return:
        '''

        model = GeppettoModel(id='typeName', name=typeName, libraries=[self.factory.geppetto_common_library, library])

        v1 = self.factory.create_time_series_variable(id='v1', values=[1, 2, 3], unit='s')
        v2 = self.factory.create_time_series_variable(id='v2', values=[1, 2, 3], unit='s')
        v3 = Variable(id='v3')
        model.variables.append(v1)
        model.variables.append(v2)
        model.variables.append(v3)

        v31 = self.factory.createStateVariable(id='v31', initialValue=self.factory.createImportValue())
        v32 = self.factory.create_time_series_variable(id='v32', values=[1, 2, 3], unit='s')

        ct = CompositeType(name='ct1', id='ct1', variables=[v31, v32])

        library.types.append(ct)
        v3.types.append(ct)

        v4 = Variable(id="v4")
        no_autores_type = ImportType(id="v4", url='/whatever', autoresolve=False)
        library.types.append(no_autores_type)
        v4.types.append(no_autores_type)
        v5 = Variable(id="v5")
        autores_type = ImportType(id="v5", url='/whatever/again', autoresolve=True)
        v5.types.append(autores_type)
        library.types.append(autores_type)

        model.variables.append(v4)
        model.variables.append(v5)
        return model

    def importValue(self, importValue):
        return self.factory.createTimeSeries(values=[4, 5, 6], unit='s')

    def importType(self, url, typeName, library, common_library_access: GeppettoModelAccess):
        assert url is not None
        assert typeName
        assert library
        assert common_library_access
        vi1 = self.factory.create_text_variable(id='vi', text='imported!!!')

        ct = CompositeType(name='ct2', id='ct2', variables=[vi1])
        library.types.append(ct)
        return ct

    def downloadModel(self, pointer, format, aspectConfiguration):
        pass

    def getSupportedOutputs(self, pointer):
        pass

    def getName(self):
        pass

    def getDependentModels(self):
        pass
