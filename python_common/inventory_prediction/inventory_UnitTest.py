import unittest
from inventory_prediction import * # code from module you're testing


class OrderTestCase(unittest.TestCase):

	def setUp(self):
	    """Call before every test case."""
            from datetime import datetime
	    self.order = Order(datetime.today(),"Beijing",'toy',5,3)

	def tearDown(self):
	    """Call after every test case."""
	    del self.order

	def testGetName(self):
	    """Test case A. note that all test method names must begin with 'test.'"""
            pass
	def testGetSalary(self):
	    """test case B"""
            pass
class OtherTestCase(unittest.TestCase):

	def setUp(self):
            pass
	def tearDown(self):
            pass
	def testGetEmpCount(self):
	    """ getEmpCount() is a static method """
            pass
	def testNothing(self):
	    pass


if __name__ == "__main__":
	unittest.main() # run all tests
