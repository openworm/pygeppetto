from pyecore.resources import global_registry
from .types import getEClassifier, eClassifiers
from .types import name, nsURI, nsPrefix, eClass
from .types import Type, VisualType, ImportType, CompositeType, PointerType, QuantityType, ParameterType, StateVariableType, DynamicsType, ArgumentType, ExpressionType, HTMLType, JSONType, TextType, URLType, PointType, ArrayType, CompositeVisualType, ConnectionType, SimpleType, ImageType, SimpleArrayType, MetadataType

from pygeppetto.model import DomainModel, Tag
from pygeppetto.model.variables import Variable
from pygeppetto.model.values import ArrayValue, Pointer, Quantity, Argument, Text, VisualValue, JSON, VisualGroup, Point, Expression, AArrayValue, Composite, Image, URL, HTML, Dynamics

from . import types
from .. import model


__all__ = ['Type', 'VisualType', 'ImportType', 'CompositeType', 'PointerType', 'QuantityType', 'ParameterType', 'StateVariableType', 'DynamicsType', 'ArgumentType', 'ExpressionType',
           'HTMLType', 'JSONType', 'TextType', 'URLType', 'PointType', 'ArrayType', 'CompositeVisualType', 'ConnectionType', 'SimpleType', 'ImageType', 'SimpleArrayType', 'MetadataType']

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

register_packages = [types] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
