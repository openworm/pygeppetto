from .datasources import getEClassifier, eClassifiers
from .datasources import name, nsURI, nsPrefix, eClass
from .datasources import DataSource, DataSourceLibraryConfiguration, Query, ProcessQuery, SimpleQuery, CompoundQuery, CompoundRefQuery, QueryResults, RunnableQuery, AQueryResult, QueryResult, SerializableQueryResult, QueryMatchingCriteria, BooleanOperator
from . import datasources
from .. import model

__all__ = ['DataSource', 'DataSourceLibraryConfiguration', 'Query', 'ProcessQuery', 'SimpleQuery', 'CompoundQuery', 'CompoundRefQuery', 'QueryResults', 'RunnableQuery', 'AQueryResult', 'QueryResult', 'SerializableQueryResult', 'QueryMatchingCriteria', 'BooleanOperator']

eSubpackages = []
eSuperPackage = model
datasources.eSubpackages = eSubpackages


# Manage all other EClassifiers (EEnum, EDatatypes...)
otherClassifiers = [BooleanOperator]
for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif._container = datasources

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
