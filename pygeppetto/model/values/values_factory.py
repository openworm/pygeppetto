from .values import *
from ..exceptions import IllegalArgumentException


# package: org.geppetto.model.values.
#
#  * <!-- begin-user-doc -->
#  * An ementation of the model <b>Factory</b>.
#  * <!-- end-user-doc -->
#  * @generated
#
class EFactory: pass


class ValuesFactory(EFactory):
    eINSTANCE = None

    """ generated source for class ValuesFactory """

    #
    # 	 * Creates the default factory ementation.
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    # @classmethod
    # def init(cls):
    #     """ generated source for method init """
    #     try:
    #         theValuesFactory = EPackage.Registry.INSTANCE.getEFactory(ValuesPackage.eNS_URI)
    #         if theValuesFactory != None:
    #             return theValuesFactory
    #     except Exception as exception:
    #         EcorePlugin.INSTANCE.log(exception)
    #     return ValuesFactory()

    #
    # 	 * Creates an instance of the factory.
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def __init__(self):
        """ generated source for method __init__ """
        super(ValuesFactory, self).__init__()

    #
    #
    # #
    # # 	 * <!-- begin-user-doc -->
    # # 	 * <!-- end-user-doc -->
    # # 	 * @generated
    # #
    # def createFromString(self, eDataType, initialValue):
    #     """ generated source for method createFromString """
    #     if eDataType.getClassifierID() == ValuesPackage.CONNECTIVITY:
    #         return self.createConnectivityFromString(eDataType, initialValue)
    #     elif eDataType.getClassifierID() == ValuesPackage.IMAGE_FORMAT:
    #         return self.createImageFormatFromString(eDataType, initialValue)
    #     else:
    #         raise IllegalArgumentException("The datatype '" + eDataType.__name__ + "' is not a valid classifier")
    #
    # #
    # # 	 * <!-- begin-user-doc -->
    # # 	 * <!-- end-user-doc -->
    # # 	 * @generated
    # #
    # def convertToString(self, eDataType, instanceValue):
    #     """ generated source for method convertToString """
    #     if eDataType.getClassifierID() == ValuesPackage.CONNECTIVITY:
    #         return self.convertConnectivityToString(eDataType, instanceValue)
    #     elif eDataType.getClassifierID() == ValuesPackage.IMAGE_FORMAT:
    #         return self.convertImageFormatToString(eDataType, instanceValue)
    #     else:
    #         raise IllegalArgumentException("The datatype '" + eDataType.__name__ + "' is not a valid classifier")

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createComposite(self):
        """ generated source for method createComposite """
        composite = Composite()
        return composite

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createStringToValueMap(self):
        """ generated source for method createStringToValueMap """
        stringToValueMap = StringToValueMap()
        return stringToValueMap

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createQuantity(self):
        """ generated source for method createQuantity """
        quantity = Quantity()
        return quantity

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createPhysicalQuantity(self):
        """ generated source for method createPhysicalQuantity """
        physicalQuantity = PhysicalQuantity()
        return physicalQuantity

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createUnit(self):
        """ generated source for method createUnit """
        unit = Unit()
        return unit

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createTimeSeries(self):
        """ generated source for method createTimeSeries """
        timeSeries = TimeSeries()
        return timeSeries

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createMDTimeSeries(self):
        """ generated source for method createMDTimeSeries """
        # TODO implement MDTimeSeries
        raise NotImplementedError()
        # mdTimeSeries = MDTimeSeries()
        # return mdTimeSeries

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createText(self):
        """ generated source for method createText """
        text = Text()
        return text

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createURL(self):
        """ generated source for method createURL """
        url = URL()
        return url

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createHTML(self):
        """ generated source for method createHTML """
        html = HTML()
        return html

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createPointer(self) -> Pointer:
        """ generated source for method createPointer """
        pointer = Pointer()
        return pointer

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createPointerElement(self):
        """ generated source for method createPointerElement """
        pointerElement = PointerElement()
        return pointerElement

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createPoint(self):
        """ generated source for method createPoint """
        point = Point()
        return point

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createDynamics(self):
        """ generated source for method createDynamics """
        dynamics = Dynamics()
        return dynamics

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createFunctionPlot(self):
        """ generated source for method createFunctionPlot """
        functionPlot = FunctionPlot()
        return functionPlot

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createFunction(self):
        """ generated source for method createFunction """
        function_ = Function()
        return function_

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createArgument(self):
        """ generated source for method createArgument """
        argument = Argument()
        return argument

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createExpression(self):
        """ generated source for method createExpression """
        expression = Expression()
        return expression

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createCollada(self):
        """ generated source for method createCollada """
        collada = Collada()
        return collada

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createOBJ(self):
        """ generated source for method createOBJ """
        obj = OBJ()
        return obj

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createSphere(self):
        """ generated source for method createSphere """
        sphere = Sphere()
        return sphere

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createCylinder(self):
        """ generated source for method createCylinder """
        cylinder = Cylinder()
        return cylinder

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createParticles(self):
        """ generated source for method createParticles """
        # TODO implement Particles
        raise NotImplementedError()
        # particles = Particles()
        # return particles

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createSkeletonAnimation(self):
        """ generated source for method createSkeletonAnimation """
        skeletonAnimation = SkeletonAnimation()
        return skeletonAnimation

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createSkeletonTransformation(self):
        """ generated source for method createSkeletonTransformation """
        skeletonTransformation = SkeletonTransformation()
        return skeletonTransformation

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createVisualGroupElement(self):
        """ generated source for method createVisualGroupElement """
        visualGroupElement = VisualGroupElement()
        return visualGroupElement

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createVisualGroup(self):
        """ generated source for method createVisualGroup """
        visualGroup = VisualGroup()
        return visualGroup

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createConnection(self):
        """ generated source for method createConnection """
        connection = Connection()
        return connection

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createArrayElement(self):
        """ generated source for method createArrayElement """
        arrayElement = ArrayElement()
        return arrayElement

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createArrayValue(self):
        """ generated source for method createArrayValue """
        arrayValue = ArrayValue()
        return arrayValue

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createImage(self):
        """ generated source for method createImage """
        image = Image()
        return image

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createImportValue(self):
        """ generated source for method createImportValue """
        importValue = ImportValue()
        return importValue

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createConnectivityFromString(self, eDataType, initialValue):
        """ generated source for method createConnectivityFromString """
        result = Connectivity.get(initialValue)
        if result == None:
            raise IllegalArgumentException(
                "The value '" + initialValue + "' is not a valid enumerator of '" + eDataType.__name__ + "'")
        return result

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def convertConnectivityToString(self, eDataType, instanceValue):
        """ generated source for method convertConnectivityToString """
        return None if instanceValue == None else instanceValue.__str__()

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def createImageFormatFromString(self, eDataType, initialValue):
        """ generated source for method createImageFormatFromString """
        result = ImageFormat.get(initialValue)
        if result == None:
            raise IllegalArgumentException(
                "The value '" + initialValue + "' is not a valid enumerator of '" + eDataType.__name__ + "'")
        return result

    #
    # 	 * <!-- begin-user-doc -->
    # 	 * <!-- end-user-doc -->
    # 	 * @generated
    #
    def convertImageFormatToString(self, eDataType, instanceValue):
        """ generated source for method convertImageFormatToString """
        return None if instanceValue == None else instanceValue.__str__()


ValuesFactory.eINSTANCE = ValuesFactory()
