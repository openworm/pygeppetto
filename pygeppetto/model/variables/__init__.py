from pyecore.resources import global_registry
from .variables import getEClassifier, eClassifiers
from .variables import name, nsURI, nsPrefix, eClass
from .variables import Variable, TypeToValueMap

from pygeppetto.model import Tag
from pygeppetto.model.values import Value, Point
from pygeppetto.model.types import Type

from . import variables
from .. import model


__all__ = ['Variable', 'TypeToValueMap']

eSubpackages = []
eSuperPackage = model
variables.eSubpackages = eSubpackages
variables.eSuperPackage = eSuperPackage


otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [variables] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
