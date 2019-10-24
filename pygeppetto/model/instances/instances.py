from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from ..model import ISynchable
from ..model import Node
from ..values import Connectivity

name = 'instances'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/master/src/main/resources/geppettoModel.ecore#//instances'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)




@abstract
class Instance(Node):
    type = EReference()
    value = EReference(containment=True)

    def __init__(self, type=None, value=None, **kwargs):
        super().__init__(**kwargs)
        if type is not None:
            self.type = type
        if value is not None:
            self.value = value


class SimpleInstance(Instance):
    visualValue = EReference()
    position = EReference(containment=True)

    def __init__(self, visualValue=None, position=None, **kwargs):
        super().__init__(**kwargs)
        if visualValue is not None:
            self.visualValue = visualValue
        if position is not None:
            self.position = position


class SimpleConnectionInstance(Instance):
    connectivity = EAttribute(eType=Connectivity)
    a = EReference()
    b = EReference()

    def __init__(self, a=None, b=None, connectivity=None, **kwargs):
        super().__init__(**kwargs)
        if connectivity is not None:
            self.connectivity = connectivity
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b
