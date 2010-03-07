from pyparsing import Word, nums, Literal, ZeroOrMore, alphas, alphanums
from base import BaseModelica, IncorrectValue, NonImplemented


class Ident(BaseModelica):
    __ebnf__ = Word(alphas + "_", alphanums + "_").setParseAction(lambda s, l, t: Ident(t[0]))

    value = None

    def __init__(self, value = None):
        if type(value) is str:
            self.value = value
        else:
            raise IncorrectValue("Non-string passed.")

    def dump(self):
        return str(self.value)

class Integer(BaseModelica):
    __ebnf__ = Word(nums).setParseAction(lambda s, l, t: Integer(t[0]))
    
    def __init__(self, value=0):
        if type(value) is str:
            self.value = int(value)
        else:
            raise IncorrectValue("Non-string passed.'")
    
    def dump(self):
        return str(self.value)


class IntegerList(BaseModelica):
    __ebnf__ = (Integer.__ebnf__ + ZeroOrMore(Literal(",") + Integer.__ebnf__)).setParseAction(lambda s, l, t: IntegerList(t[::2]))

    def __init__(self, integers = []):
        self.integers = integers

    def dump(self):
        return ", ".join(map(str, self.integers))


if __name__ == '__main__':
    

    print Integer.load("123123")
    print IntegerList.load("123123 , 123123112, 12123123 ,123123,    12312")
