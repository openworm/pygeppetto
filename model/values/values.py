from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *
from model import ISynchable
from model import Node

name = 'values'
nsURI = 'https://raw.githubusercontent.com/openworm/org.geppetto.model/development/src/main/resources/geppettoModel.ecore#//values'
nsPrefix = 'gep'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


Connectivity = EEnum('Connectivity', literals=['DIRECTIONAL', 'BIDIRECTIONAL', 'NON_DIRECTIONAL'])  # noqa
ImageFormat = EEnum('ImageFormat', literals=['PNG', 'JPEG', 'IIP'])  # noqa


class StringToValueMap(EObject):
    __metaclass__ = MetaEClass
    key = EAttribute(eType=EString)
    value = EReference()

    def __init__(self, key=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(StringToValueMap, self).__init__()
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value


class PointerElement(EObject):
    __metaclass__ = MetaEClass
    index = EAttribute(eType=EInteger)
    variable = EReference()
    type = EReference()

    def __init__(self, variable=None, type=None, index=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(PointerElement, self).__init__()
        if index is not None:
            self.index = index
        if variable is not None:
            self.variable = variable
        if type is not None:
            self.type = type


class FunctionPlot(EObject):
    __metaclass__ = MetaEClass
    title = EAttribute(eType=EString)
    xAxisLabel = EAttribute(eType=EString)
    yAxisLabel = EAttribute(eType=EString)
    initialValue = EAttribute(eType=EDouble)
    finalValue = EAttribute(eType=EDouble)
    stepValue = EAttribute(eType=EDouble)

    def __init__(self, title=None, xAxisLabel=None, yAxisLabel=None, initialValue=None, finalValue=None, stepValue=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(FunctionPlot, self).__init__()
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


class SkeletonTransformation(EObject):
    __metaclass__ = MetaEClass
    skeletonTransformation = EAttribute(eType=EDouble, upper=-1)

    def __init__(self, skeletonTransformation=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super(SkeletonTransformation, self).__init__()
        if skeletonTransformation:
            self.skeletonTransformation.extend(skeletonTransformation)


@abstract
class Value(ISynchable):

    def __init__(self, **kwargs):
        super(Value, self).__init__(**kwargs)


class Composite(Value):
    value = EReference(upper=-1, containment=True)

    def __init__(self, value=None, **kwargs):
        super(Composite, self).__init__(**kwargs)
        if value:
            self.value.extend(value)


class Quantity(Value):
    scalingFactor = EAttribute(eType=EInt)
    value = EAttribute(eType=EDouble)

    def __init__(self, scalingFactor=None, value=None, **kwargs):
        super(Quantity, self).__init__(**kwargs)
        if scalingFactor is not None:
            self.scalingFactor = scalingFactor
        if value is not None:
            self.value = value


class Unit(Value):
    unit = EAttribute(eType=EString)

    def __init__(self, unit=None, **kwargs):
        super(Unit, self).__init__(**kwargs)
        if unit is not None:
            self.unit = unit


class TimeSeries(Value):
    scalingFactor = EAttribute(eType=EInt)
    value = EAttribute(eType=EDouble, upper=-1)
    unit = EReference(containment=True)

    def __init__(self, unit=None, scalingFactor=None, value=None, **kwargs):
        super(TimeSeries, self).__init__(**kwargs)
        if scalingFactor is not None:
            self.scalingFactor = scalingFactor
        if value:
            self.value.extend(value)
        if unit is not None:
            self.unit = unit


@abstract
class MetadataValue(Value):

    def __init__(self, **kwargs):
        super(MetadataValue, self).__init__(**kwargs)


class Pointer(Value):
    path = EAttribute(eType=EString)
    elements = EReference(upper=-1, containment=True)
    point = EReference(containment=True)

    def __init__(self, elements=None, point=None, path=None, **kwargs):
        super(Pointer, self).__init__(**kwargs)
        if path is not None:
            self.path = path
        if elements:
            self.elements.extend(elements)
        if point is not None:
            self.point = point
    def getInstancePath(self):
        raise NotImplementedError('Operation getInstancePath(...) is not yet implemented')


class Point(Value):
    x = EAttribute(eType=EDouble)
    y = EAttribute(eType=EDouble)
    z = EAttribute(eType=EDouble)

    def __init__(self, x=None, y=None, z=None, **kwargs):
        super(Point, self).__init__(**kwargs)
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z


class Dynamics(Value):
    initialCondition = EReference(containment=True)
    dynamics = EReference(containment=True)

    def __init__(self, initialCondition=None, dynamics=None, **kwargs):
        super(Dynamics, self).__init__(**kwargs)
        if initialCondition is not None:
            self.initialCondition = initialCondition
        if dynamics is not None:
            self.dynamics = dynamics


class Function(Value):
    arguments = EReference(upper=-1, containment=True)
    expression = EReference(containment=True)
    functionPlot = EReference(containment=True)

    def __init__(self, arguments=None, expression=None, functionPlot=None, **kwargs):
        super(Function, self).__init__(**kwargs)
        if arguments:
            self.arguments.extend(arguments)
        if expression is not None:
            self.expression = expression
        if functionPlot is not None:
            self.functionPlot = functionPlot


class Argument(Value):
    argument = EAttribute(eType=EString)

    def __init__(self, argument=None, **kwargs):
        super(Argument, self).__init__(**kwargs)
        if argument is not None:
            self.argument = argument


class Expression(Value):
    expression = EAttribute(eType=EString)

    def __init__(self, expression=None, **kwargs):
        super(Expression, self).__init__(**kwargs)
        if expression is not None:
            self.expression = expression


@abstract
class VisualValue(Value):
    groupElements = EReference(upper=-1)
    position = EReference(containment=True)

    def __init__(self, groupElements=None, position=None, **kwargs):
        super(VisualValue, self).__init__(**kwargs)
        if groupElements:
            self.groupElements.extend(groupElements)
        if position is not None:
            self.position = position


class VisualGroupElement(Node):
    defaultColor = EAttribute(eType=EString)
    parameter = EReference(containment=True)

    def __init__(self, defaultColor=None, parameter=None, **kwargs):
        super(VisualGroupElement, self).__init__(**kwargs)
        if defaultColor is not None:
            self.defaultColor = defaultColor
        if parameter is not None:
            self.parameter = parameter


class VisualGroup(Node):
    lowSpectrumColor = EAttribute(eType=EString)
    highSpectrumColor = EAttribute(eType=EString)
    type = EAttribute(eType=EString)
    visualGroupElements = EReference(upper=-1, containment=True)

    def __init__(self, lowSpectrumColor=None, highSpectrumColor=None, type=None, visualGroupElements=None, **kwargs):
        super(VisualGroup, self).__init__(**kwargs)
        if lowSpectrumColor is not None:
            self.lowSpectrumColor = lowSpectrumColor
        if highSpectrumColor is not None:
            self.highSpectrumColor = highSpectrumColor
        if type is not None:
            self.type = type
        if visualGroupElements:
            self.visualGroupElements.extend(visualGroupElements)


class Connection(Value):
    connectivity = EAttribute(eType=Connectivity)
    a = EReference(containment=True)
    b = EReference(containment=True)

    def __init__(self, a=None, b=None, connectivity=None, **kwargs):
        super(Connection, self).__init__(**kwargs)
        if connectivity is not None:
            self.connectivity = connectivity
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b


class ArrayElement(Value):
    index = EAttribute(eType=EInt)
    position = EReference(containment=True)
    initialValue = EReference(containment=True)

    def __init__(self, index=None, position=None, initialValue=None, **kwargs):
        super(ArrayElement, self).__init__(**kwargs)
        if index is not None:
            self.index = index
        if position is not None:
            self.position = position
        if initialValue is not None:
            self.initialValue = initialValue


class ArrayValue(Value):
    elements = EReference(upper=-1, containment=True)

    def __init__(self, elements=None, **kwargs):
        super(ArrayValue, self).__init__(**kwargs)
        if elements:
            self.elements.extend(elements)


class Image(Value):
    data = EAttribute(eType=EString)
    name = EAttribute(eType=EString)
    reference = EAttribute(eType=EString)
    format = EAttribute(eType=ImageFormat)

    def __init__(self, data=None, name=None, reference=None, format=None, **kwargs):
        super(Image, self).__init__(**kwargs)
        if data is not None:
            self.data = data
        if name is not None:
            self.name = name
        if reference is not None:
            self.reference = reference
        if format is not None:
            self.format = format


class ImportValue(Value):
    modelInterpreterId = EAttribute(eType=EString)

    def __init__(self, modelInterpreterId=None, **kwargs):
        super(ImportValue, self).__init__(**kwargs)
        if modelInterpreterId is not None:
            self.modelInterpreterId = modelInterpreterId


class PhysicalQuantity(Quantity):
    unit = EReference(containment=True)

    def __init__(self, unit=None, **kwargs):
        super(PhysicalQuantity, self).__init__(**kwargs)
        if unit is not None:
            self.unit = unit


class Text(MetadataValue):
    text = EAttribute(eType=EString)

    def __init__(self, text=None, **kwargs):
        super(Text, self).__init__(**kwargs)
        if text is not None:
            self.text = text


class URL(MetadataValue):
    url = EAttribute(eType=EString)

    def __init__(self, url=None, **kwargs):
        super(URL, self).__init__(**kwargs)
        if url is not None:
            self.url = url


class HTML(MetadataValue):
    html = EAttribute(eType=EString)

    def __init__(self, html=None, **kwargs):
        super(HTML, self).__init__(**kwargs)
        if html is not None:
            self.html = html


class Collada(VisualValue):
    collada = EAttribute(eType=EString)

    def __init__(self, collada=None, **kwargs):
        super(Collada, self).__init__(**kwargs)
        if collada is not None:
            self.collada = collada


class OBJ(VisualValue):
    obj = EAttribute(eType=EString)

    def __init__(self, obj=None, **kwargs):
        super(OBJ, self).__init__(**kwargs)
        if obj is not None:
            self.obj = obj


class Sphere(VisualValue):
    radius = EAttribute(eType=EDouble)

    def __init__(self, radius=None, **kwargs):
        super(Sphere, self).__init__(**kwargs)
        if radius is not None:
            self.radius = radius


class Cylinder(VisualValue):
    bottomRadius = EAttribute(eType=EDouble)
    topRadius = EAttribute(eType=EDouble)
    height = EAttribute(eType=EDouble)
    distal = EReference(containment=True)

    def __init__(self, bottomRadius=None, topRadius=None, height=None, distal=None, **kwargs):
        super(Cylinder, self).__init__(**kwargs)
        if bottomRadius is not None:
            self.bottomRadius = bottomRadius
        if topRadius is not None:
            self.topRadius = topRadius
        if height is not None:
            self.height = height
        if distal is not None:
            self.distal = distal


class SkeletonAnimation(VisualValue):
    skeletonTransformationSeries = EReference(upper=-1)

    def __init__(self, skeletonTransformationSeries=None, **kwargs):
        super(SkeletonAnimation, self).__init__(**kwargs)
        if skeletonTransformationSeries:
            self.skeletonTransformationSeries.extend(skeletonTransformationSeries)


class Particle(VisualValue, Point):

    def __init__(self, **kwargs):
        super(Particle, self).__init__(**kwargs)
