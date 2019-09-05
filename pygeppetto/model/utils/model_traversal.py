from pyecore.ecore import EObject


def apply(eobject: EObject, fn, condition=lambda eobject: True):
    for element in eobject.eAllContents():
        if condition(element):
            fn(element)
