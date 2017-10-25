from pyecore.resources import global_registry
from .model import getEClassifier, eClassifiers
from .model import name, nsURI, nsPrefix, eClass
from .model import GeppettoModel, Node, GeppettoLibrary, LibraryManager, ExperimentState, VariableValue, Tag, DomainModel, ModelFormat, ExternalDomainModel, FileFormat, StringToStringMap, ISynchable
from .types import Type, VisualType, CompositeType, PointerType, QuantityType, ParameterType, StateVariableType, DynamicsType, ArgumentType, ExpressionType, HTMLType, TextType, URLType, PointType, ArrayType, CompositeVisualType, ConnectionType, ImageType
from .values import Pointer, Value, VisualValue, Composite, Quantity, Dynamics, Argument, Expression, HTML, Text, URL, Point, ArrayValue, VisualGroup, Image, StringToValueMap, Unit, PointerElement, PhysicalQuantity, Function, FunctionPlot, VisualGroupElement, SkeletonTransformation, ArrayElement, TimeSeries, Cylinder, SkeletonAnimation, Connection
from .variables import Variable, TypeToValueMap
from .datasources import DataSource, Query, DataSourceLibraryConfiguration, QueryMatchingCriteria, AQueryResult, ProcessQuery, CompoundQuery, CompoundRefQuery, QueryResults
from . import model
from . import types
from . import values
from . import variables
from . import datasources

__all__ = ['GeppettoModel', 'Node', 'GeppettoLibrary', 'LibraryManager', 'ExperimentState', 'VariableValue', 'Tag', 'DomainModel', 'ModelFormat', 'ExternalDomainModel', 'FileFormat', 'StringToStringMap', 'ISynchable']

eSubpackages = [types, values, variables, datasources]
eSuperPackage = None
model.eSubpackages = eSubpackages

# Non opposite EReferences
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
Composite.value.eType = StringToValueMap
StringToValueMap.value.eType = Value
PhysicalQuantity.unit.eType = Unit
TimeSeries.unit.eType = Unit
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
SkeletonAnimation.skeletonTransformationSeries.eType = SkeletonTransformation
VisualGroupElement.parameter.eType = Quantity
VisualGroup.visualGroupElements.eType = VisualGroupElement
Connection.a.eType = Pointer
Connection.b.eType = Pointer
ArrayElement.position.eType = Point
ArrayElement.initialValue.eType = Value
ArrayValue.elements.eType = ArrayElement
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

# opposite EReferences
Type.referencedVariables.eType = Variable
Variable.types.eType = Type
Variable.types.eOpposite = Type.referencedVariables


# Manage all other EClassifiers (EEnum, EDatatypes...)
otherClassifiers = [FileFormat]
for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif._container = model

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

# Manually register all the URI and master URI in the global registry
# This registering is performed outside the previous 'for' to ease future
# code merging (in case of new metamodel versions)
geppetto_master_uri = ('https://raw.githubusercontent.com/openworm/'
                       'org.geppetto.model/master/src/main/resources/'
                       'geppettoModel.ecore')

global_registry[nsURI] = model
global_registry[geppetto_master_uri] = model
for subpack in eSubpackages:
    global_registry[subpack.nsURI] = subpack
    global_registry[geppetto_master_uri + '#//' + subpack.name] = subpack
