from .model import GeppettoModel
from .variables import Variable, TypeToValueMap
from .values import Cylinder, Sphere, Point, PhysicalQuantity, TimeSeries, Unit
from pyecore.resources import ResourceSet, URI
import os.path


class GeppettoModelFactory():

    def __init__(self):
        rset = ResourceSet()
        # Build the model URI
        model_uri = URI(os.path.join(os.path.dirname(__file__), '..',
                                     'ecore', 'GeppettoCommonLibrary.xmi'))
        resource = rset.get_resource(model_uri)  # We load the model
        self.geppetto_common_library = resource.contents[0]  # We get the root

    def createGeppettoModel(self, name):
        # We create a GeppettoModel instance and we add the common library to it
        geppetto_model = GeppettoModel(name=name, libraries=[self.geppetto_common_library])
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

    def createTimeSeries(self, id, values, unit=None):
        if unit:
            unit = Unit(unit)
        ts = TimeSeries(value=values, unit=unit)
        return ts

    def createStateVariable(self, id, initialValue=None):
        initialValue = initialValue or PhysicalQuantity()
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[2])
        if initialValue is not None:
            variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[2],initialValue))
        return variable
