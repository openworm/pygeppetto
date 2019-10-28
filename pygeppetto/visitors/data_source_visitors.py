from pygeppetto.model import Variable, CompoundQuery, ProcessQuery, CompoundRefQuery
from pygeppetto.model.datasources import Query, SimpleQuery
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.utils import model_traversal
from pygeppetto.visitors import Switch
from pyecore.utils import dispatch
from pygeppetto.model.exceptions import GeppettoDataSourceException
from pygeppetto.model.datasources.datasources import QueryResults, QueryResult

class ExecuteQueryVisitor(Switch):

    def __init__(self, variable: Variable,
                 geppetto_model_access: GeppettoModelAccess,
                 count_only = False,
                 processing_output_map = None):
        self.variable = variable
        self.geppetto_model_access = geppetto_model_access
        self.count = count_only
        self.results = None
        self.processing_output_map = processing_output_map if processing_output_map else {}
        self.ID = "ID"
        self.merged_results = QueryResults(id="merge_results", 
                                          header=["ID"], 
                                          results=[])


    @dispatch
    def do_switch(self, query):
        raise NotImplemented

    @do_switch.register(CompoundQuery)
    def case_compound_query(self, query: CompoundQuery):
        if self.count and not query.runForCount:
            return None
        run_query_visitor = ExecuteQueryVisitor(self.variable, self.geppetto_model_access, processing_output_map=self.processing_output_map)
        model_traversal.apply_direct_children_only(query, run_query_visitor)
        self.merge_results(run_query_visitor.results)



    @do_switch.register(ProcessQuery)
    def case_process_query(self, query: ProcessQuery):
        pass # TODO ExecuteQueryVisitor.case_process_query


    @do_switch.register(CompoundRefQuery)
    def case_compound_query_ref(self, query: CompoundRefQuery):
        raise NotImplemented


    @do_switch.register(SimpleQuery)
    def case_simple_query(self, query: SimpleQuery):
        pass # TODO ExecuteQueryVisitor.case_simple_query

    def merge_results(self, processed_results: QueryResults):
        #  if this arrives from a first query results should be empty, so we automatically assign
        #  processedResults to results
        if self.results != None:
            if not self.ID in self.results.header or not self.ID in processed_results.header:
                raise GeppettoDataSourceException("Cannot merge without an ID in the results")
            
            id_pos = self.results.header.index(self.ID)
            proc_id_pos = processed_results.header.index(self.ID)

            current_record_ids = [record.values[id_pos] for record in self.results.results]
            self.results.header.update(processed_results.header)
            for record in processed_results.results:
                if not record.values[proc_id_pos] in current_record_ids:
                    self.results.results.add(record)
                else:
                    index = current_record_ids.index(record.values[proc_id_pos])
                    self.results.results[index].values.update(record.values)
        else:
            self.results = processed_results
