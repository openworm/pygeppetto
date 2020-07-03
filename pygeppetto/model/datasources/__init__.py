from pyecore.resources import global_registry
from .datasources import getEClassifier, eClassifiers
from .datasources import name, nsURI, nsPrefix, eClass
from .datasources import DataSource, DataSourceLibraryConfiguration, Query, ProcessQuery, SimpleQuery, CompoundQuery, CompoundRefQuery, QueryResults, RunnableQuery, AQueryResult, QueryResult, SerializableQueryResult, QueryMatchingCriteria, BooleanOperator

from pygeppetto.model import GeppettoLibrary, Tag, StringToStringMap
from pygeppetto.model.types import Type

from . import datasources
from .. import model


__all__ = ['DataSource', 'DataSourceLibraryConfiguration', 'Query', 'ProcessQuery', 'SimpleQuery', 'CompoundQuery', 'CompoundRefQuery',
           'QueryResults', 'RunnableQuery', 'AQueryResult', 'QueryResult', 'SerializableQueryResult', 'QueryMatchingCriteria', 'BooleanOperator']

eSubpackages = []
eSuperPackage = model
datasources.eSubpackages = eSubpackages
datasources.eSuperPackage = eSuperPackage


otherClassifiers = [BooleanOperator]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [datasources] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
