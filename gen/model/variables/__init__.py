
from .variables import getEClassifier, eClassifiers
from .variables import name, nsURI, nsPrefix, eClass
from .variables import Variable, TypeToValueMap

from model.values import Point, Value
from model.types import Type
from model import Tag

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
