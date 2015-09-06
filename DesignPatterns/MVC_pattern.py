#Model-View-Control

#the code is borrowed and modified from tutorialspoint


class Student():
    """Model class"""
    def __init__(self,rollNum,name):
        self.rollNum = rollNum
        self.name = name


class StudentView():
    """View class
    processes output
    """
    def printDetails(self,student):
        print "Student",student.name, student.rollNum

class StudentController():
    """Controller class
    control the main workflow and algorithm
    """
    def __init__(self,model,view):
        self.model = model
        self.view = view

    def setName(self,name):
        self.model.name = name

    def setRollNo(self,rollNo):
        self.model.rollNum = rollNo

    def updateView(self):
        self.view.printDetails(self.model)

if __name__ == '__main__':
    model = Student(1,'lin')
    view = StudentView()
    control = StudentController(model,view)
    control.updateView()
    control.setName('dian')
    control.updateView()
    control.setRollNo(4)
    control.updateView()

