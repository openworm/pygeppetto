from .types import getEClassifier, eClassifiers
from .types import name, nsURI, nsPrefix, eClass
from .types import Type, VisualType, ImportType, CompositeType, PointerType, QuantityType, ParameterType, \
    StateVariableType, DynamicsType, ArgumentType, ExpressionType, HTMLType, JSONType, TextType, URLType, PointType, \
    ArrayType, CompositeVisualType, ConnectionType, SimpleType, ImageType, SimpleArrayType

from model import DomainModel, Tag
from model.values import Point, URL, Text, AArrayValue, Expression, Quantity, Pointer, Composite, Argument, Image, \
    VisualValue, Dynamics, JSON, HTML, VisualGroup, ArrayValue
from model.variables import Variable

from . import types
from .. import model

__all__ = ['Type', 'VisualType', 'ImportType', 'CompositeType', 'PointerType', 'QuantityType', 'ParameterType',
           'StateVariableType', 'DynamicsType', 'ArgumentType',
           'ExpressionType', 'HTMLType', 'JSONType', 'TextType', 'URLType', 'PointType', 'ArrayType',
           'CompositeVisualType', 'ConnectionType', 'SimpleType', 'ImageType', 'SimpleArrayType']

eSubpackages = []
eSuperPackage = model
types.eSubpackages = eSubpackages
types.eSuperPackage = eSuperPackage

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
