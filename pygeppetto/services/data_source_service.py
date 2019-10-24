from pygeppetto.model import Query, DataSource, QueryResults
from pygeppetto.model.datasources import RunnableQuery
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.visitor.data_source_visitors import ExecuteQueryVisitor


class GeppettoDataSourceException(Exception): pass

class BooleanOperator:
    AND = 0
    NAND = 1
    OR = 2


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
        """
        Moved from https://github.com/openworm/org.geppetto.datasources/blob/master/src/main/java/org/geppetto/datasources/ExecuteMultipleQueriesVisitor.java
        Implementation is simplified without caching
        :param runnable_query:
        :return:
        """
        variable = self.model_access.get_variable(runnable_query.targetVariablePath)
        query = self.model_access.get_query(runnable_query.queryPath)
        execute_query_visitor = ExecuteQueryVisitor(variable, self.model_access)
        return self.process_response(execute_query_visitor.do_switch(query))

    def merge_results(self, results: dict) -> QueryResults:
        """
            Ported from https://github.com/openworm/org.geppetto.datasources/blob/master/src/main/java/org/geppetto/datasources/ExecuteMultipleQueriesVisitor.java#getResults
        """
        final_results = QueryResults(header=next(iter(results.values())).header)
        first = True
        for result, operator in results:
            if final_results.header != result.header: # TODO test it: may not be supported
                raise GeppettoDataSourceException(
                    "Multiple queries were executed but they returned incompatible headers"
                )
            if operator == BooleanOperator.AND:
                if first:
                    final_results.results += [r for r in result.results]

        #TODO finish
        return final_results

    def process_response(self, response_dict):
        """
        Custom logic to process response
        :param response_dict:
        :return:
        """
        raise NotImplemented
