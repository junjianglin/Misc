class Singleton():
    #inner class
    class __OnlyOne:
        def __init__(self):
            self.val = None
        def __str__(self):
            return  repr(self)+ self.val

    instance = None

    def __init__(self):
        if Singleton.instance is None:
            Singleton.instance = Singleton.__OnlyOne()

    #delegate access to inner class implementation
    def __getattr__(self,name):
        return getattr(self.instance,name)
    def __setattr__(self,name,value):
        return setattr(self.instance,name,value)


if __name__ == '__main__':
    x = Singleton()
    x.val = 'sausage'
    print x
    y = Singleton()
    y.val = 'eggs'
    print y
    z = Singleton()
    z.val = 'spam'
    print z

    print x
    print y
    print z


