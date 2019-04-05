from multimethod import multidispatch
from pygeppetto.constants import GeppettoPackage
from pygeppetto.model import GeppettoLibrary
from pygeppetto.model.exceptions import GeppettoVisitingException
from pygeppetto.model.utils.pointer_utility import PointerUtility

from src.pyecore.pyecore.ecore import EClass


class GeppettoModelAccess(object):
    """ generated source for class GeppettoModelAccess """
    geppettoModel = None
    commonlibrary = GeppettoLibrary()
    editingDomain = None

    def __init__(self, geppettoModel):
        """ generated source for method __init__ """
        super(GeppettoModelAccess, self).__init__()
        self.geppettoModel = geppettoModel
        # self.editingDomain = AdapterFactoryEditingDomain.getEditingDomainFor(geppettoModel)
        # if self.editingDomain == None:
        #     self.editingDomain = AdapterFactoryEditingDomain(ComposedAdapterFactory(), BasicCommandStack())
        for library in geppettoModel.getLibraries():
            if library.id == "common":
                self.commonlibrary = library
                break
        if self.commonlibrary == None:
            raise GeppettoVisitingException("Common library not found")

    #
    # 	 * Usage commonLibraryAccess.getType(TypesPackage.Literals.PARAMETER_TYPE);
    # 	 *
    # 	 * @return
    # 	 * @throws GeppettoVisitingException
    #
    @multidispatch
    def getType(self, eclass):
        """ generated source for method getType """
        try:
            return next(type_ for type_ in self.commonlibrary.types if type_.eClass() == eclass)
        except StopIteration:
            raise GeppettoVisitingException("Type for eClass " + eclass + " not found in common library.")

    #
    # 	 * Usage commonLibraryAccess.getType(TypesPackage.Literals.VISUAL_TYPE, "particles");
    # 	 * @param eclass
    # 	 * @param id
    # 	 * @return
    # 	 * @throws GeppettoVisitingException
    #
    @getType.register(object, EClass, str)
    def getType_0(self, eclass, id):
        """ generated source for method getType_0 """
        try:
            return next(type_ for type_ in self.commonlibrary.types if type_.eClass() == eclass and type_.id == id)
        except StopIteration:
            raise GeppettoVisitingException("Type for eClass " + eclass + " not found in common library.")

    #
    # 	 * @param instancePath
    # 	 * @return
    # 	 * @throws GeppettoModelException
    #
    def getPointer(self, instancePath):
        """ generated source for method getPointer """
        return PointerUtility.getPointer(self.geppettoModel, instancePath)

    #
    # 	 * @param variable
    #
    def addVariable(self, variable):
        """ generated source for method addVariable """
        raise NotImplemented()

    #
    # 	 * @param tag
    #
    def addTag(self, tag):
        """ generated source for method addTag """
        raise NotImplemented()

    #
    # 	 * @param tag
    #
    def addLibrary(self, library):
        """ generated source for method addLibrary """
        raise NotImplemented()

    #
    # 	 * @param tag
    #
    def addTypeToLibrary(self, type_, targetLibrary):
        """ generated source for method addTypeToLibrary """
        self.markAsUnsynched(targetLibrary)
        raise NotImplemented()

    #
    # 	 * This method will change an attribute of an object
    # 	 *
    # 	 * @param object
    # 	 *            the object target of the operation
    # 	 * @param field
    # 	 *            the field to set, needs to come from the Literals enumeration inside the package, e.g. GeppettoPackage.Literals.NODE__NAME to change the name
    # 	 * @param value
    # 	 *            the new value
    #
    def setObjectAttribute(self, object_, field, value):
        """ generated source for method setObjectAttribute """
        raise NotImplemented()

    #
    # 	 * This method will set the synched attribute for the object to false indicating that whatever version of the object exists client side it is now out of synch
    # 	 *
    # 	 * @param object
    #
    def markAsUnsynched(self, object_):
        """ generated source for method markAsUnsynched """
        raise NotImplemented()

    #
    # 	 * @param typeToRetrieve
    # 	 * @param libraries
    # 	 * @return
    #
    def getOrCreateSimpleType(self, typeToRetrieve, libraries):
        """ generated source for method getOrCreateSimpleType """
        raise NotImplemented()
        for dependencyLibrary in libraries:
            for candidateSuperType in dependencyLibrary.getTypes():
                if candidateSuperType.getId() == typeToRetrieve:
                    return candidateSuperType
        supertypeType = TypesFactory.eINSTANCE.createSimpleType()
        supertypeType.setId(typeToRetrieve)
        supertypeType.setName(typeToRetrieve)
        self.addTypeToLibrary(supertypeType, libraries.get(0))
        return supertypeType

    #
    # 	 * @param newVar
    # 	 * @param targetType
    #
    def addVariableToType(self, newVar, targetType):
        """ generated source for method addVariableToType """
        self.markAsUnsynched(targetType)
        raise NotImplemented()

    #
    # 	 * Note this command won't remove the typeToBeReplaced from its container in case it's being iterated over
    # 	 *
    # 	 * @param typeToBeReplaced
    # 	 * @param newType
    # 	 * @param library
    #
    def swapType(self, typeToBeReplaced, newType, library):
        """ generated source for method swapType """
        raise NotImplemented()
        replaceCommand = ReplaceCommand.create(self.editingDomain, typeToBeReplaced.eContainer(),
                                               GeppettoPackage.Literals.GEPPETTO_LIBRARY__TYPES, typeToBeReplaced,
                                               Collections.singleton(newType))
        self.editingDomain.getCommandStack().execute(replaceCommand)
        self.markAsUnsynched(newType.eContainer())
        referencedVars = ArrayList(typeToBeReplaced.getReferencedVariables())
        for v in referencedVars:
            replaceInVarCommand = ReplaceCommand.create(self.editingDomain, v,
                                                        VariablesPackage.Literals.VARIABLE__TYPES, typeToBeReplaced,
                                                        Collections.singleton(newType))
            self.editingDomain.getCommandStack().execute(replaceInVarCommand)
            self.markAsUnsynched(v)

    #
    # 	 * @param object
    #
    def removeType(self, object_):
        """ generated source for method removeType """
        raise NotImplemented()
        removeCommand = RemoveCommand.create(self.editingDomain, object_.eContainer(),
                                             GeppettoPackage.Literals.GEPPETTO_LIBRARY__TYPES, object_)
        self.editingDomain.getCommandStack().execute(removeCommand)

    #
    # 	 * @param queryPath
    # 	 * @return
    #
    def getQuery(self, queryPath):
        """ generated source for method getQuery """
        raise NotImplemented()
        return ModelUtility.getQuery(queryPath, self.geppettoModel)

    #
    # 	 * @return
    #
    def getQueries(self):
        """ generated source for method getQueries """
        return self.geppettoModel.getQueries()
