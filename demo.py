from pyecore.resources import ResourceSet, URI
import model as pygeppetto

# We create a new resource set (not required, but better)
rset = ResourceSet()

model_url = URI('tests/xmi-data/MediumNet.net.nml.xmi')  # > 3100 objects
resource = rset.get_resource(model_url)  # We load the model
geppettomodel = resource.contents[0]  # We get the root

assert geppettomodel is not None  # Is the root not None?

# At this point, we can handle the geppettomodel variable as it is the XMI
# model root

# If geppettomodel name is empty or None we set it
if not geppettomodel.name:
    geppettomodel.name = 'pygeppetto_API_demo'

# We save the modified model in a new file
resource.save(output=URI('new-Medium.xmi'))
