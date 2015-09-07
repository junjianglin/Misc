import unittest
from Employee_class import Employee # code from module you're testing


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
	"""Call before every test case."""
	self.emp = Employee('Lin',10000)
	self.emp2 = Employee('Jun',20000)

    def tearDown(self):
	"""Call after every test case."""
	del self.emp
	del self.emp2

    def testGetName(self):
	"""Test case A. note that all test method names must begin with 'test.'"""
	self.assertEqual(self.emp.getName(),'Lin')  # test getName() whether return correct answer"
	self.assertNotEqual(self.emp2.getName(),'Lin')

    def testGetSalary(self):
	"""test case B"""
	self.assertEqual(self.emp2.getSalary(),20000)   # test getSalary() whether return correct answer
	self.assertNotEqual(self.emp.getSalary(),20000)

class OtherTestCase(unittest.TestCase):

    def setUp(self):
	self.emp3 = Employee('jiang',30000)

    def tearDown(self):
	del self.emp3

    def testGetEmpCount(self):
	""" getEmpCount() is a static method """
	self.assertEqual(Employee.getEmpCount(),1)    # test getEmpCount() whether return correct answer

    def testNothing(self):
	pass


if __name__ == "__main__":
	unittest.main() # run all tests
