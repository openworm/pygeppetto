from pygeppetto.model import GeppettoModel
from pygeppetto.model.model_factory import SharedLibraryManager
from pygeppetto.model.types import ImportType


class GeppettoModelAccess:
    '''Gives access to a model and the common library'''

    def __init__(self, geppetto_model):
        if (type(geppetto_model) == str):
            geppetto_model = self.create_geppetto_model(geppetto_model)
        self.geppetto_model = geppetto_model
        try:
            self.geppetto_common_library = next(lib for lib in self.geppetto_model.libraries if lib.id == 'common')
        except StopIteration:
            self.geppetto_common_library = SharedLibraryManager.get_shared_common_library()
            geppetto_model.libraries.append(self.geppetto_common_library)

    @classmethod
    def create_geppetto_model(cls, name):
        # We create a GeppettoModel instance and we add the common library to it

        geppetto_model = GeppettoModel(name=name, libraries=[SharedLibraryManager.get_shared_common_library()])
        return geppetto_model

    def swap_type(self, itype: ImportType, newtype):
        # TODO test
        newtype.eContainer().synched = False
        for variable in itype.referencedVariables:
            variable.synched = False
            variable.types.clear()
            variable.types.append(newtype)
