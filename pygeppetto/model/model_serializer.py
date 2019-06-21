import sys

from pyecore.resources import ResourceSet
from pyecore.resources.json import JsonOptions
from pygeppetto.model import ISynchable

from .geppetto_resource import GeppettoResource
from .utils.bytesuri import BytesURI

GeppettoModelSerializer = GeppettoSerializer = sys.modules[__name__]

from pyecore.resources.json import DefaultObjectMapper


class SynchableMapper(DefaultObjectMapper):
    def __init__(self):
        pass

    def to_dict_from_obj(self, obj, options, use_uuid, resource):
        if hasattr(obj, 'synched'):
            if obj.synched:
                return {'synched': True}
            else:
                d = super().to_dict_from_obj(obj, options, use_uuid, resource)
                obj.synched = True
                return d
        else:
            return super().to_dict_from_obj(obj, options, use_uuid, resource)


class IgnoreSyncMapper(DefaultObjectMapper):
    def __init__(self):
        pass

    def to_dict_from_obj(self, obj, options, use_uuid, resource):
        if hasattr(obj, 'synched') and obj.synched:
            obj.synched = False
            d = super().to_dict_from_obj(obj, options, use_uuid, resource)
            obj.synched = True
            return d
        else:
            return super().to_dict_from_obj(obj, options, use_uuid, resource)


def serialize(geppetto_model, onlySerialiseDelta=False):
    # we now create a resource to save the geppetto model and serialize it to a JSON string
    rset = ResourceSet()
    uri = BytesURI('geppetto_model.json')
    rset.resource_factory['*'] = lambda uri: GeppettoResource(uri, indent=2)
    resource = rset.create_resource(uri)
    resource.append(geppetto_model)
    if onlySerialiseDelta:
        resource.register_mapper(ISynchable, SynchableMapper())
    else:
        resource.register_mapper(ISynchable, IgnoreSyncMapper())

    resource.save(options={JsonOptions.SERIALIZE_DEFAULT_VALUES: True})
    return uri.getvalue().decode("utf-8")


def load(json):
    rset = ResourceSet()
    uri = BytesURI('geppetto_model.json')
    rset.resource_factory['*'] = lambda uri: GeppettoResource(uri, indent=2)
    resource = rset.create_resource(uri)
