import os.path

from pyecore.resources import ResourceSet, URI
from pygeppetto.model import MDTimeSeries
from pygeppetto.utils import clone

from .model import GeppettoModel
from .values import Cylinder, Sphere, Point, PhysicalQuantity, TimeSeries, Unit, ImportValue, Text
from .variables import Variable, TypeToValueMap


class GeppettoCommonLibrary:
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

    def createCylinder(self, id, bottomRadius=1.0, topRadius=1.0,
                       position=None, distal=None):
        position = position or Point()
        distal = distal or Point()
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[8])
        cylinder = Cylinder(bottomRadius=bottomRadius, topRadius=topRadius)
        cylinder.distal = distal
        cylinder.position = position
        variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[8], cylinder))
        return variable

    def createSphere(self, id, radius=1.0, position=None):
        position = position or Point()
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[8])
        sphere = Sphere(radius=radius, position=position)
        variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[8], sphere))
        return variable

    @classmethod
    def createTimeSeries(cls, id, values, unit=None):
        if unit:
            unit = Unit(unit)
        ts = TimeSeries(value=values, unit=unit)
        return ts

    def createMDTimeSeries(self, id, values):
        MD_ts = MDTimeSeries(value=values)
        return MD_ts

    @classmethod
    def createImportValue(cls):
        iv = ImportValue()
        return iv

    def createStateVariable(self, id, initialValue=None):
        initialValue = initialValue or PhysicalQuantity()
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[2])
        if initialValue is not None:
            variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[2], initialValue))
        return variable

    def createTextVariable(self, id, text=''):
        variable = Variable(name=id, id=id)
        variable.types.append(self.geppetto_common_library.types[5])
        variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[5], Text(text)))

        return variable
