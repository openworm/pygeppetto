"""Definition of meta model 'datasources'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from pygeppetto.model import Node, ISynchable
from pyecore.type import String, Boolean


name = 'datasources'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//datasources'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
BooleanOperator = EEnum('BooleanOperator', literals=['AND', 'NAND', 'OR'])


class DataSourceLibraryConfiguration(EObject, metaclass=MetaEClass):

    modelInterpreterId = EAttribute(eType=String, derived=False, changeable=True)
    format = EAttribute(eType=String, derived=False, changeable=True)
    library = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, library=None, modelInterpreterId=None, format=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if modelInterpreterId is not None:
            self.modelInterpreterId = modelInterpreterId

        if format is not None:
            self.format = format

        if library is not None:
            self.library = library


class QueryResults(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=String, derived=False, changeable=True)
    header = EAttribute(eType=String, derived=False, changeable=True, upper=-1)
    results = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, id=None, header=None, results=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if header:
            self.header.extend(header)

        if results:
            self.results.extend(results)

    def getValue(self, field=None, row=None):

        raise NotImplementedError('operation getValue(...) not yet implemented')


class RunnableQuery(EObject, metaclass=MetaEClass):

    targetVariablePath = EAttribute(eType=String, derived=False, changeable=True)
    queryPath = EAttribute(eType=String, derived=False, changeable=True)
    booleanOperator = EAttribute(eType=BooleanOperator, derived=False,
                                 changeable=True, default_value=BooleanOperator.AND)

    def __init__(self, targetVariablePath=None, queryPath=None, booleanOperator=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if targetVariablePath is not None:
            self.targetVariablePath = targetVariablePath

        if queryPath is not None:
            self.queryPath = queryPath

        if booleanOperator is not None:
            self.booleanOperator = booleanOperator


@abstract
class AQueryResult(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class QueryMatchingCriteria(EObject, metaclass=MetaEClass):

    type = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, type=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if type:
            self.type.extend(type)


class QueryResult(AQueryResult):

    values = EAttribute(eType=EJavaObject, derived=False, changeable=True, upper=-1)

    def __init__(self, values=None, **kwargs):

        super().__init__(**kwargs)

        if values:
            self.values.extend(values)


class SerializableQueryResult(AQueryResult):

    values = EAttribute(eType=String, derived=False, changeable=True, upper=-1)

    def __init__(self, values=None, **kwargs):

        super().__init__(**kwargs)

        if values:
            self.values.extend(values)


class DataSource(Node):

    dataSourceService = EAttribute(eType=String, derived=False, changeable=True)
    url = EAttribute(eType=String, derived=False, changeable=True)
    auth = EAttribute(eType=String, derived=False, changeable=True)
    libraryConfigurations = EReference(ordered=True, unique=True, containment=True, upper=-1)
    queries = EReference(ordered=True, unique=True, containment=True, upper=-1)
    dependenciesLibrary = EReference(ordered=True, unique=True, containment=False, upper=-1)
    targetLibrary = EReference(ordered=True, unique=True, containment=False)
    fetchVariableQuery = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, dataSourceService=None, libraryConfigurations=None, url=None, queries=None, dependenciesLibrary=None, targetLibrary=None, fetchVariableQuery=None, auth=None, **kwargs):

        super().__init__(**kwargs)

        if dataSourceService is not None:
            self.dataSourceService = dataSourceService

        if url is not None:
            self.url = url

        if auth is not None:
            self.auth = auth

        if libraryConfigurations:
            self.libraryConfigurations.extend(libraryConfigurations)

        if queries:
            self.queries.extend(queries)

        if dependenciesLibrary:
            self.dependenciesLibrary.extend(dependenciesLibrary)

        if targetLibrary is not None:
            self.targetLibrary = targetLibrary

        if fetchVariableQuery is not None:
            self.fetchVariableQuery = fetchVariableQuery


@abstract
class Query(Node):

    description = EAttribute(eType=String, derived=False, changeable=True)
    runForCount = EAttribute(eType=Boolean, derived=False, changeable=True, default_value=True)
    matchingCriteria = EReference(ordered=True, unique=True, containment=True, upper=-1)
    returnType = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, description=None, matchingCriteria=None, runForCount=None, returnType=None, **kwargs):

        super().__init__(**kwargs)

        if description is not None:
            self.description = description

        if runForCount is not None:
            self.runForCount = runForCount

        if matchingCriteria:
            self.matchingCriteria.extend(matchingCriteria)

        if returnType is not None:
            self.returnType = returnType


class ProcessQuery(Query):

    queryProcessorId = EAttribute(eType=String, derived=False, changeable=True)
    parameters = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, parameters=None, queryProcessorId=None, **kwargs):

        super().__init__(**kwargs)

        if queryProcessorId is not None:
            self.queryProcessorId = queryProcessorId

        if parameters:
            self.parameters.extend(parameters)


class SimpleQuery(Query):

    query = EAttribute(eType=String, derived=False, changeable=True)
    countQuery = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, query=None, countQuery=None, **kwargs):

        super().__init__(**kwargs)

        if query is not None:
            self.query = query

        if countQuery is not None:
            self.countQuery = countQuery


class CompoundQuery(Query):
    """Compound queries allow creating composite queries which chain together multiple queries. The results of a query in the chain will be fed to the subsequent query."""
    queryChain = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, queryChain=None, **kwargs):

        super().__init__(**kwargs)

        if queryChain:
            self.queryChain.extend(queryChain)


class CompoundRefQuery(Query):
    """Compound ref queries make it possible to reference queries from any datasource"""
    queryChain = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, queryChain=None, **kwargs):

        super().__init__(**kwargs)

        if queryChain:
            self.queryChain.extend(queryChain)
