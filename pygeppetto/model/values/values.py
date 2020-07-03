"""Definition of meta model 'values'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from pygeppetto.model import Node, ISynchable
from pyecore.type import Int, String, Double, IntObject


name = 'values'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/master/src/main/resources/geppettoModel.ecore#//values'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
Connectivity = EEnum('Connectivity', literals=['DIRECTIONAL', 'BIDIRECTIONAL', 'NON_DIRECTIONAL'])

ImageFormat = EEnum('ImageFormat', literals=[
                    'PNG', 'JPEG', 'IIP', 'DCM', 'NIFTI', 'TIFF', 'DZI', 'GOOGLE_MAP'])


class StringToValueMap(EObject, metaclass=MetaEClass):

    key = EAttribute(eType=String, derived=False, changeable=True)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if key is not None:
            self.key = key

        if value is not None:
            self.value = value


class PointerElement(EObject, metaclass=MetaEClass):

    index = EAttribute(eType=IntObject, derived=False, changeable=True, default_value=-1)
    variable = EReference(ordered=True, unique=True, containment=False)
    type = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, variable=None, type=None, index=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if index is not None:
            self.index = index

        if variable is not None:
            self.variable = variable

        if type is not None:
            self.type = type


class FunctionPlot(EObject, metaclass=MetaEClass):

    title = EAttribute(eType=String, derived=False, changeable=True)
    xAxisLabel = EAttribute(eType=String, derived=False, changeable=True)
    yAxisLabel = EAttribute(eType=String, derived=False, changeable=True)
    initialValue = EAttribute(eType=Double, derived=False, changeable=True)
    finalValue = EAttribute(eType=Double, derived=False, changeable=True)
    stepValue = EAttribute(eType=Double, derived=False, changeable=True)

    def __init__(self, title=None, xAxisLabel=None, yAxisLabel=None, initialValue=None, finalValue=None, stepValue=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if title is not None:
            self.title = title

        if xAxisLabel is not None:
            self.xAxisLabel = xAxisLabel

        if yAxisLabel is not None:
            self.yAxisLabel = yAxisLabel

        if initialValue is not None:
            self.initialValue = initialValue

        if finalValue is not None:
            self.finalValue = finalValue

        if stepValue is not None:
            self.stepValue = stepValue


class SkeletonTransformation(EObject, metaclass=MetaEClass):

    skeletonTransformation = EAttribute(eType=Double, derived=False, changeable=True, upper=-1)

    def __init__(self, skeletonTransformation=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if skeletonTransformation:
            self.skeletonTransformation.extend(skeletonTransformation)


@abstract
class Value(ISynchable):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Composite(Value):

    value = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, value=None, **kwargs):

        super().__init__(**kwargs)

        if value:
            self.value.extend(value)


class Quantity(Value):

    scalingFactor = EAttribute(eType=Int, derived=False, changeable=True)
    value = EAttribute(eType=Double, derived=False, changeable=True)

    def __init__(self, scalingFactor=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if scalingFactor is not None:
            self.scalingFactor = scalingFactor

        if value is not None:
            self.value = value


class Unit(Value):

    unit = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, unit=None, **kwargs):

        super().__init__(**kwargs)

        if unit is not None:
            self.unit = unit


class TimeSeries(Value):

    scalingFactor = EAttribute(eType=Int, derived=False, changeable=True)
    value = EAttribute(eType=Double, derived=False, changeable=True, upper=-1)
    unit = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, unit=None, scalingFactor=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if scalingFactor is not None:
            self.scalingFactor = scalingFactor

        if value:
            self.value.extend(value)

        if unit is not None:
            self.unit = unit


class MDTimeSeries(Value):

    value = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, value=None, **kwargs):

        super().__init__(**kwargs)

        if value:
            self.value.extend(value)


@abstract
class MetadataValue(Value):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Pointer(Value):

    path = EAttribute(eType=String, derived=False, changeable=True)
    elements = EReference(ordered=True, unique=True, containment=True, upper=-1)
    point = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, elements=None, point=None, path=None, **kwargs):

        super().__init__(**kwargs)

        if path is not None:
            self.path = path

        if elements:
            self.elements.extend(elements)

        if point is not None:
            self.point = point

    def getInstancePath(self):

        raise NotImplementedError('operation getInstancePath(...) not yet implemented')


class Point(Value):

    x = EAttribute(eType=Double, derived=False, changeable=True)
    y = EAttribute(eType=Double, derived=False, changeable=True)
    z = EAttribute(eType=Double, derived=False, changeable=True)

    def __init__(self, x=None, y=None, z=None, **kwargs):

        super().__init__(**kwargs)

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if z is not None:
            self.z = z


class Dynamics(Value):

    initialCondition = EReference(ordered=True, unique=True, containment=True)
    dynamics = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, initialCondition=None, dynamics=None, **kwargs):

        super().__init__(**kwargs)

        if initialCondition is not None:
            self.initialCondition = initialCondition

        if dynamics is not None:
            self.dynamics = dynamics


class Function(Value):

    arguments = EReference(ordered=True, unique=True, containment=True, upper=-1)
    expression = EReference(ordered=True, unique=True, containment=True)
    functionPlot = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, arguments=None, expression=None, functionPlot=None, **kwargs):

        super().__init__(**kwargs)

        if arguments:
            self.arguments.extend(arguments)

        if expression is not None:
            self.expression = expression

        if functionPlot is not None:
            self.functionPlot = functionPlot


class Argument(Value):

    argument = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, argument=None, **kwargs):

        super().__init__(**kwargs)

        if argument is not None:
            self.argument = argument


class Expression(Value):

    expression = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, expression=None, **kwargs):

        super().__init__(**kwargs)

        if expression is not None:
            self.expression = expression


@abstract
class VisualValue(Value):

    groupElements = EReference(ordered=True, unique=True, containment=False, upper=-1)
    position = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, groupElements=None, position=None, **kwargs):

        super().__init__(**kwargs)

        if groupElements:
            self.groupElements.extend(groupElements)

        if position is not None:
            self.position = position


class Particles(Value):

    particles = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, particles=None, **kwargs):

        super().__init__(**kwargs)

        if particles:
            self.particles.extend(particles)


class VisualGroupElement(Node):

    defaultColor = EAttribute(eType=String, derived=False, changeable=True)
    parameter = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, defaultColor=None, parameter=None, **kwargs):

        super().__init__(**kwargs)

        if defaultColor is not None:
            self.defaultColor = defaultColor

        if parameter is not None:
            self.parameter = parameter


class VisualGroup(Node):

    lowSpectrumColor = EAttribute(eType=String, derived=False, changeable=True)
    highSpectrumColor = EAttribute(eType=String, derived=False, changeable=True)
    type = EAttribute(eType=String, derived=False, changeable=True)
    visualGroupElements = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, lowSpectrumColor=None, highSpectrumColor=None, type=None, visualGroupElements=None, **kwargs):

        super().__init__(**kwargs)

        if lowSpectrumColor is not None:
            self.lowSpectrumColor = lowSpectrumColor

        if highSpectrumColor is not None:
            self.highSpectrumColor = highSpectrumColor

        if type is not None:
            self.type = type

        if visualGroupElements:
            self.visualGroupElements.extend(visualGroupElements)


class Connection(Value):

    connectivity = EAttribute(eType=Connectivity, derived=False, changeable=True)
    a = EReference(ordered=True, unique=True, containment=True)
    b = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, a=None, b=None, connectivity=None, **kwargs):

        super().__init__(**kwargs)

        if connectivity is not None:
            self.connectivity = connectivity

        if a is not None:
            self.a = a

        if b is not None:
            self.b = b


class ArrayElement(Value):

    index = EAttribute(eType=Int, derived=False, changeable=True)
    position = EReference(ordered=True, unique=True, containment=True)
    initialValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, index=None, position=None, initialValue=None, **kwargs):

        super().__init__(**kwargs)

        if index is not None:
            self.index = index

        if position is not None:
            self.position = position

        if initialValue is not None:
            self.initialValue = initialValue


class ArrayValue(Value):

    elements = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, elements=None, **kwargs):

        super().__init__(**kwargs)

        if elements:
            self.elements.extend(elements)


class Image(Value):

    data = EAttribute(eType=String, derived=False, changeable=True)
    name = EAttribute(eType=String, derived=False, changeable=True)
    reference = EAttribute(eType=String, derived=False, changeable=True)
    format = EAttribute(eType=ImageFormat, derived=False, changeable=True)

    def __init__(self, data=None, name=None, reference=None, format=None, **kwargs):

        super().__init__(**kwargs)

        if data is not None:
            self.data = data

        if name is not None:
            self.name = name

        if reference is not None:
            self.reference = reference

        if format is not None:
            self.format = format


class ImportValue(Value):

    modelInterpreterId = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, modelInterpreterId=None, **kwargs):

        super().__init__(**kwargs)

        if modelInterpreterId is not None:
            self.modelInterpreterId = modelInterpreterId


@abstract
class AArrayValue(Value):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class PhysicalQuantity(Quantity):

    unit = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, unit=None, **kwargs):

        super().__init__(**kwargs)

        if unit is not None:
            self.unit = unit


class Text(MetadataValue):

    text = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, text=None, **kwargs):

        super().__init__(**kwargs)

        if text is not None:
            self.text = text


class URL(MetadataValue):

    url = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, url=None, **kwargs):

        super().__init__(**kwargs)

        if url is not None:
            self.url = url


class HTML(MetadataValue):

    html = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, html=None, **kwargs):

        super().__init__(**kwargs)

        if html is not None:
            self.html = html


class Collada(VisualValue):

    collada = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, collada=None, **kwargs):

        super().__init__(**kwargs)

        if collada is not None:
            self.collada = collada


class OBJ(VisualValue):

    obj = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, obj=None, **kwargs):

        super().__init__(**kwargs)

        if obj is not None:
            self.obj = obj


class Sphere(VisualValue):

    radius = EAttribute(eType=Double, derived=False, changeable=True)

    def __init__(self, radius=None, **kwargs):

        super().__init__(**kwargs)

        if radius is not None:
            self.radius = radius


class Cylinder(VisualValue):

    bottomRadius = EAttribute(eType=Double, derived=False, changeable=True)
    topRadius = EAttribute(eType=Double, derived=False, changeable=True)
    height = EAttribute(eType=Double, derived=False, changeable=True)
    distal = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, bottomRadius=None, topRadius=None, height=None, distal=None, **kwargs):

        super().__init__(**kwargs)

        if bottomRadius is not None:
            self.bottomRadius = bottomRadius

        if topRadius is not None:
            self.topRadius = topRadius

        if height is not None:
            self.height = height

        if distal is not None:
            self.distal = distal


class SkeletonAnimation(VisualValue):

    skeletonTransformationSeries = EReference(
        ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, skeletonTransformationSeries=None, **kwargs):

        super().__init__(**kwargs)

        if skeletonTransformationSeries:
            self.skeletonTransformationSeries.extend(skeletonTransformationSeries)


class Metadata(MetadataValue):

    value = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, value=None, **kwargs):

        super().__init__(**kwargs)

        if value:
            self.value.extend(value)


class JSON(MetadataValue):

    json = EAttribute(eType=String, derived=False, changeable=True)

    def __init__(self, json=None, **kwargs):

        super().__init__(**kwargs)

        if json is not None:
            self.json = json


class GenericArray(AArrayValue):

    elements = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, elements=None, **kwargs):

        super().__init__(**kwargs)

        if elements:
            self.elements.extend(elements)


class StringArray(AArrayValue):

    elements = EAttribute(eType=String, derived=False, changeable=True, upper=-1)

    def __init__(self, elements=None, **kwargs):

        super().__init__(**kwargs)

        if elements:
            self.elements.extend(elements)


class IntArray(AArrayValue):

    elements = EAttribute(eType=Int, derived=False, changeable=True, upper=-1)

    def __init__(self, elements=None, **kwargs):

        super().__init__(**kwargs)

        if elements:
            self.elements.extend(elements)


class DoubleArray(AArrayValue):

    elements = EAttribute(eType=Double, derived=False, changeable=True, upper=-1)

    def __init__(self, elements=None, **kwargs):

        super().__init__(**kwargs)

        if elements:
            self.elements.extend(elements)
