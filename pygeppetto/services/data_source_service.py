from pygeppetto.model import Query, DataSource, QueryResults
from pygeppetto.model.datasources import RunnableQuery
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.visitor.data_source_visitors import ExecuteQueryVisitor


class GeppettoDataSourceException(Exception): pass


class DataSourceService:

    def __init__(self, configuration: DataSource, model_access: GeppettoModelAccess):
        self.configuration = configuration
        self.model_access = model_access

    def fetch_variable(self):
        raise NotImplemented

    def execute(self, queries):
        return self.merge_results(
            {self.execute_runnable_query(runnable_query): runnable_query.booleanOperator for runnable_query in queries}
        )

    def get_number_of_results(self, queries):
        raise NotImplemented

    def get_available_queries(self):
        raise NotImplemented

    def execute_runnable_query(self, runnable_query: RunnableQuery):
        '''
        Moved from https://github.com/openworm/org.geppetto.datasources/blob/master/src/main/java/org/geppetto/datasources/ExecuteMultipleQueriesVisitor.java
        Implementation is simplified without caching
        :param runnable_query:
        :return:
        '''
        variable = self.model_access.get_variable(runnable_query.targetVariablePath)
        query = self.model_access.get_query(runnable_query.queryPath)
        execute_query_visitor = ExecuteQueryVisitor(variable, self.model_access)
        return execute_query_visitor.do_switch(query)

    def merge_results(self, results: dict) -> QueryResults:
        final_results = QueryResults()

        for result, operator in results:
            final_results.header += result.header
        return final_results
