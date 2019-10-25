from pygeppetto.model import Variable, CompoundQuery, ProcessQuery, CompoundRefQuery
from pygeppetto.model.datasources import SimpleQuery, SerializableQueryResult
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.utils import model_traversal
from pygeppetto.visitors import Switch
from pyecore.utils import dispatch
from pygeppetto.model.exceptions import GeppettoDataSourceException


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

    def merge_results(self, processedResults: QueryResults) -> None: # throws GeppettoDataSourceException
        """ generated source for method mergeResults """
        #  if this arrives from a first query results should be empty, so we automatically assign
        #  processedResults to results
        if self.results != None:
            if not self.ID in self.results.header or not self.ID in processedResults.header:
                raise GeppettoDataSourceException("Cannot merge without an ID in the results")
            
            idsList = set() # str

            #  Extract the index of the id for each list of results
            baseId = results.header.index(self.ID) # int
            mergeId = processedResults.header.index(self.ID) #int

            #  add all the ids from results and processedResults to idsList, a Set that will contain all
            #  unique ids that we can iterate to do a merge of the data
            
            idsList.add([result.values[baseId] for result in results.results])

            idsList.add([result.values[mergeId] for result in processedResults.getResults()])

            # Extract all the headers contained in results and processedResults and put all in mergedResults
            self.results.header.add([column for column in processedResults.header if not column == self.ID])

            self.mergedResults.header.add([column for column in results.header])
                
            lastId = self.mergedResults.header.index(self.ID)

            for id in idsList:
                # This is the real deal, here we iterate all the ids and for each id
                newRecord = None
                resultAdded = False
                for result in results.results:
                    # if the id is found in one of the records contained in results then we set newRecord
                    # to the result found
                    if result.values[baseId] == id:
                        newRecord = result
                        ## FIXME?? why are we not breaking here?
                
                # Then we check the same id in processedResults
                for result in processedResults.results:
                    # If this is found 
                    if result.values[mergeId] == id:
                        # and was not found in the results iteration, then newRecord will be set to this result
                        if newRecord == None:
                            newRecord = result
                        else:
                            # differently we iterate this results per column and we add whatever is present here
                            # that was not present in the previous check, keep in mind that we overwrite also the
                            # columns that were already present
                            for column in processedResults.header:
                                if not column == self.ID:
                                    columnId = processedResults.header.index(column)
                                    newRecord.values.add(result.values[columnId])
                            break
                
                # Finally we check if this id is present also in mergedResults, that carry over all the results
                # from previous queries/compound, if this was already present then we overwrite all the
                # previous informations with the coming one
                for result in self.mergedResults.results:
                    if result.values[lastId] == id and newRecord != None:
                        for column in self.mergedResults.header:
                            if not column == self.ID:
                                columnId = self.mergedResults.header.index(column)
                                result.values.add(newRecord.values[columnId])

                        resultAdded = True
                        break
                # Instead if the id was not present in mergedResult we simply add this record
                if not resultAdded:
                    self.mergedResults.results.add(newRecord)

            self.results = self.mergedResults
        else:
            self.results = processedResults
