import os

import pytest
from pyecore.resources import ResourceSet, URI
from pygeppetto.model.utils.pointer_utility import PointerUtility, GeppettoModelException


@pytest.fixture
def geppetto_model():
    res_set = ResourceSet()
    resource = res_set.get_resource(URI(os.path.join(os.path.dirname(__file__), "xmi-data/GeppettoModelTest2.xmi")))
    return resource.contents[0]


def test_get_pointer(geppetto_model):
    PointerUtility.get_pointer(geppetto_model, "addressBook[30].address.zone[4].area")
    PointerUtility.get_pointer(geppetto_model, "sample.person.name")


def test_equals(geppetto_model):
    p1 = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3].name(genericParameter)")
    p2 = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3].name(genericParameter)")
    assert p1 is not p2
    assert "addressBook(addressBook)[3].name(genericParameter)" == p1.get_instance_path()
    assert p1.get_instance_path() == p2.get_instance_path()
    assert PointerUtility.equals(p1, p2)
    p3 = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3]")
    assert p1 is not p3
    assert not PointerUtility.equals(p1, p3)
    p4 = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3].address(address)")
    assert p1 is not p3
    assert not (PointerUtility.equals(p1, p4))
    assert not (PointerUtility.equals(p3, p4))


def test_get_pointer_negative1(geppetto_model):
    with pytest.raises(GeppettoModelException):
        PointerUtility.get_pointer(geppetto_model, "addressBook(addressBok)[3].name(genericParameter)")


def test_get_pointer_negative2(geppetto_model):
    with pytest.raises(GeppettoModelException):
        PointerUtility.get_pointer(geppetto_model, "addresBook")


def test_get_pointer_negative3(geppetto_model):
    with pytest.raises(GeppettoModelException):
        PointerUtility.get_pointer(geppetto_model, "addressBook6]")


def test_get_pointer_negative4(geppetto_model):
    with pytest.raises(GeppettoModelException):
        PointerUtility.get_pointer(geppetto_model,
                                   "addressBook(addressBook)[30]address(address).zone(zone)[4].area(genericParameter)")


def test_get_pointer_negative5(geppetto_model):
    with pytest.raises(Exception):
        PointerUtility.get_pointer(geppetto_model, "addressBook[30].address.zone[].area")


def test_get_pointer_negative6(geppetto_model):
    with pytest.raises(GeppettoModelException):
        PointerUtility.get_pointer(geppetto_model, "addressBook[30].address.zone[2].arrea")


def test_get_pointer_negative7(geppetto_model):
    with pytest.raises(GeppettoModelException):
        PointerUtility.get_pointer(geppetto_model, "addressBook(addressBok)[3].")


def test_get_variable(geppetto_model):
    p = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3].name(genericParameter)")
    assert "name" == PointerUtility.get_variable(p).id
    assert "name" == PointerUtility.get_variable(p).name
    assert "genericParameter" == PointerUtility.get_variable(p).types[0].id
    p = PointerUtility.get_pointer(geppetto_model, "addressBook")
    assert "addressBook" == PointerUtility.get_variable(p).id
    assert "addressBook" == PointerUtility.get_variable(p).name
    assert "addressBook" == PointerUtility.get_variable(p).types[0].id
    p = PointerUtility.get_pointer(geppetto_model, "addressBook[6]")
    assert "addressBook" == PointerUtility.get_variable(p).id
    assert "addressBook" == PointerUtility.get_variable(p).name
    assert "addressBook" == PointerUtility.get_variable(p).types[0].id
    assert 6 == p.elements[0].index
    p = PointerUtility.get_pointer(geppetto_model,
                                   "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
    assert "area", PointerUtility.get_variable(p).id
    assert "area", PointerUtility.get_variable(p).name
    assert "genericParameter" == PointerUtility.get_variable(p).types[0].id
    assert 30, p.elements[0].index
    assert -1, p.elements[1].index
    assert 4, p.elements[2].index
    p = PointerUtility.get_pointer(geppetto_model, "addressBook[30].address.zone[4].area")
    assert "area", PointerUtility.get_variable(p).id
    assert "area", PointerUtility.get_variable(p).name
    assert "genericParameter" == PointerUtility.get_variable(p).types[0].id
    assert 30, p.elements[0].index
    assert -1, p.elements[1].index
    assert 4, p.elements[2].index


def test_get_type(geppetto_model):
    """ generated source for method testget_type """
    p = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3].name(genericParameter)")
    assert "genericParameter" == PointerUtility.get_type(p).id
    assert "genericParameter" == PointerUtility.get_type(p).name
    p = PointerUtility.get_pointer(geppetto_model, "addressBook")
    assert "addressBook" == PointerUtility.get_type(p).id
    assert "addressBook" == PointerUtility.get_type(p).name
    p = PointerUtility.get_pointer(geppetto_model, "addressBook[6]")
    assert "addressBook" == PointerUtility.get_type(p).id
    assert "addressBook" == PointerUtility.get_type(p).name
    assert int(6), p.elements[0].index
    p = PointerUtility.get_pointer(geppetto_model,
                                   "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
    assert "genericParameter" == PointerUtility.get_type(p).id
    assert "genericParameter" == PointerUtility.get_type(p).name
    p = PointerUtility.get_pointer(geppetto_model, "addressBook[30].address.zone[4].area")
    assert "genericParameter" == PointerUtility.get_type(p).id
    assert "genericParameter" == PointerUtility.get_type(p).name


def test_get_geppetto_library(geppetto_model):
    p = PointerUtility.get_pointer(geppetto_model, "addressBook(addressBook)[3].name(genericParameter)")
    assert "sample" == PointerUtility.get_geppetto_library(p).id
    assert "sample" == PointerUtility.get_geppetto_library(p).id
    p = PointerUtility.get_pointer(geppetto_model, "addressBook[6]")
    assert "sample" == PointerUtility.get_geppetto_library(p).id
    p = PointerUtility.get_pointer(geppetto_model,
                                   "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
    assert "sample" == PointerUtility.get_geppetto_library(p).id
    p = PointerUtility.get_pointer(geppetto_model, "addressBook[30].address.zone[4].area")
    assert "sample" == PointerUtility.get_geppetto_library(p).id


def test_get_instance_path(geppetto_model):
    p = PointerUtility.get_pointer(geppetto_model, "addressBook")
    assert "addressBook(addressBook)" == PointerUtility.get_instance_path(PointerUtility.get_variable(p),
                                                                          PointerUtility.get_type(p))
