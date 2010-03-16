from pyparsing import Word, nums, Literal, ZeroOrMore, alphas, alphanums, QuotedString, Group
from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, Optional
from pyparsing import nums, alphas, alphanums, printables

from string import printable

s_escape = Literal("\\'") ^ "\\\"" ^ "\\?" ^ "\\\\" ^ "\\a" ^ "\\b" ^ "\\f" ^ "\\n" ^ "\\r" ^ "\\t" ^ "\\v"

def escape(string):
    return string\
        .replace("'", "\\'").\
        .replace("\"", "\\\"")
        
def unescape(string):
    return string\
        .replace("\\'", "'").\
        .replace("\\\"", "\"")


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
            self.value = value
        else:
            raise IncorrectValue("Non-string passed.'")
    
    def dump(self):
        return str(self.value)

class Number(BaseModelica):
    __ebnf__ = (
        Combine(Word(nums) + Optional(Literal(".") + Optional(Word(nums)))).setResultsName('mantissa') + 
        Optional((Literal("e") ^ Literal("E")) + Optional(Literal("+") ^ Literal("-")).setResultsName('exponent_sign') + Word(nums).setResultsName('exponent'))
        ).setParseAction(lambda s,l,t: Number(**dict(t)))

    mantissa = None
    exponent = None
    exponent_sign = None

    def __init__(self, mantissa="0", exponent_sign = "+", exponent = "0"):
        self.mantissa = mantissa
        self.exponent = exponent
        self.exponent_sign = exponent_sign


    def dump(self):
        return self.mantissa + "e" + ("-" if self.exponent_sign == "-" else "") + self.exponent

