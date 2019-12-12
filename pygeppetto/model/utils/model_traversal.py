from pyecore.ecore import EObject
from pygeppetto.visitors import Switch


def apply_single(eobject: EObject, fn, condition=lambda eobject: True):
    for element in eobject.eAllContents():
        if condition(element):
            fn(element)


def apply(eobject: EObject, visitor: Switch):
    visitor.do_switch(eobject)
    for element in eobject.eAllContents():
        visitor.do_switch(element)


def apply_direct_children_only(eobject: EObject, visitor: Switch):
    for element in eobject.eContents:
        visitor.do_switch(element)
