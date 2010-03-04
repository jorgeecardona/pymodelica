from pyparsing import Word, nums, Literal, ZeroOrMore

class NonImplemented(Exception):
    pass

class BaseModelica:
    """
    BaseModelica
    ============

    This class is the base of all modelica entities. It has two methods:

    * **load(cls, string)** It creates an element based on the string passed.

    * **dump(self)** It return the element in string modelica format.

    """
    __ebnf__ = None
    
    @classmethod
    def load(cls, string):
        # This reads a string and return the element created.
        return cls.__ebnf__.parseString(string)[0]
    
    def dump(self):
        raise NonImplemented

    def __str__(self):
        return self.dump()

class Integer(BaseModelica):

    __ebnf__ = Word(nums).setParseAction(lambda s, l, t: Integer(t[0]))
    
    value = 0
    
    def __init__(self, value=0):
        if type(value) is str:
            self.value = int(value)
    
    def dump(self):
        return str(self.value)


class IntegerList(BaseModelica):
    __ebnf__ = (Integer.__ebnf__ + ZeroOrMore(Literal(",") + Integer.__ebnf__)).setParseAction(lambda s, l, t: IntegerList(t[::2]))

    def __init__(self, integers = []):
        self.integers = integers

    def dump(self):
        return ", ".join(map(str, self.integers))


print Integer.load("123123")
print IntegerList.load("123123 , 123123112, 12123123 ,123123,    12312")
