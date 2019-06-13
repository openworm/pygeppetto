""" Derived from generated source for class PointerUtility
https://github.com/openworm/org.geppetto.model/blob/master/src/main/java/org/geppetto/model/util/java"""
import sys

from multimethod import multidispatch

from ..exceptions import GeppettoModelException
from ..model import GeppettoLibrary, GeppettoModel
from ..types import CompositeType, ArrayType, Type
from ..values.values import Pointer, PointerElement
from ..values.values_factory import ValuesFactory
from ..variables import Variable

# Fake a static class
PointerUtility = sys.modules[__name__]


#
# 	 * @param variable
# 	 * @param type
# 	 * @param index
# 	 * @return
#
@multidispatch
def getPointer(variable: Variable, type_, index):
    """ generated source for method getPointer """
    pointer = ValuesFactory.eINSTANCE.createPointer()
    pointerElement = ValuesFactory.eINSTANCE.createPointerElement()
    pointerElement.setIndex(index)
    pointerElement.setVariable(variable)
    pointerElement.setType(type_)
    pointer.elements.add(pointerElement)
    pointer.setPath(pointer.getInstancePath())
    return pointer


#
# 	 * @param model
# 	 * @param instancePath
# 	 * @return
#
#
# 	 * @param model
# 	 * @param instancePath
# 	 * @return
# 	 * @throws GeppettoModelException
#
@getPointer.register(GeppettoModel, str)
def getPointer_model(model: GeppettoModel, instancePath):
    """ generated source for method getPointer_0 """
    pointer = ValuesFactory.eINSTANCE.createPointer()
    pointer.setPath(instancePath)
    st = iter(instancePath.split("."))
    lastType = None

    for token in st:
        element = ValuesFactory.eINSTANCE.createPointerElement()
        v = None
        if lastType is None:
            v = findInstanceVariable(getVariable(token), model)
            if v is None:
                #  it's not an instance but it might a library
                library = findLibrary(model, token)
                if library is not None and st:
                    type_ = next(st)
                    lastType = getType(model, token + "." + type_)
                    element.setType(lastType)
                    pointer.elements.add(element)
                    continue
                else:
                    raise GeppettoModelException(token + " is neither an instance variable nor a library id")
        else:
            if isinstance(lastType, CompositeType):
                v = findVariable(getVariable(token), lastType)
            else:
                if isinstance(lastType, ArrayType) and isinstance(lastType.arrayType, CompositeType):
                    v = findVariable(getVariable(token), (lastType).arrayType)
                else:
                    raise GeppettoModelException(
                        lastType.id + " is not of type CompositeType there can't be nested variables")
        lastType = findType(getType_str(token), v)
        element.setVariable(v)
        element.setType(lastType)
        if isinstance(element.type, ArrayType):
            index = getIndex(token)
            if index is not None:
                element.setIndex(getIndex(token))
        pointer.elements.add(element)
    return pointer


#
# 	 * @param model
# 	 * @param instancePath
# 	 * @return
#
#
# 	 * @param model
# 	 * @param instancePath
# 	 * @return
# 	 * @throws GeppettoModelException
#
@multidispatch
def getType(model, path):
    """ generated source for method getType """
    st = iter(path.split('.'))
    lastType = None
    lastVar = None
    library = None
    for token in st:

        #  token can be a library, a type or a variable
        if lastType is not None:
            if isinstance(lastType, CompositeType):
                lastVar = findVariable(getVariable(token), lastType)
            elif isinstance(lastType, ArrayType) and isinstance(lastType.arrayType, CompositeType):
                lastVar = findVariable(getVariable(token), (lastType).arrayType)
            else:
                raise GeppettoModelException(
                    "{} is not of type CompositeType there can't be nested variables".format(lastType.id))
        elif lastVar is not None:
            lastType = findType(getType_str(token), lastVar)
        elif library is not None:
            lastType = findType(token, library)
        else:
            #  they are all null
            library = findLibrary(model, token)
            if library is None:
                raise GeppettoModelException("Can't find a type for the path " + path)
    if lastType is not None and lastType.getPath() == path:
        return lastType
    else:
        raise GeppettoModelException("Couldn't find a type for the path " + path)


@getType.register(str)
def getType_str(token: str):
    """ generated source for method getType_1 """
    if "(" in token:
        return token[token.find("(") + 1: token.find(")")]
    else:
        return None


