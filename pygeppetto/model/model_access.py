from pygeppetto.model import GeppettoModel, model_utility, World
from pygeppetto.model.exceptions import GeppettoModelException
from pygeppetto.model.model_factory import SharedLibraryManager
from pygeppetto.model.types import ImportType
from pygeppetto.model.utils import pointer_utility
from pyecore.commands import CommandStack, Add, EditingDomain


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

    def get_variable(self, variable_path):
        # TODO support worlds in get_variable
        return pointer_utility.find_variable_from_path(self.geppetto_model, variable_path)

    def get_type(self, type_path):
        return pointer_utility.get_type(self.geppetto_model, type_path)

    def get_value(self, variable_path):
        try:
            return self.get_variable(variable_path).initialValues[0].value
        except Exception as e:
            raise GeppettoModelException("Can't find a value for path " + variable_path) from e

    def get_query(self, query_path):
        return model_utility.get_query(model=self.geppetto_model, query_path=query_path)

    def add_variable_legacy(self, variable):
        # TODO Implement with commands: see https://pyecore.readthedocs.io/en/latest/user/advanced.html#modifying-elements-using-commands

        self.geppetto_model.variables.append(variable)
        self.geppetto_model.synched = False

    def add_variable(self, variable, world_id=None, legacy=False):
        # TODO Implement add_variable with commands: see https://pyecore.readthedocs.io/en/latest/user/advanced.html#modifying-elements-using-commands
        if legacy:
            return self.add_variable_legacy(variable)
        world = self.get_world(world_id)
        world.variables.append(variable)
        world.synched = False
        self.geppetto_model.synched = False

    def get_world(self, world_id=None) -> World:
        if len(self.geppetto_model.worlds) < 1:
            raise GeppettoModelException(f"No world was defined in the geppetto model")
        if len(self.geppetto_model.worlds) > 1:
            raise NotImplementedError("Multiple worlds are not yet supported")
        # TODO support multiple worlds
        if world_id is None:
            return self.geppetto_model.worlds[0]
        try:
            return next(world for world in self.geppetto_model.worlds if world.id == world_id)
        except StopIteration:
            raise GeppettoModelException(f"World not fount in model: {world_id}")

    def add_instance(self, instance, world_name=None):
        # TODO Implement add_instance with commands: see https://pyecore.readthedocs.io/en/latest/user/advanced.html#modifying-elements-using-commands
        world = self.get_world(world_name)
        world.instances.append(instance)
        world.synched = False
        self.geppetto_model.synched = False

    def get_variables(self, world_name=None):
        return self.get_world(world_name).variables

    def get_instances(self, world_name=None):
        return self.get_world(world_name).instances
