from model import GeppettoModel
from .variables import Variable, TypeToValueMap
from .values import Cylinder, Sphere, Point, PhysicalQuantity
from pyecore.resources import ResourceSet, URI
import os.path

class GeppettoModelFactory():

    def __init__(self):
        rset = ResourceSet()
        model_url = URI(os.path.join(os.path.dirname(__file__), '../ecore/GeppettoCommonLibrary.xmi'))  # The model URI
        resource = rset.get_resource(model_url)  # We load the model
        self.geppetto_common_library = resource.contents[0]  # We get the root

    def createGeppettoModel(self, name):
        # We create a GeppettoModel instance and we add the common library to it
        geppetto_model = GeppettoModel(name=name, libraries=[self.geppetto_common_library])
        return geppetto_model

    def createCylinder(self, id, bottomRadius=1.0,topRadius=1.0,position=Point(),distal=Point()):
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[8])
        cylinder = Cylinder(bottomRadius=bottomRadius, topRadius=topRadius)
        cylinder.distal=distal
        cylinder.position=position
        variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[8],cylinder))
        return variable

    def createSphere(self, id, radius=1.0,position=Point()):
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[8])
        sphere = Sphere(radius=radius, position=position)
        variable.initialValues.append(TypeToValueMap(self.geppetto_common_library.types[8],sphere))
        return variable

    def createStateVariable(self, id, initialValue=PhysicalQuantity()):
        variable = Variable(id=id)
        variable.types.append(self.geppetto_common_library.types[2])
        if(initialValue):
            pass
            #Create value and add it
        return variable

