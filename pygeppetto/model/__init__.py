from pyecore.resources import global_registry
from .model import getEClassifier, eClassifiers
from .model import name, nsURI, nsPrefix, eClass
from .model import GeppettoModel, Node, GeppettoLibrary, LibraryManager, ExperimentState, VariableValue, Tag, DomainModel, ModelFormat, ExternalDomainModel, FileFormat, StringToStringMap, ISynchable, World

from .instances import Instance
from .variables import Variable
from .datasources import DataSource, Query
from .types import Type
from .values import Value, Pointer

from .types import PointType, QuantityType, CompositeType, ConnectionType, ArgumentType, URLType, PointerType, TextType, DynamicsType, SimpleArrayType, ImageType, JSONType, Type, VisualType, StateVariableType, HTMLType, CompositeVisualType, ParameterType, ArrayType, ExpressionType
from .values import VisualValue, ArrayElement, Unit, VisualGroupElement, Pointer, AArrayValue, FunctionPlot, Expression, Argument, GenericArray, VisualGroup, Point, PhysicalQuantity, PointerElement, JSON, HTML, SkeletonTransformation, Image, Function, Text, Cylinder, URL, TimeSeries, StringToValueMap, Value, ArrayValue, Metadata, Particles, SkeletonAnimation, Connection, Composite, MDTimeSeries, Quantity, Dynamics
from .variables import Variable, TypeToValueMap
from .datasources import CompoundQuery, AQueryResult, QueryResults, Query, ProcessQuery, CompoundRefQuery, DataSource, DataSourceLibraryConfiguration, QueryMatchingCriteria
from .instances import SimpleConnectionInstance, Instance, SimpleInstance
from . import model
from . import types

from . import values

from . import variables

from . import datasources

from . import instances


__all__ = ['GeppettoModel', 'Node', 'GeppettoLibrary', 'LibraryManager', 'ExperimentState', 'VariableValue', 'Tag',
           'DomainModel', 'ModelFormat', 'ExternalDomainModel', 'FileFormat', 'StringToStringMap', 'ISynchable', 'World']

eSubpackages = [types, values, variables, datasources, instances]
eSuperPackage = None
model.eSubpackages = eSubpackages
model.eSuperPackage = eSuperPackage

Type.superType.eType = Type
Type.visualType.eType = VisualType
Type.domainModel.eType = DomainModel
VisualType.defaultValue.eType = VisualValue
CompositeType.variables.eType = Variable
CompositeType.defaultValue.eType = Composite
PointerType.defaultValue.eType = Pointer
QuantityType.defaultValue.eType = Quantity
ParameterType.defaultValue.eType = Quantity
StateVariableType.defaultValue.eType = Quantity
DynamicsType.defaultValue.eType = Dynamics
ArgumentType.defaultValue.eType = Argument
ExpressionType.defaultValue.eType = Expression
HTMLType.defaultValue.eType = HTML
JSONType.defaultValue.eType = JSON
TextType.defaultValue.eType = Text
URLType.defaultValue.eType = URL
PointType.defaultValue.eType = Point
ArrayType.arrayType.eType = Type
ArrayType.defaultValue.eType = ArrayValue
CompositeVisualType.variables.eType = Variable
CompositeVisualType.visualGroups.eType = VisualGroup
ConnectionType.variables.eType = Variable
ConnectionType.defaultValue.eType = Composite
ImageType.defaultValue.eType = Image
SimpleArrayType.defaultValue.eType = AArrayValue
Composite.value.eType = StringToValueMap
StringToValueMap.value.eType = Value
PhysicalQuantity.unit.eType = Unit
TimeSeries.unit.eType = Unit
MDTimeSeries.value.eType = Value
Pointer.elements.eType = PointerElement
Pointer.point.eType = Point
PointerElement.variable.eType = Variable
PointerElement.type.eType = Type
Dynamics.initialCondition.eType = PhysicalQuantity
Dynamics.dynamics.eType = Function
Function.arguments.eType = Argument
Function.expression.eType = Expression
Function.functionPlot.eType = FunctionPlot
VisualValue.groupElements.eType = VisualGroupElement
VisualValue.position.eType = Point
Cylinder.distal.eType = Point
Particles.particles.eType = Point
SkeletonAnimation.skeletonTransformationSeries.eType = SkeletonTransformation
VisualGroupElement.parameter.eType = Quantity
VisualGroup.visualGroupElements.eType = VisualGroupElement
Connection.a.eType = Pointer
Connection.b.eType = Pointer
ArrayElement.position.eType = Point
ArrayElement.initialValue.eType = Value
ArrayValue.elements.eType = ArrayElement
Metadata.value.eType = StringToValueMap
GenericArray.elements.eType = Value
Variable.anonymousTypes.eType = Type
Variable.initialValues.eType = TypeToValueMap
Variable.position.eType = Point
TypeToValueMap.key.eType = Type
TypeToValueMap.value.eType = Value
DataSource.libraryConfigurations.eType = DataSourceLibraryConfiguration
DataSource.queries.eType = Query
DataSource.dependenciesLibrary.eType = GeppettoLibrary
DataSource.targetLibrary.eType = GeppettoLibrary
DataSource.fetchVariableQuery.eType = Query
DataSourceLibraryConfiguration.library.eType = GeppettoLibrary
Query.matchingCriteria.eType = QueryMatchingCriteria
Query.returnType.eType = Type
ProcessQuery.parameters.eType = StringToStringMap
CompoundQuery.queryChain.eType = Query
CompoundRefQuery.queryChain.eType = Query
QueryResults.results.eType = AQueryResult
QueryMatchingCriteria.type.eType = Type
Instance.type.eType = Type
Instance.value.eType = Value
SimpleInstance.visualValue.eType = VisualValue
SimpleInstance.position.eType = Point
SimpleConnectionInstance.a.eType = Instance
SimpleConnectionInstance.b.eType = Instance
GeppettoModel.variables.eType = Variable
GeppettoModel.worlds.eType = World
GeppettoModel.libraries.eType = GeppettoLibrary
GeppettoModel.tags.eType = Tag
GeppettoModel.dataSources.eType = DataSource
GeppettoModel.queries.eType = Query
Node.tags.eType = Tag
GeppettoLibrary.types.eType = Type
GeppettoLibrary.sharedTypes.eType = Type
LibraryManager.libraries.eType = GeppettoLibrary
ExperimentState.recordedVariables.eType = VariableValue
ExperimentState.setParameters.eType = VariableValue
VariableValue.pointer.eType = Pointer
VariableValue.value.eType = Value
Tag.tags.eType = Tag
DomainModel.format.eType = ModelFormat
World.variables.eType = Variable
World.instances.eType = Instance
Type.referencedVariables.eType = Variable
Variable.types.eType = Type
Variable.types.eOpposite = Type.referencedVariables

otherClassifiers = [FileFormat]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [model] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
