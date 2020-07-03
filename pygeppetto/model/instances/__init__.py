from pyecore.resources import global_registry
from .instances import getEClassifier, eClassifiers
from .instances import name, nsURI, nsPrefix, eClass
from .instances import Instance, SimpleInstance, SimpleConnectionInstance

from pygeppetto.model.values import Value, Point, VisualValue
from pygeppetto.model.types import Type
from pygeppetto.model import Tag

from . import instances
from .. import model


__all__ = ['Instance', 'SimpleInstance', 'SimpleConnectionInstance']

eSubpackages = []
eSuperPackage = model
instances.eSubpackages = eSubpackages
instances.eSuperPackage = eSuperPackage


otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [instances] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
