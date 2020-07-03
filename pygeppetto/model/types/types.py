"""Definition of meta model 'types'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from pygeppetto.model import Node, ISynchable
from pyecore.type import Int, String, Boolean


name = 'types'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/master/src/main/resources/geppettoModel.ecore#//types'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


@abstract
class Type(Node):

    abstract = EAttribute(eType=Boolean, derived=False, changeable=True)
    superType = EReference(ordered=True, unique=True, containment=False, upper=-1)
    visualType = EReference(ordered=True, unique=True, containment=False)
    referencedVariables = EReference(ordered=True, unique=True, containment=False, upper=-1)
    domainModel = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, superType=None, abstract=None, visualType=None, referencedVariables=None, domainModel=None, **kwargs):

        super().__init__(**kwargs)

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

        raise NotImplementedError('operation getDefaultValue(...) not yet implemented')

    def extendsType(self, type=None):

        raise NotImplementedError('operation extendsType(...) not yet implemented')


class VisualType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class ImportType(Type):

    url = EAttribute(eType=String, derived=False, changeable=True)
    referenceURL = EAttribute(eType=String, derived=False, changeable=True)
    modelInterpreterId = EAttribute(eType=String, derived=False, changeable=True)
    autoresolve = EAttribute(eType=Boolean, derived=False, changeable=True, default_value=True)

    def __init__(self, url=None, referenceURL=None, modelInterpreterId=None, autoresolve=None, **kwargs):

        super().__init__(**kwargs)

        if url is not None:
            self.url = url

        if referenceURL is not None:
            self.referenceURL = referenceURL

        if modelInterpreterId is not None:
            self.modelInterpreterId = modelInterpreterId

        if autoresolve is not None:
            self.autoresolve = autoresolve


class CompositeType(Type):

    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, variables=None, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if variables:
            self.variables.extend(variables)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class PointerType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class QuantityType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class ParameterType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class StateVariableType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class DynamicsType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class ArgumentType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class ExpressionType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class HTMLType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class JSONType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class TextType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class URLType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class PointType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class ArrayType(Type):

    size = EAttribute(eType=Int, derived=False, changeable=True)
    arrayType = EReference(ordered=True, unique=True, containment=False)
    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, size=None, arrayType=None, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if size is not None:
            self.size = size

        if arrayType is not None:
            self.arrayType = arrayType

        if defaultValue is not None:
            self.defaultValue = defaultValue


class ConnectionType(Type):

    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, variables=None, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if variables:
            self.variables.extend(variables)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class SimpleType(Type):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class ImageType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class SimpleArrayType(Type):

    defaultValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultValue=None, **kwargs):

        super().__init__(**kwargs)

        if defaultValue is not None:
            self.defaultValue = defaultValue


class MetadataType(Type):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class CompositeVisualType(VisualType):

    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    visualGroups = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, variables=None, visualGroups=None, **kwargs):

        super().__init__(**kwargs)

        if variables:
            self.variables.extend(variables)

        if visualGroups:
            self.visualGroups.extend(visualGroups)
