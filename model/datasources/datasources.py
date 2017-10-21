from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from model import ISynchable
from model import Node

name = 'datasources'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//datasources'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


BooleanOperator = EEnum('BooleanOperator', literals=['AND', 'NAND', 'OR'])  # noqa


class DataSourceLibraryConfiguration(EObject):
    __metaclass__ = MetaEClass
    modelInterpreterId = EAttribute(eType=EString)
    format = EAttribute(eType=EString)
    library = EReference()

    def __init__(self, library=None, modelInterpreterId=None, format=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(DataSourceLibraryConfiguration, self).__init__()
        if modelInterpreterId is not None:
            self.modelInterpreterId = modelInterpreterId
        if format is not None:
            self.format = format
        if library is not None:
            self.library = library


class QueryResults(EObject):
    __metaclass__ = MetaEClass
    id = EAttribute(eType=EString)
    header = EAttribute(eType=EString, upper=-1)
    results = EReference(upper=-1, containment=True)

    def __init__(self, id=None, header=None, results=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(QueryResults, self).__init__()
        if id is not None:
            self.id = id
        if header:
            self.header.extend(header)
        if results:
            self.results.extend(results)
    def getValue(self, field, row):
        raise NotImplementedError('Operation getValue(...) is not yet implemented')


class RunnableQuery(EObject):
    __metaclass__ = MetaEClass
    targetVariablePath = EAttribute(eType=EString)
    queryPath = EAttribute(eType=EString)
    booleanOperator = EAttribute(eType=BooleanOperator)

    def __init__(self, targetVariablePath=None, queryPath=None, booleanOperator=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(RunnableQuery, self).__init__()
        if targetVariablePath is not None:
            self.targetVariablePath = targetVariablePath
        if queryPath is not None:
            self.queryPath = queryPath
        if booleanOperator is not None:
            self.booleanOperator = booleanOperator


@abstract
class AQueryResult(EObject):
    __metaclass__ = MetaEClass

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(AQueryResult, self).__init__()


class QueryMatchingCriteria(EObject):
    __metaclass__ = MetaEClass
    type = EReference(upper=-1)

    def __init__(self, type=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(QueryMatchingCriteria, self).__init__()
        if type:
            self.type.extend(type)


class QueryResult(AQueryResult):
    values = EAttribute(eType=EJavaObject, upper=-1)

    def __init__(self, values=None, **kwargs):
        super(QueryResult, self).__init__(**kwargs)
        if values:
            self.values.extend(values)


class SerializableQueryResult(AQueryResult):
    values = EAttribute(eType=EString, upper=-1)

    def __init__(self, values=None, **kwargs):
        super(SerializableQueryResult, self).__init__(**kwargs)
        if values:
            self.values.extend(values)


class DataSource(Node):
    dataSourceService = EAttribute(eType=EString)
    url = EAttribute(eType=EString)
    libraryConfigurations = EReference(upper=-1, containment=True)
    queries = EReference(upper=-1, containment=True)
    dependenciesLibrary = EReference(upper=-1)
    targetLibrary = EReference()
    fetchVariableQuery = EReference(containment=True)

    def __init__(self, dataSourceService=None, libraryConfigurations=None, url=None, queries=None, dependenciesLibrary=None, targetLibrary=None, fetchVariableQuery=None, **kwargs):
        super(DataSource, self).__init__(**kwargs)
        if dataSourceService is not None:
            self.dataSourceService = dataSourceService
        if url is not None:
            self.url = url
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
    description = EAttribute(eType=EString)
    runForCount = EAttribute(eType=EBoolean)
    matchingCriteria = EReference(upper=-1, containment=True)
    returnType = EReference()

    def __init__(self, description=None, matchingCriteria=None, runForCount=None, returnType=None, **kwargs):
        super(Query, self).__init__(**kwargs)
        if description is not None:
            self.description = description
        if runForCount is not None:
            self.runForCount = runForCount
        if matchingCriteria:
            self.matchingCriteria.extend(matchingCriteria)
        if returnType is not None:
            self.returnType = returnType


class ProcessQuery(Query):
    queryProcessorId = EAttribute(eType=EString)
    parameters = EReference(upper=-1, containment=True)

    def __init__(self, parameters=None, queryProcessorId=None, **kwargs):
        super(ProcessQuery, self).__init__(**kwargs)
        if queryProcessorId is not None:
            self.queryProcessorId = queryProcessorId
        if parameters:
            self.parameters.extend(parameters)


class SimpleQuery(Query):
    query = EAttribute(eType=EString)
    countQuery = EAttribute(eType=EString)

    def __init__(self, query=None, countQuery=None, **kwargs):
        super(SimpleQuery, self).__init__(**kwargs)
        if query is not None:
            self.query = query
        if countQuery is not None:
            self.countQuery = countQuery


class CompoundQuery(Query):
    """Compound queries allow creating composite queries which chain together multiple queries. The results of a query in the chain will be fed to the subsequent query."""
    queryChain = EReference(upper=-1, containment=True)

    def __init__(self, queryChain=None, **kwargs):
        super(CompoundQuery, self).__init__(**kwargs)
        if queryChain:
            self.queryChain.extend(queryChain)


class CompoundRefQuery(Query):
    """Compound ref queries make it possible to reference queries from any datasource"""
    queryChain = EReference(upper=-1)

    def __init__(self, queryChain=None, **kwargs):
        super(CompoundRefQuery, self).__init__(**kwargs)
        if queryChain:
            self.queryChain.extend(queryChain)
