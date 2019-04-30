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

    for e in all_objects:
        cloned = create_instance(e)
        created_elements[e] = cloned
        clone_refs[e] = (cloned, first_setup(e, cloned))

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
