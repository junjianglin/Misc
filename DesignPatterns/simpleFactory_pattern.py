#code are borrowed and modified from the book 'Design Patterns in Python ver0.1'

class Person():
    """Person class
    Superclass of Male and Female
    Attributes:
        name: the name of person
        gender: either male or female
    """
    def __init__(self):
        self.name = None
        self.gender = None

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

class Male(Person):
    """Male class
    Subclass of Person
    """
    def __init__(self,name):
        print 'Hello Mr.' + name

class Female(Person):
    """Female class
    subclass of Person
    """
    def __init__(self,name):
        print 'Morning, Miss.' + name

class Factory():
    """Factory class
    generate class object according to user's input
    """
    def getPerson(self,name,gender):
        if gender.upper() == 'M':
            return Male(name)
        elif gender.upper() == 'F':
            return Female(name)
        else:
            print 'gender must be M or F'

if __name__ == '__main__':
    factory = Factory()
    Lin = factory.getPerson('Lin','M')
    Dian = factory.getPerson('Dian','F')
    some = factory.getPerson('aa','N')
