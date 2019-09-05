""" Derived from generated source for class PointerUtility
https://github.com/openworm/org.geppetto.model/blob/master/src/main/java/org/geppetto/model/util/java"""
import sys

from multimethod import multidispatch

from ..exceptions import GeppettoModelException
from ..model import GeppettoLibrary, GeppettoModel
from ..types import CompositeType, ArrayType, Type
from ..values.values import Pointer, PointerElement
from ..variables import Variable

# Fake a static class
PointerUtility = sys.modules[__name__]


@multidispatch
def get_pointer(variable: Variable, type_, index):
    pointerElement = PointerElement()
    pointerElement.index = index
    pointerElement.variable = variable
    pointerElement.type = type_
    pointer = Pointer(elements=(pointerElement,))

    return pointer


@get_pointer.register(GeppettoModel, str)
def get_pointer_model(model: GeppettoModel, instance_path):
    pointer = Pointer(path=instance_path)

    st = iter(instance_path.split("."))
    lastType = None

    for token in st:
        element = PointerElement()
        v = None
        if lastType is None:
            v = find_instance_variable(get_variable(token), model)
            if v is None:
                #  it's not an instance but it might a library
                library = find_library(model, token)
                if library is not None and st:
                    type_ = next(st)
                    lastType = get_type(model, token + "." + type_)
                    element.type = lastType
                    pointer.elements.add(element)
                    continue
                else:
                    raise GeppettoModelException(token + " is neither an instance variable nor a library id")
        else:
            if isinstance(lastType, CompositeType):
                v = find_variable(get_variable(token), lastType)
            else:
                if isinstance(lastType, ArrayType) and isinstance(lastType.arrayType, CompositeType):
                    v = find_variable(get_variable(token), (lastType).arrayType)
                else:
                    raise GeppettoModelException(
                        lastType.name + " is not of type CompositeType: there can't be nested variables")
        lastType = find_type(get_type_str(token), v)
        element.variable = v
        element.type = lastType
        if isinstance(element.type, ArrayType):
            index = get_index(token)
            if index is not None:
                element.index = get_index(token)
        pointer.elements.add(element)
    return pointer


@multidispatch
def get_type(model, path):
    st = iter(path.split('.'))
    lastType = None
    lastVar = None
    library = None
    for token in st:

        #  token can be a library, a type or a variable
        if lastType is not None:
            if isinstance(lastType, CompositeType):
                lastVar = find_variable(get_variable(token), lastType)
            elif isinstance(lastType, ArrayType) and isinstance(lastType.arrayType, CompositeType):
                lastVar = find_variable(get_variable(token), (lastType).arrayType)
            else:
                raise GeppettoModelException(
                    "{} is not of type CompositeType there can't be nested variables".format(lastType.id))
        elif lastVar is not None:
            lastType = find_type(get_type_str(token), lastVar)
        elif library is not None:
            lastType = find_type(token, library)
        else:
            #  they are all null
            library = find_library(model, token)
            if library is None:
                raise GeppettoModelException("Can't find a type for the path " + path)
    if lastType is not None and lastType.getPath() == path:
        return lastType
    else:
        raise GeppettoModelException("Couldn't find a type for the path " + path)


@get_type.register(str)
def get_type_str(token: str):
    if "(" in token:
        return token[token.find("(") + 1: token.find(")")]
    else:
        return None


@get_type.register(Pointer)
def get_type_pointer(pointer: Pointer):
    return pointer.elements[-1].type


def get_value(model, path, state_variable_type=None):
    st = iter(path.split('.'))
    lastType = None
    lastVar = None
    library = None
    for token in st:
        #  token can be a library, a type or a variable
        if lastType is not None:
            if isinstance(lastType, CompositeType):
                lastVar = find_variable(get_variable(token), lastType)
                lastType = None
            else:
                if isinstance(lastType, ArrayType) and isinstance(lastType.arrayType, CompositeType):
                    lastVar = find_variable(get_variable(token), (lastType).arrayType)
                else:
                    raise GeppettoModelException(
                        "{} is not of type CompositeType there can't be nested variables".format(lastType.id))
        elif lastVar is not None:
            lastType = find_type(get_type_str(token), lastVar)
        elif library is not None:
            lastType = find_type(token, library)
        else:
            #  they are all null
            library = find_library(model, token)
            if library is None:
                raise GeppettoModelException("Can't find a value for the path " + path)
    if lastType is not None and lastType.path == path:
        return lastType.defaultValue
    elif lastVar is not None:
        if state_variable_type is not None:
            try:
                return next(type_value_map.value for type_value_map in lastVar.initialValues if
                            type_value_map.type == state_variable_type)
            except StopIteration as e:
                raise GeppettoModelException("Couldn't find a value for the path " + path) from e
        else:
            return lastVar.initialValues[0].value
    else:
        raise GeppettoModelException("Couldn't find a value for the path " + path)


