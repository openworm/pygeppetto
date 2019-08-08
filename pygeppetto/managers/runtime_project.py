from pygeppetto.data_model import GeppettoProject
from pygeppetto.managers.runtime_experiment import RuntimeExperiment
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.types import ImportType
from pygeppetto.model.utils import pointer_utility as PointerUtility, model_traversal, pointer_utility
from pygeppetto.model.utils import url_reader
from pygeppetto.services import model_interpreter

from pygeppetto.model.exceptions import GeppettoExecutionException, ModelInterpreterException


class RuntimeProject(object):
    def __init__(self, project: GeppettoProject, manager):
        """
        :param project: pygeppetto.data_model.GeppettoProject
        :param manager: GeppettoManager
        """
        self.geppetto_manager = manager
        self.project = project
        self.experiments = {}
        self.active_experiment = None
        self.model = project.geppettoModel
        self.geppetto_model_access = GeppettoModelAccess(self.model)
        self.import_types(self.model)

        # TODO handle views
        # TODO handle experiments

    def release(self):
        pass

    def import_types(self, model):
        model_traversal.apply(model, self.import_type,
                              lambda eobject: type(eobject) == ImportType and eobject.autoresolve)

    def import_type(self, itype: ImportType):
        library = itype.eContainer()
        actual_model_interpreter = model_interpreter.get_model_interpreter_from_library(library)
        newtype = actual_model_interpreter.importType(itype.url, itype.id, library, self.geppetto_model_access)
        self.geppetto_model_access.swap_type(itype, newtype)

    def open_experiment(self, experiment):
        self.experiments[experiment] = RuntimeExperiment(self, experiment)
        self.active_experiment = experiment

    def get_runtime_experiment(self, experiment):
        return self.experiments[experiment]

    def __getitem__(self, item):
        return self.get_runtime_experiment(item)

    def resolve_import_value(self, path):
        """
        Retrieves the value from the path and updates the Geppetto Model with the new value
        :param path: the instance path to replace
        :return:
        """
        variable = PointerUtility.find_variable_from_path(self.model, path)

        variable.synched = False  # This will say to the serializer to send the value
        variable_container = variable.eContainer()

        source_library = variable_container.eContainer()

        # here we are simplifying the logic to retrieve the model interpreter. In Java geppetto here we have a switch-visitor call, we don't need that here anyway, unless we're missing something important
        actual_model_interpreter = model_interpreter.get_model_interpreter_from_library(source_library)

        var_to_import = pointer_utility.find_variable_from_path(self.model, path)
        value = var_to_import.initialValues[0].value
        new_value = actual_model_interpreter.importValue(value)

        # Set the new value in replacement of ImportValue
        variable.initialValues[0].value = new_value
        # TODO? it would be nice here to have an api that sets a value and also handles the sync
        variable_container.synched = False
        source_library.synched = False
        return self.model

    def resolve_import_type(self, typePaths):
        """Loads a new Geppetto Model"""

        #  let's find the importType

        for typePath in typePaths:
            type_ = PointerUtility.get_type(self.model, typePath)

            try:
                importedType = None

                # this import type is inside a library
                library = type_.eContainer()
                actual_model_interpreter = model_interpreter.get_model_interpreter(library)
                url = None
                if type_.url != None:
                    url = url_reader.getURL(type_.url, self.project.baseUrl)

                self.model = actual_model_interpreter.importType(url, type_.id, library,
                                                                 self.geppetto_model_access)

                # FIXME to be completed. importType does not return a model

                # TODO if we want to support default view customization, uncomment below and implement
                # if self.gatherDefaultView and actual_model_interpreter.isSupported(
                #         GeppettoFeature.DEFAULT_VIEW_CUSTOMISER_FEATURE):
                #     viewCustomisations.add((actual_model_interpreter.getFeature(
                #         GeppettoFeature.DEFAULT_VIEW_CUSTOMISER_FEATURE)).getDefaultViewCustomisation(
                #         importedType))


            except IOError as e:
                raise GeppettoExecutionException(e)

            except ModelInterpreterException as e:
                raise GeppettoExecutionException(e)

        return self.model

    def populate_new_experiment(self, experiment):
        raise NotImplemented()