@getType.register(Pointer)
def getType_pointer(pointer: Pointer):
    """ generated source for method getType_0 """
    return pointer.elements[-1].type


def getValue(model, path, stateVariablType):
    """ generated source for method getValue """
    # FIXME there's something wrong here and also on Java implementation: the value should be retrieved from the instance path, not type path.
    st = iter(path.split('.'))
    lastType = None
    lastVar = None
    library = None
    for token in st:
        #  token can be a library, a type or a variable
        if lastType is not None:
            if isinstance(lastType, CompositeType):
                lastVar = findVariable(getVariable(token), lastType)
                lastType = None
            else:
                if isinstance(lastType, ArrayType) and isinstance(lastType.arrayType, CompositeType):
                    lastVar = findVariable(getVariable(token), (lastType).arrayType)
                else:
                    raise GeppettoModelException(
                        "{} is not of type CompositeType there can't be nested variables".format(lastType.id))
        elif lastVar is not None:
            lastType = findType(getType_str(token), lastVar)
        elif library is not None:
            lastType = findType(token, library)
        else:
            #  they are all null
            library = findLibrary(model, token)
            if library is None:
                raise GeppettoModelException("Can't find a value for the path " + path)
    if lastType is not None and lastType.path == path:
        return lastType.defaultValue
    elif lastVar is not None:
        return lastVar.initialValues[stateVariablType]
    else:
        raise GeppettoModelException("Couldn't find a value for the path " + path)


#
# 	 * @param model
# 	 * @param libraryId
# 	 * @return
# 	 * @throws GeppettoModelException
#
def findLibrary(model, libraryId):
    """ generated source for method findLibrary """
    return next((library for library in model.getLibraries() if library.id == libraryId), None)


#
# 	 * @param pointer
# 	 * @param pointer2
# 	 * @return true if the two pointers point to the same variables and types
#
@multidispatch
def equals(pointer: Pointer, pointer2: Pointer):
    """ generated source for method equals """
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
    """ generated source for method equals_0 """
    sameType = pointer.type == pointer2.type or pointer.type == pointer2.type
    sameVar = pointer.variable == pointer2.variable or pointer.variable == pointer2.variable
    sameIndex = pointer.index == pointer2.index
    return sameType and sameVar and sameIndex


#
# 	 * @param pointer
# 	 * @return
#
@multidispatch
def getVariable(pointer: Pointer):
    """ generated source for method getVariable """
    return pointer.elements[-1].variable


@getVariable.register(str)
def getVariable_str(token: str) -> str:
    """ generated source for method getVariable_0 """
    if "(" in token:
        return token[0: token.find("(")]
    elif "[" in token:
        return token[0: token.find("[")]
    else:
        return token


def getGeppettoLibrary(pointer):
    """ generated source for method getGeppettoLibrary """
    type_ = getType(pointer)
    while not isinstance(type_.eContainer(), GeppettoLibrary):
        type_ = type_.eContainer().eContainer()
    if (type_.eContainer()).id == "common":
        var = getVariable(pointer)
        type_ = var.eContainer()
        while not isinstance(type_.eContainer(), GeppettoLibrary):
            type_ = type_.eContainer().eContainer()
    return type_.eContainer()


def getInstancePath(variable, type_):
    """ generated source for method getInstancePath """
    return variable.id + "(" + type_.id + ")"


@multidispatch
def findType(type_, variable: Variable) -> Type:
    """ generated source for method findType_0 """
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


#
# 	 * @param typeId
# 	 * @param library
# 	 * @return
#
@findType.register(str, GeppettoLibrary)
def findType_library(typeId, library: GeppettoLibrary):
    """ generated source for method findType """
    return next((type_ for type_ in library.types if type_.id == typeId), None)


def findInstanceVariable(variablename: str, model: GeppettoModel):
    """ generated source for method findInstanceVariable """
    for v in model.getVariables():
        if v.id == variablename:
            return v
    return None


def findVariable(variablename: str, type_: Type) -> Variable:
    """ generated source for method findVariable """
    for v in type_.getVariables():
        if v.id == variablename:
            return v
    raise GeppettoModelException("The variable " + variablename + " was not found in the type " + type_.id)


def getIndex(token):
    """ generated source for method getIndex """
    if "[" in token:
        return int(token[token.find("[") + 1: token.find("]")])
    else:
        return None


def getPathWithoutTypes(path):
    """ generated source for method getPathWithoutTypes """
    return path.replaceAll("\\([^)]*\\)", "")
