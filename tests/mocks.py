from pygeppetto.model import GeppettoModel, GeppettoLibrary, CompositeType, Variable
from pygeppetto.model.model_factory import GeppettoModelFactory


class MockModelInterpreter:

    def __init__(self):
        self.factory = GeppettoModelFactory(GeppettoModelFactory.createGeppettoModel('test'))

    def create_model(self, url=None, typeName='MyGeppettoModel', library='mylib', commonLibraryAccess=None):
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
        flib = GeppettoLibrary(id=library)
        model = GeppettoModel(id='typeName', name=typeName, libraries=[flib])

        v1 = self.factory.createStateVariable(id='v1', initialValue=self.factory.createTimeSeries('ts1', [1, 2, 3]))
        v2 = self.factory.createStateVariable(id='v2', initialValue=self.factory.createTimeSeries('ts1', [1, 2, 3]))
        v3 = Variable(id='v3')
        model.variables.append(v1)
        model.variables.append(v2)
        model.variables.append(v3)

        v31 = self.factory.createStateVariable(id='v31', initialValue=self.factory.createImportValue())
        v32 = self.factory.createStateVariable(id='v32', initialValue=self.factory.createTimeSeries('ts1', [1, 2, 3]))

        ct = CompositeType(name='ct1', id='ct1', variables=[v31, v32])
        flib.types.append(ct)
        v3.types.append(ct)

        return model

    def importValue(self, importValue):
        return self.factory.createTimeSeries('tsx', [4, 5, 6])

    def downloadModel(self, pointer, format, aspectConfiguration):
        pass

    def getSupportedOutputs(self, pointer):
        pass

    def getName(self):
        pass

    def getDependentModels(self):
        pass
