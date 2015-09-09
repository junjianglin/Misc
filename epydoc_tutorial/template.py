"""
@author: JunjiangLin
@date: 2015/09/11
"""

import math

class Vechicle():
    """ A vechicle class
    We define this class for fun
    @param name: name of the vechicle
    @param numWheels: number of wheels
    """

    def __init__(self,name,numWheels):
        """constructor of Vechicle"""
        self.name = name
        self.numWheels = numWheels

    def getName(self):
        """return the name of vechicle
        @return: the name
        """
        return self.name

    def getWheelMulti(self,num):
        """calculate num of wheels * num.
        Nothing complicated, I just want to type more
        sentences to see result.
        @param num: the multipler to multipy
        @return: the result
        """
        return self.numWheels*num

class Car(Vechicle):
    """Inherited from Vechicle
    @param model: model of the car
    """
    def __init__(self,name,model):
        """Constructor for car"""
        Vechicle.__init__(self,name,4)
        self.model = model

    def getModelAndName(self):
        """return a string of model and name
        @return: a string of model and name
        """
        return self.model + " " + self.name

if __name__ == '__main__':
    car = Car('lin','bmw')
    print car.getModelAndName()

