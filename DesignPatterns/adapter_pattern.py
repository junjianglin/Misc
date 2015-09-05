#The Adapter pattern changes the interface of an object in order to match the interface that's expected
#The following code is borrowed and modified from 'ginstrom.com/scribbles/2009/03/27/the-adapter-pattern-in-python/

#Motivation for adapter pattern:
#We are going to start with a simple system, then add components to it with an interface that's different
#from the one our system expects. We'll use the Adapter pattern to wrap the new components,
#so we can use them without chaning the code in our existing system


class Person():
    """ A representation of a person
    """
    def __init__(self,name):
        self.name = name
    def speak(self):
        return "hello"

def click_creature(creature):
    """
    React to a click by retrieving the creature's name and
    what is says
    """
    return creature.name,creature.speak()


class Dog():
    """ A representation of a dog,
        with a different name of speak method,
        but we want to incorporate it into our system
    """
    def __init__(self,name):
        self.name = name

    def bark(self):
        return "woof"

class DogAdapter():
    """ Dog adapter class
    adapts the dog class through encapsulation
    """
    def __init__(self,dog_obj):
        self.dog_obj = dog_obj

    def speak(self):
        return self.dog_obj.bark()

    def __getattr__(self,attr):
        """everything else is delegated to the dog object
        """
        return getattr(self.dog_obj,attr)



if __name__ == '__main__':
    lin = Person("Lin")
    dian = DogAdapter(Dog("Dian"))
    #dian.name = 'dian'
    for creature in (lin,dian):
        print  creature.name ,'says', creature.speak()
