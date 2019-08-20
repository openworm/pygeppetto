
from .model import getEClassifier, eClassifiers
from .model import name, nsURI, nsPrefix, eClass
from .model import GeppettoModel, Node, GeppettoLibrary, LibraryManager, ExperimentState, VariableValue, Tag, DomainModel, ModelFormat, ExternalDomainModel, FileFormat, StringToStringMap, ISynchable

from model.types import Type
from model.values import Pointer, Value
from model.datasources import Query, DataSource
from model.variables import Variable

from .types import ArrayType, VisualType, DynamicsType, TextType, QuantityType, ExpressionType, SimpleArrayType, PointType, CompositeVisualType, StateVariableType, JSONType, ConnectionType, PointerType, CompositeType, ArgumentType, ImageType, Type, URLType, ParameterType, HTMLType
from .values import MDTimeSeries, Particles, StringToValueMap, Metadata, Quantity, PhysicalQuantity, VisualValue, HTML, Cylinder, Value, ArrayValue, SkeletonTransformation, Point, Composite, GenericArray, Function, TimeSeries, URL, PointerElement, Expression, Dynamics, SkeletonAnimation, JSON, FunctionPlot, Text, ArrayElement, AArrayValue, Pointer, VisualGroupElement, Argument, Image, Connection, Unit, VisualGroup
from .variables import TypeToValueMap, Variable
from .datasources import QueryMatchingCriteria, DataSourceLibraryConfiguration, ProcessQuery, CompoundQuery, Query, DataSource, AQueryResult, QueryResults, CompoundRefQuery
from . import model
from . import types

from . import values

from . import variables

from . import datasources


__all__ = ['GeppettoModel', 'Node', 'GeppettoLibrary', 'LibraryManager', 'ExperimentState', 'VariableValue',
           'Tag', 'DomainModel', 'ModelFormat', 'ExternalDomainModel', 'FileFormat', 'StringToStringMap', 'ISynchable']

eSubpackages = [types, values, variables, datasources]
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
GeppettoModel.variables.eType = Variable
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
