from pyecore.ecore import *
import pyecore.ecore as Ecore

name = 'model'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore'
nsPrefix = 'gep'

eClass = Ecore.EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)


FileFormat = EEnum('FileFormat', literals=['ZIP','HDF5',])


class GeppettoModel(EObject, metaclass=MetaEClass):
    """The root of every Geppetto model"""
    id = EAttribute(eType=EString)
    name = EAttribute(eType=EString)
    variables = EReference(upper=-1, containment=True)
    libraries = EReference(upper=-1, containment=True)
    tags = EReference(upper=-1, containment=True)
    dataSources = EReference(upper=-1, containment=True)
    queries = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()


class LibraryManager(EObject, metaclass=MetaEClass):
    libraries = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()


class ExperimentState(EObject, metaclass=MetaEClass):
    experimentId = EAttribute(eType=ELong)
    projectId = EAttribute(eType=ELong)
    recordedVariables = EReference(upper=-1, containment=True)
    setParameters = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()


class VariableValue(EObject, metaclass=MetaEClass):
    pointer = EReference(containment=True)
    value = EReference(containment=True)

    def __init__(self):
        super().__init__()


class DomainModel(EObject, metaclass=MetaEClass):
    domainModel = EAttribute(eType=EJavaObject)
    format = EReference(containment=True)

    def __init__(self):
        super().__init__()


class ModelFormat(EObject, metaclass=MetaEClass):
    modelFormat = EAttribute(eType=EString)

    def __init__(self):
        super().__init__()


class StringToStringMap(EObject, metaclass=MetaEClass):
    key = EAttribute(eType=EString)
    value = EAttribute(eType=EString)

    def __init__(self):
        super().__init__()


@abstract
class ISynchable(EObject, metaclass=MetaEClass):
    synched = EAttribute(eType=EBoolean)

    def __init__(self):
        super().__init__()


@abstract
class Node(ISynchable):
    id = EAttribute(eType=EString)
    name = EAttribute(eType=EString)
    tags = EReference(upper=-1)

    def __init__(self):
        super().__init__()

    def getPath(self):
        raise NotImplementedError('Operation getPath(...) is not yet implemented')


class Tag(ISynchable):
    name = EAttribute(eType=EString)
    tags = EReference(upper=-1, containment=True)

    def __init__(self):
        super().__init__()


class ExternalDomainModel(DomainModel):
    fileFormat = EAttribute(eType=FileFormat)

    def __init__(self):
        super().__init__()


class GeppettoLibrary(Node):
    types = EReference(upper=-1, containment=True)
    sharedTypes = EReference(upper=-1)

    def __init__(self):
        super().__init__()
