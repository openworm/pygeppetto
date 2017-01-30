from pyecore.ecore import *
import pyecore.ecore as Ecore
from model import ISynchable
from model import Node

name = 'variables'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//variables'
nsPrefix = 'gep'

eClass = Ecore.EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)




class TypeToValueMap(EObject, metaclass=MetaEClass):
    key = EReference()
    value = EReference(containment=True)

    def __init__(self):
        super().__init__()


class Variable(Node):
    static = EAttribute(eType=EBoolean)
    anonymousTypes = EReference(upper=-1, containment=True)
    types = EReference(upper=-1)
    initialValues = EReference(upper=-1, containment=True)
    position = EReference(containment=True)

    def __init__(self):
        super().__init__()
