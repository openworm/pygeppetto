from pygeppetto.model import Query, DataSource, QueryResults, AQueryResult, Variable, SimpleQuery
from pygeppetto.model.datasources import RunnableQuery, BooleanOperator
from pygeppetto.model.exceptions import GeppettoInitializationException
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.utils.datasource import query_check, set_custom_query_result_hash, unset_custom_query_result_hash
from pygeppetto.visitors.data_source_visitors import ExecuteQueryVisitor

ID = "ID"


class GeppettoDataSourceException(Exception): pass


class ServiceCreator(type):
    """
    Collects all subclasses of DataSourceService and enables discovery
    """
    data_source_services = {}

    def __init__(cls, name, bases, dct):
        """Initializing a new DataSourceService class"""
        super().__init__(name, bases, dct)
        if cls.__name__ != 'DataSourceService':
            ServiceCreator.data_source_services[cls.__name__] = cls

    @classmethod
    def get_new_service_instance(mcs, data_source: DataSource, model_access):
        data_source_discovery_id = data_source.dataSourceService
        if not data_source_discovery_id in ServiceCreator.data_source_services:
            raise GeppettoInitializationException(f"The service {data_source_discovery_id} was not found!")
        return mcs.data_source_services[data_source_discovery_id](data_source, model_access)


class QueryProcessor:
    pass


class DataSourceService(metaclass=ServiceCreator):

    def __init__(self, configuration: DataSource, model_access: GeppettoModelAccess):
        self.configuration = configuration
        self.model_access = model_access

    def fetch_variable(self):
        raise NotImplemented

    def execute(self, queries, count_only=False):
        return self.get_results(
            {self.execute_runnable_query(runnable_query): runnable_query.booleanOperator for runnable_query in queries}
        )

    def get_number_of_results(self, queries):
        return len(self.execute(queries, count_only=True).results)

    def get_available_queries(self, variable):
        return [query for query in self.configuration.queries if query_check(query, variable)]

    def execute_runnable_query(self, runnable_query: RunnableQuery, count_only=False):
        """
        Moved from https://github.com/openworm/org.geppetto.datasources/blob/master/src/main/java/org/geppetto/datasources/ExecuteMultipleQueriesVisitor.java
        Implementation is simplified without caching
        :param runnable_query:
        :return:
        """
        variable = None
        if runnable_query.targetVariablePath:
            variable = self.model_access.get_variable(runnable_query.targetVariablePath)
        query = self.model_access.get_query(runnable_query.queryPath)
        execute_query_visitor = ExecuteQueryVisitor(variable, self.model_access, count_only=count_only)
        return self.process_response(execute_query_visitor.do_switch(query))

    def get_results(self, results: dict) -> QueryResults:
        """
            Ported from https://github.com/openworm/org.geppetto.datasources/blob/master/src/main/java/org/geppetto/datasources/ExecuteMultipleQueriesVisitor.java#getResults
        """
        if not results: 
            return QueryResults()
        final_results = QueryResults(header=next(iter(results.keys())).header)
        first = True

        id_index = final_results.header.index(ID)
        set_custom_query_result_hash(id_index)

        for result, operator in results.items():
            if final_results.header != result.header:  # TODO test it: may not be supported
                raise GeppettoDataSourceException(
                    "Multiple queries were executed but they returned incompatible headers"
                )

            if first or operator == BooleanOperator.OR:
                method = final_results.results.update

            elif operator == BooleanOperator.AND:
                method = final_results.results.intersection_update

            elif operator == BooleanOperator.NAND:
                method = final_results.results.difference_update
            else:
                raise GeppettoDataSourceException(f"Missing operator for query result {result}")

            method(r for r in result.results)

            first = False

        unset_custom_query_result_hash()

        return final_results

    def get_connection_type(self):
        raise NotImplementedError("Method get_connection_type must be defined in every DataSourceService"
                                  "and return either `GET` or `POST`.")

    def get_template(self):
        raise NotImplemented

    def process_response(self, response_dict):
        """
        Custom logic to process response
        :param response_dict:
        :return:
        """
        raise NotImplemented
