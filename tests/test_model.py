import json

import pytest
from pyecore.ecore import EString
from pyecore.resources import ResourceSet, URI
from pygeppetto.model import TypeToValueMap, Variable
from pygeppetto.model.types import *
from pygeppetto.model.values import *
from pygeppetto.model.model_factory import GeppettoModelFactory


@pytest.fixture()
def model_factory():
    return GeppettoModelFactory()


def test_array_nested_type(model_factory):
    level1_type = CompositeType(id='level1type')
    level1_type = level1_type

    level2_type = CompositeType(id='level2type')
    level2_type = level2_type
    level2_type.variables.append(model_factory.create_text_variable(id='l3', text='default text'))

    vl2 = Variable(id='l2', name='l2', types=(level2_type,))
    level1_type.variables.append(vl2)

    vl1value = Composite()

    vl2value = Composite()
    vl2value.value.append(StringToValueMap('l3', Text('my_text')))

    vl1value.value.append(StringToValueMap('l2', vl2value))

    array_value = ArrayValue()
    array_value.elements.append(ArrayElement(index=0, initialValue=vl1value))

    assert array_value.elements[0].initialValue is not None

    referencing_type = ArrayType(defaultValue=ArrayValue(), arrayType=level1_type)
    v = Variable(id='list', types=(referencing_type,))
    v.initialValues.append(TypeToValueMap(referencing_type, array_value))


def test_create_cylinder(model_factory):
    var = model_factory.create_cylinder('c1')

    assert type(var.types[0]) == VisualType
    assert var.id == 'c1'
    c = var.initialValues[0].value

    assert c.bottomRadius == 1.0
    assert c.topRadius == 1.0

    var = model_factory.create_cylinder('c23', 2.0, 3.0)
    c = var.initialValues[0].value
    assert var.id == 'c23'
    assert c.bottomRadius == 2.0
    assert c.topRadius == 3.0


def test_create_sphere(model_factory):
    var = model_factory.create_sphere('s1')

    assert type(var.types[0]) == VisualType
    assert var.id == 's1'
    c = var.initialValues[0].value

    assert c.radius == 1.0
    assert type(c.position) == Point

    var = model_factory.create_sphere('s23', 2.0, Point(1.0, 1.0, 1.0))
    c = var.initialValues[0].value
    assert var.id == 's23'
    assert c.radius == 2.0


def test_create_state_variable(model_factory):
    var = model_factory.create_state_variable(id='aname', initialValue=Quantity(value=10.0))
    assert var.id == 'aname'
    assert var.initialValues[0].value.value == 10
    assert type(var.types[0]) == StateVariableType


def test_create_time_series_variable(model_factory):
    var = model_factory.create_time_series_variable('aname', values=[1, 2.0], unit='mV')

    assert var.id == 'aname'
    assert type(var.types[0]) == StateVariableType

    ts = var.initialValues[0].value
    assert ts.value[0] == 1
    assert type(ts) == TimeSeries


def test_create_json(model_factory):
    var = model_factory.create_JSON_variable('aname', {'a': 1, 'b': 2})

    assert var.id == 'aname'
    assert type(var.types[0]) == JSONType

    v = json.loads(var.initialValues[0].value.json)
    assert v['a'] == 1


def test_create_parameter_variable(model_factory):
    var = model_factory.create_parameter_variable('aname')

    assert var.id == 'aname'
    assert type(var.types[0]) == ParameterType


def test_create_dynamics_variable(model_factory):
    var = model_factory.create_dynamics_variable('aname')

    assert var.id == 'aname'
    assert type(var.types[0]) == DynamicsType


def test_create_html_variable(model_factory):
    var = model_factory.create_html_variable('aname', '<p>Text</p>')

    assert var.id == 'aname'
    assert type(var.types[0]) == HTMLType

    value = var.initialValues[0].value
    assert type(value) == HTML
    assert value.html == '<p>Text</p>'


def test_create_url_variable(model_factory):
    var = model_factory.create_url_variable('aname', 'http://someurl')

    assert var.id == 'aname'
    assert type(var.types[0]) == URLType

    value = var.initialValues[0].value
    assert type(value) == URL
    assert value.url == 'http://someurl'


def test_create_text_variable(model_factory):
    var = model_factory.create_text_variable('aname', 'a text')

    assert var.id == 'aname'
    assert type(var.types[0]) == TextType

    value = var.initialValues[0].value
    assert type(value) == Text
    assert value.text == 'a text'


def test_create_point_variable(model_factory):
    var = model_factory.create_point_variable('aname', 1.0, 2.0, 3.0)

    assert var.id == 'aname'
    assert type(var.types[0]) == PointType

    value = var.initialValues[0].value
    assert type(value) == Point
    assert value.x == 1.0
    assert value.y == 2.0
    assert value.z == 3.0


def test_create_expression_variable(model_factory):
    var = model_factory.create_expression_variable('aname', '')

    assert var.id == 'aname'
    assert type(var.types[0]) == ExpressionType

    value = var.initialValues[0].value
    assert type(value) == Expression


def test_create_visual_variable(model_factory):
    var = model_factory.create_visual_variable('aname')

    assert var.id == 'aname'
    assert type(var.types[0]) == VisualType


def test_create_image_variable(model_factory):
    var = model_factory.create_image_variable('aname')

    assert var.id == 'aname'
    assert type(var.types[0]) == ImageType


def test_create_connection_variable(model_factory):
    var = model_factory.create_connection_variable('aname')

    assert var.id == 'aname'
    assert type(var.types[0]) == ConnectionType


def test_create_particles_variable(model_factory):
    var = model_factory.create_particles_variable('aname', [])

    assert var.id == 'aname'
    assert type(var.types[0]) == VisualType


def test_create_pointer_variable(model_factory):
    var = model_factory.create_pointer_variable('aname', Pointer())

    assert var.id == 'aname'
    assert type(var.types[0]) == PointerType


def test_create_simple_array_variable(model_factory):
    var = model_factory.create_simple_array_variable('aname', IntArray([1, 2]))

    assert var.id == 'aname'
    assert type(var.types[0]) == SimpleArrayType
    value = var.initialValues[0].value
    assert type(value) == IntArray
    assert value.elements[0] == 1


def test_create_metadata_variable(model_factory):
    metadata = Metadata(
        [StringToValueMap('akey', Text('avalue')), StringToValueMap('anotherkey', Text('anothervalue'))])

    var = model_factory.create_metadata_variable('aname', metadata)

    assert var.id == 'aname'
    assert type(var.types[0]) == MetadataType
    value = var.initialValues[0].value
    assert type(value) == Metadata


def test_create_node_instance(model_factory):
    value = JSON('{"a": 1}')
    instance = model_factory.create_node_instance(id='inst', value=value)
    assert json.loads(instance.value.json)['a'] == 1


def test_create_edge_instance(model_factory):
    a = model_factory.create_node_instance(id='a', value=JSON('{"a": 1}'))
    b = model_factory.create_node_instance(id='b', value=JSON('{"b": 1}'))
    edge = model_factory.create_edge_instance('ab', a, b, Connectivity.from_string('DIRECTIONAL'),
                                              value=Metadata([StringToValueMap('akey', Text('avalue')),
                                                              StringToValueMap('anotherkey', Text('anothervalue'))]
                                                             )
                                              )
    assert json.loads(edge.a.value.json)['a'] == 1
    assert json.loads(edge.b.value.json)['b'] == 1
    assert str(edge.connectivity) == 'DIRECTIONAL'
    assert type(edge.value) == Metadata
