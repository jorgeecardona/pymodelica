from pyparsing import Word, nums, Literal, ZeroOrMore, alphas, alphanums, QuotedString, Group
from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine
from pyparsing import nums, alphas, alphanums, printables

from string import printable

s_escape = Literal("\\'") ^ "\\\"" ^ "\\?" ^ "\\\\" ^ "\\a" ^ "\\b" ^ "\\f" ^ "\\n" ^ "\\r" ^ "\\t" ^ "\\v"

class QIdent(BaseModelica):
    __ebnf__ = Combine(Literal("'") + CharsNotIn("\\'") + Literal("'")).setParseAction(lambda s, l, t: QIdent(t[0]))

    value = None

    def __init__(self, value= None):
        print value
        if type(value) is str:
            self.value = value
        else:
            raise IncorrectValue("Non-string passed.")

    def dump(self):
        return "'" + self.value + "'"

class Ident(BaseModelica):
    __ebnf__ = (Word(alphas + "_", alphanums + "_").setParseAction(lambda s, l, t: Ident(t[0]))) ^ QIdent.__ebnf__

    value = None

    def __init__(self, value = None):
        if type(value) is str:
            self.value = value
        elif type(value) is QIdent:
            self.value = value.value
        else:
            raise IncorrectValue("Non-string passed.")

    def dump(self):
        return str(self.value)    

class String(BaseModelica):
    __ebnf__ = (Literal('"') + Combine(ZeroOrMore(CharsNotIn("\\\"") ^ s_escape )) + Literal('"')).setParseAction(lambda s, l, t: String(
            t[1].replace("\\\"","\"")
            ))

    value = None

    def __init__(self, value= None):
        if type(value) is str:
            self.value = value
        else:
            raise IncorrectValue("Non-string passed.")

    def dump(self):
        return '"' + self.value + '"'

    
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


class Number(BaseModelica):
    __ebnf__ = (Integer.__ebnf__ + Optional(Literal(".") + Optional(Integer.__ebnf__ ,default = Integer("0"))), default) + Optional((Literal("e") ^ Literal("E")) + Optional(Literal("+") ^ Literal("-")) + Integer.__ebnf__).




if __name__ == '__main__':
    

    print Integer.load("123123")
    print IntegerList.load("123123 , 123123112, 12123123 ,123123,    12312")
