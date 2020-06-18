from pyecore.resources import global_registry
from .model import nsURI, eSubpackages

from .model import overrides # Loads overrides

# Manually register all the URI and master URI in the global registry
# This registering is performed outside the previous 'for' to ease future
# code merging (in case of new metamodel versions)
geppetto_master_uri = ('https://raw.githubusercontent.com/openworm/'
                       'org.geppetto.model/master/src/main/resources/'
                       'geppettoModel.ecore')

global_registry[nsURI] = model
global_registry[geppetto_master_uri] = model
for subpack in eSubpackages:
    global_registry[subpack.nsURI] = subpack
    global_registry[geppetto_master_uri + '#//' + subpack.name] = subpack
