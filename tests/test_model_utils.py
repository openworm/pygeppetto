import os
import unittest

from pyecore.resources import ResourceSet, URI
from pygeppetto.model.utils.pointer_utility import PointerUtility, GeppettoModelException


class PointerUtilityTest(unittest.TestCase):

    # def setUp(self):
    #     self.model_interpreter = TestModelInterpreter()
    #     self.geppetto_model = self.model_interpreter.importType()
    #
    # def test_find_value(self):
    #     value = PointerUtility.get_value('v1')
    #     self.assertEqual(type(value, ImportType))
    #
    #     value = PointerUtility.get_value('v2')
    #     self.assertEqual(type(value, StateVariableType))
    #
    #     value = PointerUtility.get_value('v3.')
    #     self.assertEqual(type(value, StateVariableType))

    @classmethod
    def setUpClass(cls):
        """ generated source for method setUp """

        #  sets the factory for the XMI type
        resSet = ResourceSet()
        #  How to read
        resource = resSet.get_resource(URI(os.path.join(os.path.dirname(__file__), "xmi-data/GeppettoModelTest2.xmi")))

        cls.geppettoModel = resource.contents[0]

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointer(self):
        """ generated source for method testGetPointer """
        # None of these should throw an exception
        # PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].name(genericParameter)")
        # PointerUtility.getPointer(self.geppettoModel, "addressBook")
        # PointerUtility.getPointer(self.geppettoModel, "addressBook[6]")
        # PointerUtility.getPointer(self.geppettoModel,
        #                           "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
        PointerUtility.getPointer(self.geppettoModel, "addressBook[30].address.zone[4].area")
        PointerUtility.getPointer(self.geppettoModel, "sample.person.name")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testEquals(self):
        """ generated source for method testEquals """
        p1 = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].name(genericParameter)")
        p2 = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].name(genericParameter)")
        self.assertIsNot(p1, p2)
        self.assertEqual("addressBook(addressBook)[3].name(genericParameter)", p1.getInstancePath())
        self.assertEqual(p1.getInstancePath(), p2.getInstancePath())
        self.assertTrue(PointerUtility.equals(p1, p2))
        p3 = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3]")
        self.assertIsNot(p1, p3)
        self.assertFalse(PointerUtility.equals(p1, p3))
        p4 = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].address(address)")
        self.assertIsNot(p1, p3)
        self.assertFalse(PointerUtility.equals(p1, p4))
        self.assertFalse(PointerUtility.equals(p3, p4))

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative1(self):
        """ generated source for method testGetPointerNegative1 """

        with self.assertRaises(GeppettoModelException):
            PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBok)[3].name(genericParameter)")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative2(self):
        """ generated source for method testGetPointerNegative2 """
        with self.assertRaises(GeppettoModelException):
            PointerUtility.getPointer(self.geppettoModel, "addresBook")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative3(self):
        """ generated source for method testGetPointerNegative3 """
        with self.assertRaises(GeppettoModelException):
            PointerUtility.getPointer(self.geppettoModel, "addressBook6]")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative4(self):
        """ generated source for method testGetPointerNegative4 """
        with self.assertRaises(GeppettoModelException):
            PointerUtility.getPointer(self.geppettoModel,
                                      "addressBook(addressBook)[30]address(address).zone(zone)[4].area(genericParameter)")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative5(self):
        """ generated source for method testGetPointerNegative5 """
        with self.assertRaises(Exception):
            PointerUtility.getPointer(self.geppettoModel, "addressBook[30].address.zone[].area")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative6(self):
        """ generated source for method testGetPointerNegative6 """
        with self.assertRaises(GeppettoModelException):
            PointerUtility.getPointer(self.geppettoModel, "addressBook[30].address.zone[2].arrea")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getPointer(org.geppetto.model.GeppettoModel, java.lang.String)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetPointerNegative7(self):
        """ generated source for method testGetPointerNegative7 """
        with self.assertRaises(GeppettoModelException):
            PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBok)[3].")

    #
    # 	 * Test method for {@link org.geppetto.model.util.PointerUtility#getVariable(org.geppetto.model.values.Pointer)}.
    # 	 *
    # 	 * @throws GeppettoModelException
    #
    def testGetVariable(self):
        """ generated source for method testGetVariable """
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].name(genericParameter)")
        self.assertEqual("name", PointerUtility.getVariable(p).id)
        self.assertEqual("name", PointerUtility.getVariable(p).name)
        self.assertEqual("genericParameter", PointerUtility.getVariable(p).types[0].id)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook")
        self.assertEqual("addressBook", PointerUtility.getVariable(p).id)
        self.assertEqual("addressBook", PointerUtility.getVariable(p).name)
        self.assertEqual("addressBook", PointerUtility.getVariable(p).types[0].id)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook[6]")
        self.assertEqual("addressBook", PointerUtility.getVariable(p).id)
        self.assertEqual("addressBook", PointerUtility.getVariable(p).name)
        self.assertEqual("addressBook", PointerUtility.getVariable(p).types[0].id)
        self.assertEqual(int(6), p.getElements()[0].index)
        p = PointerUtility.getPointer(self.geppettoModel,
                                      "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
        self.assertEqual("area", PointerUtility.getVariable(p).id)
        self.assertEqual("area", PointerUtility.getVariable(p).name)
        self.assertEqual("genericParameter", PointerUtility.getVariable(p).types[0].id)
        self.assertEqual(int(30), p.getElements()[0].index)
        self.assertEqual(int(-1), p.getElements()[1].index)
        self.assertEqual(int(4), p.getElements()[2].index)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook[30].address.zone[4].area")
        self.assertEqual("area", PointerUtility.getVariable(p).id)
        self.assertEqual("area", PointerUtility.getVariable(p).name)
        self.assertEqual("genericParameter", PointerUtility.getVariable(p).types[0].id)
        self.assertEqual(int(30), p.getElements()[0].index)
        self.assertEqual(int(-1), p.getElements()[1].index)
        self.assertEqual(int(4), p.getElements()[2].index)

    def testGetType(self):
        """ generated source for method testGetType """
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].name(genericParameter)")
        self.assertEqual("genericParameter", PointerUtility.getType(p).id)
        self.assertEqual("genericParameter", PointerUtility.getType(p).name)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook")
        self.assertEqual("addressBook", PointerUtility.getType(p).id)
        self.assertEqual("addressBook", PointerUtility.getType(p).name)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook[6]")
        self.assertEqual("addressBook", PointerUtility.getType(p).id)
        self.assertEqual("addressBook", PointerUtility.getType(p).name)
        self.assertEqual(int(6), p.getElements()[0].index)
        p = PointerUtility.getPointer(self.geppettoModel,
                                      "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
        self.assertEqual("genericParameter", PointerUtility.getType(p).id)
        self.assertEqual("genericParameter", PointerUtility.getType(p).name)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook[30].address.zone[4].area")
        self.assertEqual("genericParameter", PointerUtility.getType(p).id)
        self.assertEqual("genericParameter", PointerUtility.getType(p).name)

    def testGetGeppettoLibrary(self):
        """ generated source for method testGetGeppettoLibrary """
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook(addressBook)[3].name(genericParameter)")
        self.assertEqual("sample", PointerUtility.getGeppettoLibrary(p).id)
        self.assertEqual("sample", PointerUtility.getGeppettoLibrary(p).id)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook[6]")
        self.assertEqual("sample", PointerUtility.getGeppettoLibrary(p).id)
        p = PointerUtility.getPointer(self.geppettoModel,
                                      "addressBook(addressBook)[30].address(address).zone(zone)[4].area(genericParameter)")
        self.assertEqual("sample", PointerUtility.getGeppettoLibrary(p).id)
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook[30].address.zone[4].area")
        self.assertEqual("sample", PointerUtility.getGeppettoLibrary(p).id)

    def testGetInstancePath(self):
        """ generated source for method testGetInstancePath """
        p = PointerUtility.getPointer(self.geppettoModel, "addressBook")
        self.assertEqual("addressBook(addressBook)",
                         PointerUtility.getInstancePath(PointerUtility.getVariable(p),
                                                        PointerUtility.getType(p)))
