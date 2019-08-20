import json

import pytest
from pyecore.resources import ResourceSet, URI
from pygeppetto.model import StateVariableType, Quantity, TimeSeries, VisualType, JSONType
from pygeppetto.model.model_factory import GeppettoModelFactory


@pytest.fixture()
def model_factory():
    return GeppettoModelFactory(GeppettoModelFactory.createGeppettoModel('testModel'))


def test_model_factory(model_factory):
    assert model_factory.geppetto_model


def test_create_cylinder(model_factory):
    var = model_factory.createCylinder('c1')

    assert type(var.types[0]) == VisualType
    assert var.id == 'c1'
    c = var.initialValues[0].value

    assert c.bottomRadius == 1.0
    assert c.topRadius == 1.0

    var = model_factory.createCylinder('c23', 2.0, 3.0)
    c = var.initialValues[0].value
    assert var.id == 'c23'
    assert c.bottomRadius == 2.0
    assert c.topRadius == 3.0


def test_create_state_variable(model_factory):
    var = model_factory.createStateVariable(id='aname', initialValue=Quantity(value=10.0))
    assert var.id == 'aname'
    assert var.initialValues[0].value.value == 10
    assert type(var.types[0]) == StateVariableType


def test_create_time_series(model_factory):
    var = model_factory.createTimeSeriesVariable('aname', values=[1, 2.0], unit='mV')

    assert var.id == 'aname'
    assert type(var.types[0]) == StateVariableType

    ts = var.initialValues[0].value
    assert ts.value[0] == 1
    assert type(ts) == TimeSeries


def test_create_json(model_factory):
    var = model_factory.createJSONVariable('aname', {'a': 1, 'b': 2})

    assert var.id == 'aname'
    assert type(var.types[0]) == JSONType

    v = json.loads(var.initialValues[0].value.json)
    assert v['a'] == 1
