from backports.functools_lru_cache import lru_cache
from chainmap import ChainMap
from pyecore.resources.json import JsonResource
from . import eClassifiers, datasources, types, values, variables

class GeppettoResource(JsonResource):
    packages = [eClassifiers,
                datasources.eClassifiers,
                types.eClassifiers,
                values.eClassifiers,
                variables.eClassifiers]
    chain = ChainMap(*packages)

    def serialize_eclass(self, eclass):
        return eclass.name

    @lru_cache()
    def resolve_eclass(self, uri):
        return self.chain.get(uri)