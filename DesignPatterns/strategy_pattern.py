#In strategy pattern, a class behavior or its algorithm can be changed at run time.
#For example, a class that performs validation on incoming data may use a strategy pattern to
#select a validation algorithm based on the type of data, the source of data,
#user choice, or other discriminating factors.These factors are not known for each case
#until run-time,and may require radically different validation to be performed.

#The code is borrowed from www.tutorialspoint.com/design_pattern/strategy_pattern.htm

class Strategy:
    """Abstract class concept for readability
    """
    def doAlgo(self,num1,num2):
        raise NotImplementedError("Strategy is supposed to be an abstract class!")

class OperationAdd(Strategy):
    """Concrete strategy class
    """
    def doAlgo(self,num1,num2):
        return num1+num2

class OperationSubstract(Strategy):
    """Concrete strategy class
    """
    def doAlgo(self,num1,num2):
        return num1-num2

class OperationMultiply(Strategy):
    """Concrete strategy class
    """
    def doAlgo(self,num1,num2):
        return num1*num2

class Context():
    """Context class determine which strategy to use
    based on the given input
    """
    def executeStrategy(self,num1,num2,input):
        if input == '+':
            algo = OperationAdd()
            print algo.doAlgo(num1,num2)
        elif input == '-':
            algo = OperationSubstract()
            print algo.doAlgo(num1,num2)
        elif input == '*':
            algo = OperationMultiply()
            print algo.doAlgo(num1,num2)
        else:
            print "invalid input"

if __name__ == '__main__':
    context = Context()
    context.executeStrategy(10,18,'+')
    context.executeStrategy(10,18,'-')
    context.executeStrategy(10,18,'*')
