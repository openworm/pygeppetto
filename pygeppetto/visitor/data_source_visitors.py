from pygeppetto.model import Variable, CompoundQuery, ProcessQuery, CompoundRefQuery
from pygeppetto.model.datasources import SimpleQuery
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.visitor import Switch
from pyecore.utils import dispatch

class ExecuteQueryVisitor(Switch):


    def __init__(self, variable: Variable, geppetto_model_access: GeppettoModelAccess):
        self.variable = variable
        self.geppetto_model_access = geppetto_model_access


    @dispatch
    def do_switch(self, query):
        pass

    @do_switch.register(CompoundQuery)
    def case_compound_query(self, query: CompoundQuery):
        pass


    @do_switch.register(ProcessQuery)
    def case_process_query(self, query: ProcessQuery):
        pass


    @do_switch.register(CompoundRefQuery)
    def case_compound_query_ref(self, query: CompoundRefQuery):
        raise NotImplemented


    @do_switch.register(SimpleQuery)
    def case_compound_query(self, query: SimpleQuery):
        pass