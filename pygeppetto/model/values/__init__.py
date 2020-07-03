from pyecore.resources import global_registry
from .values import getEClassifier, eClassifiers
from .values import name, nsURI, nsPrefix, eClass
from .values import Value, Composite, StringToValueMap, Quantity, PhysicalQuantity, Unit, TimeSeries, MDTimeSeries, MetadataValue, Text, URL, HTML, Pointer, PointerElement, Point, Dynamics, FunctionPlot, Function, Argument, Expression, VisualValue, Collada, OBJ, Sphere, Cylinder, Particles, SkeletonAnimation, SkeletonTransformation, VisualGroupElement, VisualGroup, Connection, Connectivity, ArrayElement, ArrayValue, Image, ImageFormat, ImportValue, Metadata, JSON, GenericArray, StringArray, IntArray, DoubleArray, AArrayValue

from pygeppetto.model import Tag
from pygeppetto.model.variables import Variable
from pygeppetto.model.types import Type

from . import values
from .. import model


__all__ = ['Value', 'Composite', 'StringToValueMap', 'Quantity', 'PhysicalQuantity', 'Unit', 'TimeSeries', 'MDTimeSeries', 'MetadataValue', 'Text', 'URL', 'HTML', 'Pointer', 'PointerElement', 'Point', 'Dynamics', 'FunctionPlot', 'Function', 'Argument', 'Expression', 'VisualValue', 'Collada', 'OBJ', 'Sphere',
           'Cylinder', 'Particles', 'SkeletonAnimation', 'SkeletonTransformation', 'VisualGroupElement', 'VisualGroup', 'Connection', 'Connectivity', 'ArrayElement', 'ArrayValue', 'Image', 'ImageFormat', 'ImportValue', 'Metadata', 'JSON', 'GenericArray', 'StringArray', 'IntArray', 'DoubleArray', 'AArrayValue']

eSubpackages = []
eSuperPackage = model
values.eSubpackages = eSubpackages
values.eSuperPackage = eSuperPackage


otherClassifiers = [Connectivity, ImageFormat]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [values] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
