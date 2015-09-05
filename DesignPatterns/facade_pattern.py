import time

class TC1():
    """TestCase1
    """
    def run(self):
        print "#### In Test1 ####"
        time.sleep(1)
        print"Setting up"
        time.sleep(1)
        print "Running Test Case1"
        time.sleep(1)
        print "Tearing down Test1"

class TC2():
    """TestCase2
    """
    def run(self):
        print "#### In Test2 ####"
        time.sleep(1)
        print"Setting up"
        time.sleep(1)
        print "Running Test Case2"
        time.sleep(1)
        print "Tearing down Test2"

class TC3():
    """TestCase3
    """
    def run(self):
        print "#### In Test3 ####"
        time.sleep(1)
        print"Setting up"
        time.sleep(1)
        print "Running Test Case3"
        time.sleep(1)
        print "Tearing down Test3"

#Facade class to run all testcases
class TestRunner():
    """TestRunner class
    A simplied interface to all
    TestCase classes
    """
    def __init__(self):
        self.tc = [TC1(),TC2(),TC3()]

    def runAll(self):
        for tc in self.tc:
            tc.run()


if __name__ == '__main__':
    tr = TestRunner()
    tr.runAll()
