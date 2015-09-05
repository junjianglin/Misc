# code is borrowed and modified from the book 'python 3 patterns idioms'
class Singleton():
    #use private inner class to delegate a single instance
    class __OnlyOne:
        def __init__(self,val):
            self.val = val
        def __str__(self):
            return  repr(self)+ self.val

    instance = None

    def __init__(self,val):
        if Singleton.instance is None:
            Singleton.instance = Singleton.__OnlyOne(val)
        else:
            Singleton.instance.val = val

    #delegate access to inner class implementation
    def __getattr__(self,name):
        return getattr(self.instance,name)


if __name__ == '__main__':
    x = Singleton('sausage')
    print x
    y = Singleton('eggs')
    print y
    z = Singleton('spam')
    print z

    print x
    print y
    print z


