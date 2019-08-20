import json
import os.path

from pyecore.resources import ResourceSet, URI
from pygeppetto.model import MDTimeSeries, Value, VisualValue
from pygeppetto.utils import clone

from .model import GeppettoModel
from .values import Cylinder, Sphere, Point, PhysicalQuantity, TimeSeries, Unit, ImportValue, Text, JSON, \
    ArrayValue, HTML, URL, Expression, Dynamics, Image, Connection, Particles, Pointer, Metadata
from .variables import Variable, TypeToValueMap



class GeppettoCommonLibrary:
    TYPE_PARAMETER = 0
    TYPE_DYNAMICS = 1
    TYPE_STATE_VARIABLE = 2

    TYPE_HTML = 3
    TYPE_URL = 4
    TYPE_TEXT = 5
    TYPE_POINT = 6
    TYPE_EXPRESSION = 7
    TYPE_VISUAL = 8
    TYPE_POINTER = 9
    TYPE_IMAGE = 10
    TYPE_CONNECTION = 11
    TYPE_PARTICLES = 12
    TYPE_JSON = 13
    TYPE_SIMPLE_ARRAY = 14
    TYPE_METADATA = 15
    rset = ResourceSet()
    # Build the model URI
    model_uri = URI(os.path.join(os.path.dirname(__file__), '..',
                                 'ecore', 'GeppettoCommonLibrary.xmi'))
    resource = rset.get_resource(model_uri)  # We load the model
    instance = resource.contents[0]

    @classmethod
    def instance_copy(cls):
        return clone(cls.instance)


class GeppettoModelFactory:

    def __init__(self, geppetto_model):
        self.geppetto_model = geppetto_model

    @property
    def geppetto_common_library(self):
        return next(lib for lib in self.geppetto_model.libraries if lib.id == 'common')

    @classmethod
    def createGeppettoModel(cls, name):
        # We create a GeppettoModel instance and we add the common library to it

        geppetto_model = GeppettoModel(name=name, libraries=[clone(GeppettoCommonLibrary.instance)])
        return geppetto_model

    def create_variable(self, id, cl_type, raw_initial_value):
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[cl_type])
        variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[cl_type], raw_initial_value))
        return variable


    def createCylinder(self, id, bottomRadius=1.0, topRadius=1.0,
                       position=None, distal=None):
        position = position or Point()
        distal = distal or Point()
        cylinder = Cylinder(bottomRadius=bottomRadius, topRadius=topRadius)
        cylinder.distal = distal
        cylinder.position = position

        return self.create_variable(id, GeppettoCommonLibrary.TYPE_VISUAL, cylinder)

    def createSphere(self, id, radius=1.0, position=None):
        position = position or Point()
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[GeppettoCommonLibrary.TYPE_VISUAL])
        sphere = Sphere(radius=radius, position=position)
        variable.initialValues.append(
            TypeToValueMap(self.geppetto_common_library.types[GeppettoCommonLibrary.TYPE_VISUAL], sphere))
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_VISUAL, sphere)

    # TODO remove -- Deprecated
    @classmethod
    def createTimeSeries(cls, id, values, unit=None):
        if unit:
            unit = Unit(unit)
        ts = TimeSeries(value=values, unit=unit)
        return ts

    # TODO remove -- Deprecated
    @classmethod
    def createMDTimeSeries(self, id, values):
        return MDTimeSeries(value=values)

    # TODO remove -- Deprecated
    def createImportValue(self):
        iv = ImportValue()
        return iv

    def createTimeSeriesVariable(self, id, values, unit=None):
        if unit:
            unit = Unit(unit)
        ts = TimeSeries(value=values, unit=unit)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, ts)

    def createMDTimeSeriesVariable(self, id, values):
        MD_ts = MDTimeSeries(value=values)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, MD_ts)

    def createStateVariable(self, id, initialValue=None):
        initialValue = initialValue or PhysicalQuantity()
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, initialValue)

    def createParameterVariable(self, id, initialValue=None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_PARAMETER, initialValue)

    def createDynamicsVariable(self, id, dynamics=None, initialCondition=None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_DYNAMICS,
                                    Dynamics(dynamics=dynamics, initialCondition=initialCondition))

    def createHTMLVariable(self, id, html_text):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_HTML, HTML(html_text))

    def createURLVariable(self, id, url):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_URL, URL(url))

    def createTextVariable(self, id, text=''):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_TEXT, Text(text))

    def createPointVariable(self, id, x=1.0, y=1.0, z=1.0):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_POINT, Point(x, y, z))

    def createExpressionVariable(self, id, expression):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_EXPRESSION, Expression(expression))

    def createVisualVariable(self, id, initialValue: VisualValue = None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_VISUAL, initialValue)

    def createImageVariable(self, id, data=None, name=None, reference=None, format=None, initialValue=None):
        if data or name or reference or format:
            initialValue = Image(data=data, name=name, reference=reference, format=format)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_IMAGE, initialValue)

    def createConnectionVariable(self, id, initialValue: Connection = None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_CONNECTION, initialValue)

    def createParticlesVariable(self, id, particles):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_PARTICLES, Particles(particles=particles))

    def createPointerVariable(self, id, initialValue: Pointer):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_POINTER, initialValue)

    def createJSONVariable(self, id, serializable_obj):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_JSON, JSON(json.dumps(serializable_obj)))

    def createSimpleArrayVariable(self, id, initialValue: ArrayValue):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_SIMPLE_ARRAY, initialValue)

    def createMetadataVariable(self, id, initialValue: Metadata):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_METADATA, initialValue)
