from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *

name = 'model'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


FileFormat = EEnum('FileFormat', literals=['ZIP', 'HDF5'])  # noqa


class GeppettoModel(EObject):
    """The root of every Geppetto model"""
    __metaclass__ = MetaEClass
    id = EAttribute(eType=EString)
    name = EAttribute(eType=EString)
    variables = EReference(upper=-1, containment=True)
    libraries = EReference(upper=-1, containment=True)
    tags = EReference(upper=-1, containment=True)
    dataSources = EReference(upper=-1, containment=True)
    queries = EReference(upper=-1, containment=True)

    def __init__(self, variables=None, libraries=None, tags=None, id=None, name=None, dataSources=None, queries=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(GeppettoModel, self).__init__()
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if variables:
            self.variables.extend(variables)
        if libraries:
            self.libraries.extend(libraries)
        if tags:
            self.tags.extend(tags)
        if dataSources:
            self.dataSources.extend(dataSources)
        if queries:
            self.queries.extend(queries)


class LibraryManager(EObject):
    __metaclass__ = MetaEClass
    libraries = EReference(upper=-1, containment=True)

    def __init__(self, libraries=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(LibraryManager, self).__init__()
        if libraries:
            self.libraries.extend(libraries)


class ExperimentState(EObject):
    __metaclass__ = MetaEClass
    experimentId = EAttribute(eType=ELong)
    projectId = EAttribute(eType=ELong)
    recordedVariables = EReference(upper=-1, containment=True)
    setParameters = EReference(upper=-1, containment=True)

    def __init__(self, recordedVariables=None, setParameters=None, experimentId=None, projectId=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(ExperimentState, self).__init__()
        if experimentId is not None:
            self.experimentId = experimentId
        if projectId is not None:
            self.projectId = projectId
        if recordedVariables:
            self.recordedVariables.extend(recordedVariables)
        if setParameters:
            self.setParameters.extend(setParameters)


class VariableValue(EObject):
    __metaclass__ = MetaEClass
    pointer = EReference(containment=True)
    value = EReference(containment=True)

    def __init__(self, pointer=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(VariableValue, self).__init__()
        if pointer is not None:
            self.pointer = pointer
        if value is not None:
            self.value = value


class DomainModel(EObject):
    __metaclass__ = MetaEClass
    domainModel = EAttribute(eType=EJavaObject)
    format = EReference(containment=True)

    def __init__(self, domainModel=None, format=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(DomainModel, self).__init__()
        if domainModel is not None:
            self.domainModel = domainModel
        if format is not None:
            self.format = format


class ModelFormat(EObject):
    __metaclass__ = MetaEClass
    modelFormat = EAttribute(eType=EString)

    def __init__(self, modelFormat=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(ModelFormat, self).__init__()
        if modelFormat is not None:
            self.modelFormat = modelFormat


class StringToStringMap(EObject):
    __metaclass__ = MetaEClass
    key = EAttribute(eType=EString)
    value = EAttribute(eType=EString)

    def __init__(self, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(StringToStringMap, self).__init__()
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value


@abstract
class ISynchable(EObject):
    __metaclass__ = MetaEClass
    synched = EAttribute(eType=EBoolean)

    def __init__(self, synched=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(ISynchable, self).__init__()
        if synched is not None:
            self.synched = synched


@abstract
class Node(ISynchable):
    id = EAttribute(eType=EString)
    name = EAttribute(eType=EString)
    tags = EReference(upper=-1)

    def __init__(self, id=None, name=None, tags=None, **kwargs):
        super(Node, self).__init__(**kwargs)
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if tags:
            self.tags.extend(tags)
    def getPath(self):
        raise NotImplementedError('Operation getPath(...) is not yet implemented')


class Tag(ISynchable):
    name = EAttribute(eType=EString)
    tags = EReference(upper=-1, containment=True)

    def __init__(self, tags=None, name=None, **kwargs):
        super(Tag, self).__init__(**kwargs)
        if name is not None:
            self.name = name
        if tags:
            self.tags.extend(tags)


class ExternalDomainModel(DomainModel):
    fileFormat = EAttribute(eType=FileFormat)

    def __init__(self, fileFormat=None, **kwargs):
        super(ExternalDomainModel, self).__init__(**kwargs)
        if fileFormat is not None:
            self.fileFormat = fileFormat


class GeppettoLibrary(Node):
    types = EReference(upper=-1, containment=True)
    sharedTypes = EReference(upper=-1)

    def __init__(self, types=None, sharedTypes=None, **kwargs):
        super(GeppettoLibrary, self).__init__(**kwargs)
        if types:
            self.types.extend(types)
        if sharedTypes:
            self.sharedTypes.extend(sharedTypes)
