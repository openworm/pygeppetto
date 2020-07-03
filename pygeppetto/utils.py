import pkgutil
import importlib
import requests


from pyecore.ecore import EObject, EClass, EReference

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def clone(eobject, skip_containment=False, skip_refs=False):
    if not isinstance(eobject, EObject) and not isinstance(eobject, type):
        return eobject
    if isinstance(eobject, type):
        eobject = eobject.eClass

    def create_instance(original):
        if isinstance(original, type):
            original = original.eClass
            cloned_object = original.eClass(original.name)
        elif original.eClass is EClass.eClass:
            cloned_object = original.eClass(original.name)
        else:
            cloned_object = original.eClass()
        return cloned_object

    def first_setup(original, cloned):
        references = []
        for feature in original._isset:
            if isinstance(feature, EReference):
                if skip_refs:
                    continue
                opposite = feature.eOpposite
                if opposite and (opposite.containment or opposite in references):
                    continue
                if skip_containment and feature.containment:
                    continue
                references.append(feature)
                continue
            if feature.many:
                cloned.eGet(feature).extend(original.eGet(feature))
            else:
                cloned.eSet(feature, original.eGet(feature))
        return references

    created_elements = {}
    clone_refs = {}
    all_objects = [eobject]
    if not skip_containment:
        all_objects.extend(eobject.eAllContents())

    for e_obj in all_objects:
        cloned = create_instance(e_obj)
        created_elements[e_obj] = cloned
        clone_refs[e_obj] = (cloned, first_setup(e_obj, cloned))

    if skip_refs:
        return created_elements.get(eobject)

    for original, (cloned, refs) in clone_refs.items():
        for feature in refs:
            if feature.many:
                eobjs = [created_elements.get(x, x) for x in original.eGet(feature)]
                cloned.eGet(feature).extend(eobjs)
            else:
                obj = original.eGet(feature)
                cloned.eSet(feature, created_elements.get(obj, obj))
    return created_elements.get(eobject)


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def stream_requests(url, params, method="GET", chunk_size=8192, auth=None):
    processed_output = []
    kwargs = {"url": url, "stream": True}

    if method == "POST":
        method = requests.post
        kwargs["json"] = params

    elif method == "GET":
        method = requests.get
        kwargs["params"] = params

    if auth:
        kwargs["auth"] = auth

    with method(**kwargs) as result:
        for chunk in result.iter_lines(chunk_size=chunk_size, delimiter=b'\n'):
            if chunk:
                processed_output.append(chunk.decode("utf-8"))

    return processed_output
