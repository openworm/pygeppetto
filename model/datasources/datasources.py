from pyecore.ecore import *
import pyecore.ecore as Ecore
from model import ISynchable
from model import Node

name = 'datasources'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//datasources'
nsPrefix = 'gep'

eClass = Ecore.EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)


BooleanOperator = EEnum('BooleanOperator', literals=['AND','NAND','OR',])


class DataSourceLibraryConfiguration(EObject, metaclass=MetaEClass):
    modelInterpreterId = EAttribute(eType=EString)
    format = EAttribute(eType=EString)
    library = EReference()

    def __init__(self):
        super().__init__()


class QueryResults(EObject, metaclass=MetaEClass):
    id = EAttribute(eType=EString)
    header = EAttribute(eType=EString, upper=-1)
    results = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()

    def getValue(self, field, row):
        raise NotImplementedError('Operation getValue(...) is not yet implemented')


class RunnableQuery(EObject, metaclass=MetaEClass):
    targetVariablePath = EAttribute(eType=EString)
    queryPath = EAttribute(eType=EString)
    booleanOperator = EAttribute(eType=BooleanOperator)

    def __init__(self):
        super().__init__()


@abstract
class AQueryResult(EObject, metaclass=MetaEClass):
    def __init__(self):
        super().__init__()


class QueryMatchingCriteria(EObject, metaclass=MetaEClass):
    type = EReference(upper=-1)

    def __init__(self):
        super().__init__()


class QueryResult(AQueryResult):
    values = EAttribute(eType=EJavaObject, upper=-1)

    def __init__(self):
        super().__init__()


class SerializableQueryResult(AQueryResult):
    values = EAttribute(eType=EString, upper=-1)

    def __init__(self):
        super().__init__()


class DataSource(Node):
    dataSourceService = EAttribute(eType=EString)
    url = EAttribute(eType=EString)
    libraryConfigurations = EReference(upper=-1, containment=True)
    queries = EReference(upper=-1, containment=True)
    dependenciesLibrary = EReference(upper=-1)
    targetLibrary = EReference()
    fetchVariableQuery = EReference(containment=True)

    def __init__(self):
        super().__init__()


@abstract
class Query(Node):
    description = EAttribute(eType=EString)
    runForCount = EAttribute(eType=EBoolean)
    matchingCriteria = EReference(upper=-1, containment=True)
    returnType = EReference()

    def __init__(self):
        super().__init__()


class ProcessQuery(Query):
    queryProcessorId = EAttribute(eType=EString)
    parameters = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()


class SimpleQuery(Query):
    query = EAttribute(eType=EString)
    countQuery = EAttribute(eType=EString)

    def __init__(self):
        super().__init__()


class CompoundQuery(Query):
    """Compound queries allow creating composite queries which chain together multiple queries. The results of a query in the chain will be fed to the subsequent query."""
    queryChain = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()


class CompoundRefQuery(Query):
    """Compound ref queries make it possible to reference queries from any datasource"""
    queryChain = EReference(upper=-1)

    def __init__(self):
        super().__init__()
