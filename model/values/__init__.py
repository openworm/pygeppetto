from .values import getEClassifier, eClassifiers
from .values import name, nsURI, nsPrefix, eClass
from .values import Value, Composite, StringToValueMap, Quantity, PhysicalQuantity, Unit, TimeSeries, MetadataValue, Text, URL, HTML, Pointer, PointerElement, Point, Dynamics, FunctionPlot, Function, Argument, Expression, VisualValue, Collada, OBJ, Sphere, Cylinder, Particle, SkeletonAnimation, SkeletonTransformation, VisualGroupElement, VisualGroup, Connection, Connectivity, ArrayElement, ArrayValue, Image, ImageFormat, ImportValue
from . import values
from .. import model

__all__ = ['Value', 'Composite', 'StringToValueMap', 'Quantity', 'PhysicalQuantity', 'Unit', 'TimeSeries', 'MetadataValue', 'Text', 'URL', 'HTML', 'Pointer', 'PointerElement', 'Point', 'Dynamics', 'FunctionPlot', 'Function', 'Argument', 'Expression', 'VisualValue', 'Collada', 'OBJ', 'Sphere', 'Cylinder', 'Particle', 'SkeletonAnimation', 'SkeletonTransformation', 'VisualGroupElement', 'VisualGroup', 'Connection', 'Connectivity', 'ArrayElement', 'ArrayValue', 'Image', 'ImageFormat', 'ImportValue']

eSubpackages = []
eSuperPackage = model
values.eSubpackages = eSubpackages


# Manage all other EClassifiers (EEnum, EDatatypes...)
otherClassifiers = [Connectivity, ImageFormat]
for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif._container = values

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
