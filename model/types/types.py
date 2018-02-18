from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from model import ISynchable
from model import Node

name = 'types'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//types'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)




@abstract
class Type(Node):
    abstract = EAttribute(eType=EBoolean)
    superType = EReference(upper=-1)
    visualType = EReference()
    referencedVariables = EReference(upper=-1)
    domainModel = EReference()

    def __init__(self, superType=None, abstract=None, visualType=None, referencedVariables=None, domainModel=None, **kwargs):
        super(Type, self).__init__(**kwargs)
        if abstract is not None:
            self.abstract = abstract
        if superType:
            self.superType.extend(superType)
        if visualType is not None:
            self.visualType = visualType
        if referencedVariables:
            self.referencedVariables.extend(referencedVariables)
        if domainModel is not None:
            self.domainModel = domainModel
    def getDefaultValue(self):
        raise NotImplementedError('Operation getDefaultValue(...) is not yet implemented')
    def extendsType(self, type):
        raise NotImplementedError('Operation extendsType(...) is not yet implemented')


class VisualType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(VisualType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class ImportType(Type):
    url = EAttribute(eType=EString)
    referenceURL = EAttribute(eType=EString)
    modelInterpreterId = EAttribute(eType=EString)

    def __init__(self, url=None, referenceURL=None, modelInterpreterId=None, **kwargs):
        super(ImportType, self).__init__(**kwargs)
        if url is not None:
            self.url = url
        if referenceURL is not None:
            self.referenceURL = referenceURL
        if modelInterpreterId is not None:
            self.modelInterpreterId = modelInterpreterId


class CompositeType(Type):
    variables = EReference(upper=-1, containment=True)
    defaultValue = EReference(containment=True)

    def __init__(self, variables=None, defaultValue=None, **kwargs):
        super(CompositeType, self).__init__(**kwargs)
        if variables:
            self.variables.extend(variables)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class PointerType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(PointerType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class QuantityType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(QuantityType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class ParameterType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(ParameterType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class StateVariableType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(StateVariableType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class DynamicsType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(DynamicsType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class ArgumentType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(ArgumentType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class ExpressionType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(ExpressionType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class HTMLType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(HTMLType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class TextType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(TextType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class URLType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(URLType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class PointType(Type):
    defaultValue = EReference(containment=True)

    def __init__(self, defaultValue=None, **kwargs):
        super(PointType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class ArrayType(Type):
    size = EAttribute(eType=EInt)
    arrayType = EReference()
    defaultValue = EReference(containment=True)

    def __init__(self, size=None, arrayType=None, defaultValue=None, **kwargs):
        super(ArrayType, self).__init__(**kwargs)
        if size is not None:
            self.size = size
        if arrayType is not None:
            self.arrayType = arrayType
        if defaultValue is not None:
            self.defaultValue = defaultValue


class ConnectionType(Type):
    variables = EReference(upper=-1, containment=True)
    defaultValue = EReference(containment=True)

    def __init__(self, variables=None, defaultValue=None, **kwargs):
        super(ConnectionType, self).__init__(**kwargs)
        if variables:
            self.variables.extend(variables)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class SimpleType(Type):

    def __init__(self, **kwargs):
        super(SimpleType, self).__init__(**kwargs)


class ImageType(Type):
    defaultValue = EReference()

    def __init__(self, defaultValue=None, **kwargs):
        super(ImageType, self).__init__(**kwargs)
        if defaultValue is not None:
            self.defaultValue = defaultValue


class CompositeVisualType(VisualType):
    variables = EReference(upper=-1, containment=True)
    visualGroups = EReference(upper=-1, containment=True)

    def __init__(self, variables=None, visualGroups=None, **kwargs):
        super(CompositeVisualType, self).__init__(**kwargs)
        if variables:
            self.variables.extend(variables)
        if visualGroups:
            self.visualGroups.extend(visualGroups)
