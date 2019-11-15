from pygeppetto.data_model import GeppettoProject
from pygeppetto.managers.runtime_experiment import RuntimeExperiment
from pygeppetto.model import GeppettoModel, model_utility, CompoundRefQuery, DataSource
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.types import ImportType
from pygeppetto.model.utils import model_traversal
from pygeppetto.model.utils import url_reader
from pygeppetto.services import model_interpreter

from pygeppetto.model.exceptions import GeppettoExecutionException, GeppettoModelException
from pygeppetto.services.data_source_service import ServiceCreator, DataSourceService


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
        if isinstance(project.geppettoModel, GeppettoModel):
            self.model = project.geppettoModel
        elif hasattr(project.geppettoModel, 'url'):
            raise NotImplementedError('PersistedData in project is not supported: cannot load model')
        else:
            raise GeppettoModelException('Bad formed project: model is not correctly specified')

        self.geppetto_model_access = GeppettoModelAccess(self.model)
        self.import_autoresolve_types(self.model)
        self.data_source_services = {}

        # TODO handle views
        # TODO handle experiments

    def release(self):
        pass

    def import_autoresolve_types(self, model):
        model_traversal.apply_single(model, self.import_type,
                                     lambda node: type(node) == ImportType and node.autoresolve)

    def import_type(self, itype: ImportType):
        library = itype.eContainer()

        url = itype.url if None is None else url_reader.getURL(itype.url, self.project.base_url)
        actual_model_interpreter = model_interpreter.get_model_interpreter_from_library(library)
        newtype = actual_model_interpreter.importType(url, itype.id, library, self.geppetto_model_access)
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
        variable = self.geppetto_model_access.get_variable(path)

        variable.synched = False  # This will say to the serializer to send the value
        variable_container = variable.eContainer()

        source_library = variable_container.eContainer()

        # here we are simplifying the logic to retrieve the model interpreter. In Java geppetto here we have a switch-visitors call, we don't need that here anyway, unless we're missing something important
        actual_model_interpreter = model_interpreter.get_model_interpreter_from_library(source_library)

        var_to_import = self.geppetto_model_access.get_variable(path)
        value = var_to_import.initialValues[0].value
        new_value = actual_model_interpreter.importValue(value)

        # Set the new value in replacement of ImportValue
        variable.initialValues[0].value = new_value
        # TODO? it would be nice here to have an api that sets a value and also handles the sync
        variable_container.synched = False
        source_library.synched = False
        return self.model

    def resolve_import_type(self, type_paths):
        """Loads types to the model"""

        #  let's find the importType

        for type_path in type_paths:
            itype = self.geppetto_model_access.get_type(type_path)

            try:
                self.import_type(itype)

                # TODO if we want to support default view customization, uncomment below and implement
                # if self.gatherDefaultView and actual_model_interpreter.isSupported(
                #         GeppettoFeature.DEFAULT_VIEW_CUSTOMISER_FEATURE):
                #     viewCustomisations.add((actual_model_interpreter.getFeature(
                #         GeppettoFeature.DEFAULT_VIEW_CUSTOMISER_FEATURE)).getDefaultViewCustomisation(
                #         importedType))
            except Exception as e:
                raise GeppettoExecutionException('Error importing type ' + type_path) from e

        return self.model

    def get_data_source_service(self, data_source: DataSource):
        if not data_source.id in self.data_source_services:
            ds_service = ServiceCreator.get_new_datasource_service_instance(data_source,
                                                                            self.geppetto_model_access)
            self.data_source_services[data_source.id] = ds_service

        return self.data_source_services[data_source.id]

    def populate_new_experiment(self, experiment):
        raise NotImplemented

    def fetch_variable(self, data_source_id, variable_ids):
        """
        Fetch a variable on the geppetto model.
        :return:
        """
        data_source_service = self.get_data_source_service_by_id(data_source_id)

        for variable_id in variable_ids:
            if not variable_id in set(v.id for v in self.model.variables):
                data_source_service.fetch_variable(variable_id)
        return self.model

    def fetch(self, data_source_id, variable_ids, instance_ids):
        """
        Fetch variables and instances on the geppetto model.
        :return:
        """
        data_source_service = self.get_data_source_service_by_id(data_source_id)

        for variable_id in variable_ids:
            if not variable_id in set(v.id for v in self.geppetto_model_access.get_variables()):
                data_source_service.fetch_variable(variable_id)

        for instance_id in instance_ids:
            if not instance_id in set(v.id for v in self.geppetto_model_access.get_instances()):
                data_source_service.fetch_instance(instance_id)
        return self.model

    def run_query(self, queries):
        query = model_utility.get_query(queries[0].queryPath, self.model)
        if isinstance(query, CompoundRefQuery):
            # Use the first query of the chain to have the datasource we want to start from
            query = queries[0].queryPath
        data_source = query.eContainer()
        while not isinstance(data_source, DataSource):
            data_source = data_source.eContainer()
            assert data_source is not None, 'Bad data source definition'
        data_source_service = self.get_data_source_service(data_source)
        return data_source_service.execute(queries)

    def get_data_source_service_by_id(self, data_source_id) -> DataSourceService:
        if not data_source_id in self.data_source_services:
            try:
                ds = next(ds for ds in self.model.dataSources if ds.id == data_source_id)
            except StopIteration:
                raise GeppettoModelException("The datasource service for " + data_source_id + " was not found")
            return self.get_data_source_service(ds)
        return self.data_source_services[data_source_id]


