class Publisher():
    def __init__(self):
        pass

    def register(self):
        pass

    def unregister(self):
        pass

    def notifyAll(self):\
        pass

class Forum(Publisher):
    def __init__(self):
        self.__listOfUsers = []
        self.postname = None

    def register(self,user):
        if user not in self.__listOfUsers:
            self.__listOfUsers.append(user)

    def unregister(self,user):
        if user in self.__listOfUsers:
            self.__listOfUsers.remove(user)

    def notifyAll(self):
        for user in self.__listOfUsers:
            user.notify(self.postname)

    def newPost(self,postname):
        self.postname = postname
        self.notifyAll()

class Observer:
    def __init__(self):
        pass

    def notify(self):
        pass

class User1(Observer):
    def notify(self,postname):
        print "User1 notified a new post {}".format(postname)

class User2(Observer):
    def notify(self,postname):
        print "User2 notified a new post {}".format(postname)

class Factory():
    def getUser(self,num):
        if num == 1:
            return User1()
        elif num == 2:
            return User2()
        else:
            print "please give factory 1 or 2 to generate user1 or user2"

if __name__ == '__main__':
    forum = Forum()
    factory = Factory()
    user1 = factory.getUser(1)
    user2 = factory.getUser(2)
    forum.register(user1)
    forum.newPost("Hello first idiot")
    forum.register(user2)
    forum.newPost("Hello two idiots")
    forum.unregister(user1)
    forum.newPost("Hello second idiots")
