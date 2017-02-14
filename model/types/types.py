from pyecore.ecore import *
import pyecore.ecore as Ecore
from model import ISynchable
from model import Node

name = 'types'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//types'
nsPrefix = 'gep'

eClass = Ecore.EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)




@abstract
class Type(Node):
    abstract = EAttribute(eType=EBoolean)
    superType = EReference(upper=-1)
    visualType = EReference()
    referencedVariables = EReference(upper=-1)
    domainModel = EReference()

    def __init__(self):
        super().__init__()

    def getDefaultValue(self):
        raise NotImplementedError('Operation getDefaultValue(...) is not yet implemented')

    def extendsType(self, type):
        raise NotImplementedError('Operation extendsType(...) is not yet implemented')


class VisualType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ImportType(Type):
    url = EAttribute(eType=EString)
    referenceURL = EAttribute(eType=EString)
    modelInterpreterId = EAttribute(eType=EString)

    def __init__(self):
        super().__init__()


class CompositeType(Type):
    variables = EReference(upper=-1, containment=True)
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class PointerType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class QuantityType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ParameterType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class StateVariableType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class DynamicsType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ArgumentType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ExpressionType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class HTMLType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class TextType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class URLType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class PointType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ArrayType(Type):
    size = EAttribute(eType=EInt)
    arrayType = EReference()
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ConnectionType(Type):
    variables = EReference(upper=-1, containment=True)
    defaultValue = EReference(containment=True)

    def __init__(self):
        super().__init__()


class SimpleType(Type):
    def __init__(self):
        super().__init__()


class ImageType(Type):
    defaultValue = EReference()

    def __init__(self):
        super().__init__()


class CompositeVisualType(VisualType):
    variables = EReference(upper=-1, containment=True)
    visualGroups = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()
