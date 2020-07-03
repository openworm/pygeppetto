"""Definition of meta model 'model'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from pyecore.type import String, Boolean, Long


name = 'model'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/master/src/main/resources/geppettoModel.ecore'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
FileFormat = EEnum('FileFormat', literals=['ZIP', 'HDF5'])


class GeppettoModel(EObject, metaclass=MetaEClass):
    """The root of every Geppetto model. This is the configuration of the Geppetto Model, to not be confused with the model Instantiation."""
    id = EAttribute(eType=String, derived=False, changeable=True)
    name = EAttribute(eType=String, derived=False, changeable=True)
    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    worlds = EReference(ordered=True, unique=True, containment=True, upper=-1)
    libraries = EReference(ordered=True, unique=True, containment=True, upper=-1)
    tags = EReference(ordered=True, unique=True, containment=True, upper=-1)
    dataSources = EReference(ordered=True, unique=True, containment=True, upper=-1)
    queries = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, variables=None, worlds=None, libraries=None, tags=None, id=None, name=None, dataSources=None, queries=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if name is not None:
            self.name = name

        if variables:
            self.variables.extend(variables)

        if worlds:
            self.worlds.extend(worlds)

        if libraries:
            self.libraries.extend(libraries)

        if tags:
            self.tags.extend(tags)

        if dataSources:
            self.dataSources.extend(dataSources)

        if queries:
            self.queries.extend(queries)


class LibraryManager(EObject, metaclass=MetaEClass):

    libraries = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, libraries=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if libraries:
            self.libraries.extend(libraries)


class ExperimentState(EObject, metaclass=MetaEClass):

    experimentId = EAttribute(eType=Long, derived=False, changeable=True)
    projectId = EAttribute(eType=Long, derived=False, changeable=True)
    recordedVariables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    setParameters = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, recordedVariables=None, setParameters=None, experimentId=None, projectId=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if experimentId is not None:
            self.experimentId = experimentId

        if projectId is not None:
            self.projectId = projectId

        if recordedVariables:
            self.recordedVariables.extend(recordedVariables)

        if setParameters:
            self.setParameters.extend(setParameters)


class VariableValue(EObject, metaclass=MetaEClass):

    pointer = EReference(ordered=True, unique=True, containment=True)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, pointer=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if pointer is not None:
            self.pointer = pointer

        if value is not None:
            self.value = value


class DomainModel(EObject, metaclass=MetaEClass):

    domainModel = EAttribute(eType=EJavaObject, derived=False, changeable=True)
    format = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, domainModel=None, format=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if domainModel is not None:
            self.domainModel = domainModel

        if format is not None:
            self.format = format


class ModelFormat(EObject, metaclass=MetaEClass):

    modelFormat = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, modelFormat=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if modelFormat is not None:
            self.modelFormat = modelFormat


class StringToStringMap(EObject, metaclass=MetaEClass):

    key = EAttribute(eType=String, derived=False, changeable=True)
    value = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if key is not None:
            self.key = key

        if value is not None:
            self.value = value


@abstract
class ISynchable(EObject, metaclass=MetaEClass):

    synched = EAttribute(eType=Boolean, derived=False, changeable=True)

    def __init__(self, synched=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if synched is not None:
            self.synched = synched


@abstract
class Node(ISynchable):

    id = EAttribute(eType=String, derived=False, changeable=True)
    name = EAttribute(eType=String, derived=False, changeable=True)
    tags = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, id=None, name=None, tags=None, **kwargs):

        super().__init__(**kwargs)

        if id is not None:
            self.id = id

        if name is not None:
            self.name = name

        if tags:
            self.tags.extend(tags)

    def getPath(self):

        raise NotImplementedError('operation getPath(...) not yet implemented')


class Tag(ISynchable):

    name = EAttribute(eType=String, derived=False, changeable=True)
    tags = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, tags=None, name=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if tags:
            self.tags.extend(tags)


class ExternalDomainModel(DomainModel):

    fileFormat = EAttribute(eType=FileFormat, derived=False,
                            changeable=True, default_value=FileFormat.ZIP)

    def __init__(self, fileFormat=None, **kwargs):

        super().__init__(**kwargs)

        if fileFormat is not None:
            self.fileFormat = fileFormat


class GeppettoLibrary(Node):

    types = EReference(ordered=True, unique=True, containment=True, upper=-1)
    sharedTypes = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, types=None, sharedTypes=None, **kwargs):

        super().__init__(**kwargs)

        if types:
            self.types.extend(types)

        if sharedTypes:
            self.sharedTypes.extend(sharedTypes)

    def getTypeById(self):

        raise NotImplementedError('operation getTypeById(...) not yet implemented')


class World(Node):

    variables = EReference(ordered=True, unique=True, containment=True, upper=-1)
    instances = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, variables=None, instances=None, **kwargs):

        super().__init__(**kwargs)

        if variables:
            self.variables.extend(variables)

        if instances:
            self.instances.extend(instances)
