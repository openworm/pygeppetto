from .instances import getEClassifier, eClassifiers
from .instances import name, nsURI, nsPrefix, eClass
from .instances import Instance, SimpleInstance, SimpleConnectionInstance
from . import instances
from .. import model

__all__ = ['Instance', 'SimpleInstance', 'SimpleConnectionInstance']

eSubpackages = []
eSuperPackage = model


# Manage all other EClassifiers (EEnum, EDatatypes...)
otherClassifiers = []
for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif._container = instances

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
