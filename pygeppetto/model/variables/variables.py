"""Definition of meta model 'variables'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from pygeppetto.model import Node, ISynchable
from pyecore.type import Boolean


name = 'variables'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/master/src/main/resources/geppettoModel.ecore#//variables'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class TypeToValueMap(EObject, metaclass=MetaEClass):

    key = EReference(ordered=True, unique=True, containment=False)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if key is not None:
            self.key = key

        if value is not None:
            self.value = value


class Variable(Node):

    static = EAttribute(eType=Boolean, derived=False, changeable=True)
    anonymousTypes = EReference(ordered=True, unique=True, containment=True, upper=-1)
    types = EReference(ordered=True, unique=True, containment=False, upper=-1)
    initialValues = EReference(ordered=True, unique=True, containment=True, upper=-1)
    position = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, anonymousTypes=None, types=None, initialValues=None, static=None, position=None, **kwargs):

        super().__init__(**kwargs)

        if static is not None:
            self.static = static

        if anonymousTypes:
            self.anonymousTypes.extend(anonymousTypes)

        if types:
            self.types.extend(types)

        if initialValues:
            self.initialValues.extend(initialValues)

        if position is not None:
            self.position = position