#
# 	 * @param model
# 	 * @param libraryId
# 	 * @return
# 	 * @throws GeppettoModelException
#
def find_library(model, libraryId):
    return next((library for library in model.libraries if library.id == libraryId), None)


#
# 	 * @param pointer
# 	 * @param pointer2
# 	 * @return true if the two pointers point to the same variables and types
#
@multidispatch
def equals(pointer: Pointer, pointer2: Pointer):
    if not pointer == pointer2:
        if len(pointer.elements) != len(pointer2.elements):
            return False
        for i, pe in enumerate(pointer.elements):
            try:
                pe2 = pointer2.elements[i]
            except:
                return False

            if not pe2 or not equals(pe, pe2):
                return False
    return True


#
# 	 * @param pointer
# 	 * @param pointer2
# 	 * @return
#
@equals.register(PointerElement, PointerElement)
def equals_pointer(pointer: PointerElement, pointer2: PointerElement):
    sameType = pointer.type == pointer2.type or pointer.type == pointer2.type
    sameVar = pointer.variable == pointer2.variable or pointer.variable == pointer2.variable
    sameIndex = pointer.index == pointer2.index
    return sameType and sameVar and sameIndex


#
# 	 * @param pointer
# 	 * @return
#
@multidispatch
def get_variable(pointer: Pointer):
    return pointer.elements[-1].variable


@get_variable.register(str)
def get_variable_str(token: str) -> str:
    if "(" in token:
        return token[0: token.find("(")]
    elif "[" in token:
        return token[0: token.find("[")]
    else:
        return token


def get_geppetto_library(pointer):
    type_ = get_type(pointer)
    while not isinstance(type_.eContainer(), GeppettoLibrary):
        type_ = type_.eContainer().eContainer()
    if (type_.eContainer()).id == "common":
        var = get_variable(pointer)
        type_ = var.eContainer()
        while not isinstance(type_.eContainer(), GeppettoLibrary):
            type_ = type_.eContainer().eContainer()
    return type_.eContainer()


def get_instance_path(variable, type_):
    return variable.id + "(" + type_.id + ")"


@multidispatch
def find_type(type_, variable: Variable) -> Type:
    if type_ is None:
        types = []
        types += variable.anonymousTypes
        types += variable.types
        if len(types) == 1:
            return types[0]
        elif len(types) == 0:
            raise GeppettoModelException("The variable {} has not types".format(variable.id))
        else:
            raise GeppettoModelException(
                "The instance path does not specify a type but more than one type are present for the variable {}".format(
                    variable.id))
    else:
        for t in variable.types:
            if t.id == type_:
                return t
        for t in variable.anonymousTypes:
            if t.id == type_:
                return t
        raise GeppettoModelException("The type {} was not found in the variable {}".format(type_, variable.id))


@find_type.register(str, GeppettoLibrary)
def find_type_library(typeId, library: GeppettoLibrary):
    return next((type_ for type_ in library.types if type_.id == typeId), None)


def find_instance_variable(variablename: str, model: GeppettoModel):
    for v in model.variables:
        if v.id == variablename:
            return v
    return None


def find_variable_from_path(model: GeppettoModel, path: str):
    return get_variable(get_pointer(model, path))


def find_variable(variablename: str, type_: Type) -> Variable:
    for v in type_.variables:
        if v.id == variablename:
            return v
    raise GeppettoModelException("The variable {} was not found in the type {}".format(variablename, type_.id))


def get_index(token):
    if "[" in token:
        return int(token[token.find("[") + 1: token.find("]")])
    else:
        return None


def get_path_without_types(path):
    return path.replaceAll("\\([^)]*\\)", "")
