# the code is borrowed and modified from
# www.tutorialspoint.com/design_pattern/abstract_factory_pattern.htm

# The difference between abstract factory and simple factory is that
# abstract factory generate different kinds of object

class Shape():
    def __init__(self):
        pass

class Circle(Shape):
    def __init__(self):
        print "creating Circle"

class Square(Shape):
    def __init__(self):
        print "creating Square"

class Color():
    def __init__(self):
        pass

class Red(Color):
    def __init__(self):
        print "drawing with red"

class Green(Color):
    def __init__(self):
        print "drawing with green"

class AbstractFactory():
    def getShape(self):
        pass
    def getColor(self):
        pass

class Factory(AbstractFactory):
    def getShape(self,type):
        if type == 'Square':
            return Square()
        elif type == 'Circle':
            return Circle()
        else:
            print "not valid Shape"

    def getColor(self,color):
        if color == 'Red':
            return Red()
        elif color == 'Green':
            return Green()
        else:
            print 'invalid color'

if __name__ == '__main__':
    factory = Factory()
    s1 = factory.getShape('Circle')
    s2 = factory.getShape('Square')
    c1 = factory.getColor('Red')
    c2 = factory.getColor('Green')

