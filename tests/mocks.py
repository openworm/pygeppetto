import json

from pyecore.resources import ResourceSet, URI
from pygeppetto.data_model import GeppettoProject
from pygeppetto.model import GeppettoModel, GeppettoLibrary, CompositeType, Variable, ProcessQuery, DataSource, \
    QueryResults, SimpleInstance
from pygeppetto.model.datasources import QueryResult
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.types import ImportType
from pygeppetto.model.values import ImportValue
from pygeppetto.services.data_manager import GeppettoDataManager
from pygeppetto.services.data_source_service import QueryProcessor, DataSourceService
from pygeppetto.services.model_interpreter import ModelInterpreter
from tests.test_xmi import filepath


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

        v31 = self.factory.create_state_variable(id='v31', initialValue=ImportValue())
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
        return self.factory.create_time_series(values=[4, 5, 6], unit='s')

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


def model_with_instances_datasource() -> GeppettoModel:
    rset = ResourceSet()
    resource = rset.get_resource(URI(filepath('instances_test.xmi')))
    return resource.contents[0]


class MockQueryProcessor(QueryProcessor):

    def process(self, query: ProcessQuery, data_source: DataSource, variable, results: QueryResults,
                model_access: GeppettoModelAccess) -> QueryResults:
        print("Processing query {}".format(query.id))
        return results


class MockFetchQueryProcessor(QueryProcessor):
    variable_name = "set by MockFetchQueryProcessor"

    def process(self, query: ProcessQuery, data_source: DataSource, query_param, results: QueryResults,
                model_access: GeppettoModelAccess) -> QueryResults:
        print("Processing query {}".format(query.id))

        if "var" in query_param:
            variable = Variable(id=query_param)
            variable.name = self.variable_name
            variable.types.append(model_access.geppetto_common_library.types[0])
            model_access.add_variable(variable)

        else:
            instance = SimpleInstance(id=query_param)
            instance.type = model_access.geppetto_common_library.types[0]
            instance.name = self.variable_name
            model_access.add_instance(instance)
        return results


class MockDataSourceService(DataSourceService):
    def get_template(self):
        return '{"statement":"$QUERY"}'

    def get_connection_type(self):
        return 'POST'

    def process_response(self, response):
        response = json.loads(response[0])['results'][0]
        query_results = QueryResults()
        query_results.header.extend(response['columns'])
        query_results.results.extend(QueryResult(values=r) for r in response['data'])

        return query_results


class MockDataManager(GeppettoDataManager):

    def get_project_from_url(self, url=None):
        project = GeppettoProject(id='mock', name='mock', geppetto_model=model_with_instances_datasource())
        self.projects[project.id] = project
        return project


def neo4j_response():
    # QUERY: "\"statement\": \"MATCH(n) RETURN id(n) as ID, n;\""
    # url: "http://localhost:7474/db/data/transaction/commit"
    return {
        "results": [{
            "columns": ["ID", "n"],
            "data": [
                {
                    "row": [
                        0,
                        {
                            "title": "The Matrix",
                            "released": 1999
                        }
                    ],
                    "meta": [
                        None,
                        {
                            "id": 0,
                            "type": "node",
                            "deleted": False
                        }
                    ]
                },
                {
                    "row": [
                        1,
                        {
                            "released": 1964,
                            "title": "Keanu Reeves"
                        }
                    ],
                    "meta": [
                        None,
                        {
                            "id": 1,
                            "type": "node",
                            "deleted": False
                        }
                    ]
                }
            ]
        }],
        "errors": []
    }


def neo4j_response_error():
    # QUERY: "\"statement\": \"MATCH(n) RETXXXXXXURN (n);\""
    # url: "http://localhost:7474/db/data/transaction/commit"
    return [{
        "results": [],
        "errors": [{
            "code": "Neo.ClientError.Statement.SyntaxError",
            "message": "Invalid input 'X': expected 'e/E' (line 1, column 11 (offset: 10))\\n\\\"MATCH(n) RXTURN (n);\\\"\\n^"
        }]
    }]
