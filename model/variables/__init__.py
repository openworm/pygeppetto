from .variables import getEClassifier, eClassifiers
from .variables import name, nsURI, nsPrefix, eClass
from .variables import Variable, TypeToValueMap
from . import variables
from .. import model

__all__ = ['Variable', 'TypeToValueMap']

eSubpackages = []
eSuperPackage = model
variables.eSubpackages = eSubpackages


# Manage all other EClassifiers (EEnum, EDatatypes...)
otherClassifiers = []
for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif._container = variables

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
