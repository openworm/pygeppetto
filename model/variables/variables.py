from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from model import ISynchable
from model import Node

name = 'variables'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//variables'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)




class TypeToValueMap(EObject):
    __metaclass__ = MetaEClass
    key = EReference()
    value = EReference(containment=True)

    def __init__(self, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(TypeToValueMap, self).__init__()
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value


class Variable(Node):
    static = EAttribute(eType=EBoolean)
    anonymousTypes = EReference(upper=-1, containment=True)
    types = EReference(upper=-1)
    initialValues = EReference(upper=-1, containment=True)
    position = EReference(containment=True)

    def __init__(self, anonymousTypes=None, types=None, initialValues=None, static=None, position=None, **kwargs):
        super(Variable, self).__init__(**kwargs)
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
