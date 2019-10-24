from pygeppetto.model import Variable, CompoundQuery, ProcessQuery, CompoundRefQuery
from pygeppetto.model.datasources import SimpleQuery
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.utils import model_traversal
from pygeppetto.visitor import Switch
from pyecore.utils import dispatch


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


    @dispatch
    def do_switch(self, query):
        pass

    @do_switch.register(CompoundQuery)
    def case_compound_query(self, query: CompoundQuery):
        if self.count and not query.runForCount:
            return None
        run_query_visitor = ExecuteQueryVisitor(self.variable, self.geppetto_model_access, processing_output_map=self.processing_output_map)
        model_traversal.apply_direct_children_only(query, run_query_visitor)
        self.merge_results(run_query_visitor.results)



    @do_switch.register(ProcessQuery)
    def case_process_query(self, query: ProcessQuery):
        pass


    @do_switch.register(CompoundRefQuery)
    def case_compound_query_ref(self, query: CompoundRefQuery):
        raise NotImplemented


    @do_switch.register(SimpleQuery)
    def case_compound_query(self, query: SimpleQuery):
        pass

    def merge_results(self, results):
        pass