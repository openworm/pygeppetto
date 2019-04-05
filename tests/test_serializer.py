import json
import os

from pyecore.resources import ResourceSet, URI
from pygeppetto.model.model_serializer import GeppettoModelSerializer as GeppettoSerializer


def testSerializer():
    #  Initialize the factory and the resource set
    resSet = ResourceSet()
    #  How to read
    resource = resSet.get_resource(URI(os.path.join(os.path.dirname(__file__), "xmi-data/GeppettoModelTest.xmi")))

    geppettoModel = resource.contents[0]

    with open(os.path.join(os.path.dirname(__file__), "json-data/test.json")) as testfile:
        jsonResource = testfile.read()
    expected_json = json.loads(jsonResource)
    assert json.loads(GeppettoSerializer.serialize(geppettoModel)) == expected_json
    assert json.loads(GeppettoSerializer.serialize(geppettoModel, True)) == expected_json
    assert json.loads(GeppettoSerializer.serialize(geppettoModel)) == expected_json
    assert geppettoModel.getVariables().get(0).isSynched()

    expected_json_synched = json.loads(
        "{'eClass':'GeppettoModel','id':'','name':'','variables':[{'synched':true}],'libraries':[{'synched':true}]}")
    assert json.loads(GeppettoSerializer.serialize(
        geppettoModel, True)) == expected_json_synched
