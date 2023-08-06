class HelloWorldKeywords(object):
    def __init__(self):
        self.name = "Noname"

    def say_hi(self):
        """ Say hi with out argument
        Examples:
        | Say Hi |
        """
        print("Say hi " + self.name)

    def say_hi2(self, name):
        """ Say hi with a argument.
        `name` Your name
        Examples:
        Say hi   <name>
        | Say Hi | somkiat |
        """
        self.name = name
        print("Say hi " + self.name)
