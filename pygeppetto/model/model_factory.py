import json
import os.path

from deprecated import deprecated

from pyecore.resources import ResourceSet, URI
from pygeppetto.model import MDTimeSeries, Value, VisualValue, AArrayValue, SimpleInstance, SimpleConnectionInstance
from pygeppetto.model.values import Connectivity
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
    TYPE_EDGE = 16
    TYPE_NODE = 17

    rset = ResourceSet()
    # Build the model URI
    model_uri = URI(os.path.join(os.path.dirname(__file__), '..',
                                 'ecore', 'GeppettoCommonLibrary.xmi'))
    resource = rset.get_resource(model_uri)  # We load the model
    instance = resource.contents[0]

    @classmethod
    def instance_copy(cls):
        return clone(cls.instance)



class SharedLibraryManager:

    @staticmethod
    def get_shared_common_library():
        return GeppettoCommonLibrary.instance_copy()

class GeppettoModelFactory:


    def __init__(self, geppetto_common_library=None):
        if geppetto_common_library is None:
            geppetto_common_library = SharedLibraryManager.get_shared_common_library()
        self.geppetto_common_library = geppetto_common_library

    @classmethod
    def createGeppettoModel(cls, name):
        return GeppettoModel(name=name, libraries=(SharedLibraryManager.get_shared_common_library(),))

    def create_variable(self, id, cl_type, raw_initial_value):
        variable = Variable(id=id, name=id)
        _type = self.geppetto_common_library.types[cl_type] if isinstance(cl_type, int) else cl_type
        variable.types.append(self.geppetto_common_library.types[cl_type])
        variable.initialValues.append(TypeToValueMap(_type, raw_initial_value))
        return variable

    def create_simple_instance(self, id, cl_type, value=None):
        _type = self.geppetto_common_library.types[cl_type] if isinstance(cl_type, int) else cl_type
        return SimpleInstance(id=id, name=id, type=_type, value=value)

    def create_connection_instance(self, id, cl_type, a, b, connectivity: Connectivity, value=None):
        _type = self.geppetto_common_library.types[cl_type] if isinstance(cl_type, int) else cl_type
        return SimpleConnectionInstance(id=id, name=id, type=_type, a=a, b=b, connectivity=connectivity, value=value)

    @deprecated(version='0.6', reason='Use the snake case version')
    def createCylinder(self, id, bottomRadius=1.0, topRadius=1.0,
                       position=None, distal=None):

        return self.create_cylinder(id, bottomRadius, topRadius,
                                    position, distal)

    def create_cylinder(self, id, bottom_radius=1.0, top_radius=1.0,
                        position=None, distal=None):
        position = position or Point()
        distal = distal or Point()
        cylinder = Cylinder(bottomRadius=bottom_radius, topRadius=top_radius)
        cylinder.distal = distal
        cylinder.position = position

        return self.create_variable(id, GeppettoCommonLibrary.TYPE_VISUAL, cylinder)

    @deprecated(version='0.6', reason='Use the snake case version')
    def createSphere(self, id, radius=1.0, position=None):
        return self.create_sphere(id, radius, position)

    def create_sphere(self, id, radius=1.0, position=None):
        position = position or Point()
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[GeppettoCommonLibrary.TYPE_VISUAL])
        sphere = Sphere(radius=radius, position=position)
        variable.initialValues.append(
            TypeToValueMap(self.geppetto_common_library.types[GeppettoCommonLibrary.TYPE_VISUAL], sphere))
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_VISUAL, sphere)

    @classmethod
    @deprecated(version='0.6', reason='Use the snake case version')
    def createTimeSeries(cls, id=None, values=None, unit=None):
        return cls.create_time_series(values, unit)


    @classmethod
    def create_time_series(cls, values, unit=None):
        if unit:
            unit = Unit(unit)
        ts = TimeSeries(value=values, unit=unit)
        return ts

    @classmethod
    @deprecated(version='0.6', reason='no need to use the factory for this')
    def createMDTimeSeries(self, id, values):
        return MDTimeSeries(value=values)

    @deprecated(version='0.6', reason='no need to use the factory for this')
    def createImportValue(self):
        iv = ImportValue()
        return iv

    def create_time_series_variable(self, id, values, unit=None):
        if unit:
            unit = Unit(unit)
        ts = TimeSeries(value=values, unit=unit)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, ts)

    @deprecated(version='0.6', reason='Use the snake case version')
    def createMDTimeSeriesVariable(self, id, values):
        MD_ts = MDTimeSeries(value=values)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, MD_ts)

    def create_MD_time_series_variable(self, id, values):
        MD_ts = MDTimeSeries(value=values)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, MD_ts)

    @deprecated(version='0.6', reason='Use the snake case version')
    def createStateVariable(self, id, initialValue=None):
        return self.create_state_variable(id, initialValue)

    def create_state_variable(self, id, initialValue=None):
        initialValue = initialValue or PhysicalQuantity()
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_STATE_VARIABLE, initialValue)

    def create_parameter_variable(self, id, initialValue=None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_PARAMETER, initialValue)

    def create_dynamics_variable(self, id, dynamics=None, initialCondition=None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_DYNAMICS,
                                    Dynamics(dynamics=dynamics, initialCondition=initialCondition))

    def create_html_variable(self, id, html_text):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_HTML, HTML(html_text))

    def create_url_variable(self, id, url):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_URL, URL(url))

    def create_text_variable(self, id, text=''):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_TEXT, Text(text))

    def create_point_variable(self, id, x=1.0, y=1.0, z=1.0):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_POINT, Point(x, y, z))

    def create_expression_variable(self, id, expression):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_EXPRESSION, Expression(expression))

    def create_visual_variable(self, id, initialValue: VisualValue = None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_VISUAL, initialValue)

    def create_image_variable(self, id, data=None, name=None, reference=None, format=None, initialValue=None):
        if data or name or reference or format:
            initialValue = Image(data=data, name=name, reference=reference, format=format)
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_IMAGE, initialValue)

    def create_connection_variable(self, id, initialValue: Connection = None):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_CONNECTION, initialValue)

    def create_particles_variable(self, id, particles):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_PARTICLES, Particles(particles=particles))

    def create_pointer_variable(self, id, initialValue: Pointer):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_POINTER, initialValue)

    def create_JSON_variable(self, id, serializable_obj):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_JSON, JSON(json.dumps(serializable_obj)))

    def create_simple_array_variable(self, id, initialValue: AArrayValue):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_SIMPLE_ARRAY, initialValue)

    def create_metadata_variable(self, id, initialValue: Metadata):
        return self.create_variable(id, GeppettoCommonLibrary.TYPE_METADATA, initialValue)

    def create_node_instance(self, id, value):
        return self.create_simple_instance(id, GeppettoCommonLibrary.TYPE_NODE, value)

    def create_edge_instance(self, id, a, b, connectivity: Connection, value=None):
        return self.create_connection_instance(id, GeppettoCommonLibrary.TYPE_EDGE, a=a, b=b, connectivity=connectivity, value=value)
