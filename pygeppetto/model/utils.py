from backports.functools_lru_cache import lru_cache
from chainmap import ChainMap
from pyecore.resources.json import JsonResource
from . import model as pygeppetto
from . import datasources
from . import types
from . import values
from . import variables


class GeppettoResource(JsonResource):
    packages = [pygeppetto.eClassifiers,
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
