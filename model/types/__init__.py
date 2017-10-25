from .types import getEClassifier, eClassifiers
from .types import name, nsURI, nsPrefix, eClass
from .types import Type, VisualType, ImportType, CompositeType, PointerType, QuantityType, ParameterType, StateVariableType, DynamicsType, ArgumentType, ExpressionType, HTMLType, TextType, URLType, PointType, ArrayType, CompositeVisualType, ConnectionType, SimpleType, ImageType
from . import types
from .. import model

__all__ = ['Type', 'VisualType', 'ImportType', 'CompositeType', 'PointerType', 'QuantityType', 'ParameterType', 'StateVariableType', 'DynamicsType', 'ArgumentType', 'ExpressionType', 'HTMLType', 'TextType', 'URLType', 'PointType', 'ArrayType', 'CompositeVisualType', 'ConnectionType', 'SimpleType', 'ImageType']

eSubpackages = []
eSuperPackage = model
types.eSubpackages = eSubpackages


# Manage all other EClassifiers (EEnum, EDatatypes...)
otherClassifiers = []
for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif._container = types

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
