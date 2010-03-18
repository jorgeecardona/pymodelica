from pyparsing import Word, nums, Literal, alphas, alphanums, QuotedString, Group
from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional
from pyparsing import nums, alphas, alphanums, printables

from string import printable

from decimal import Decimal

s_escape = Literal("\\'") ^ "\\\"" ^ "\\?" ^ "\\\\" ^ "\\a" ^ "\\b" ^ "\\f" ^ "\\n" ^ "\\r" ^ "\\t" ^ "\\v"

def unescape(string):
    return string\
        .replace("\\\"","\"")\
        .replace("\\'","'")\
        .replace("\\\\", "\\")\
        .replace("\\r", chr(13))\
        .replace("\\n", chr(10))\
        .replace("\\t", chr(9))

def escape(string):
    return string\
        .replace("\"","\\\"")\
        .replace("'","\\'")\
        .replace("\\","\\\\")\
        .replace(chr(13),"\\r")\
        .replace(chr(10),"\\n")\
        .replace(chr(9),"\\t")

class QIdent(BaseModelica):
    __ebnf__ = (Literal("'") + Combine(OneOrMore(CharsNotIn("\\'") ^ s_escape )) + Literal("'")).setParseAction(lambda s, l, t: QIdent(t[1]))

    value = None

    def __init__(self, value= None):
        if type(value) is str:
            self.value = value
        else:
            raise IncorrectValue("Non-string passed.")

    def dump(self):
        return "'" + self.value + "'"

class Ident(BaseModelica):
    __ebnf__ = (Word(alphas + "_", alphanums + "_") ^ QIdent.__ebnf__).setParseAction(lambda s, l, t: Ident(t[0]))

    value = None

    def __init__(self, value = None):

        if type(value) is str:
            self.value = value

        elif type(value) is QIdent:
            self.value = value.dump()

        else:
            print value
            raise IncorrectValue("Non-string or QIdent passed.")

    def dump(self):
        return str(self.value)    

class String(BaseModelica):
    __ebnf__ = (Literal('"') + Combine(ZeroOrMore(CharsNotIn("\\\"") ^ s_escape )) + Literal('"')).setParseAction(lambda s, l, t: String(
            t[1]
            ))

    value = None

    def __init__(self, value= None):
        # Receive a string with the escaping elements.
        value = unescape(value)
        
        if type(value) is str:
            self.value = value
        else:
            raise IncorrectValue("Non-string passed.")

    def dump(self):
        return '"' + escape(self.value) + '"'

    
class Integer(BaseModelica):
    __ebnf__ = Word(nums).setParseAction(lambda s, l, t: Integer(t[0]))
    
    def __init__(self, value=0):
        if type(value) is str:
            self.value = Decimal(value)
        else:
            raise IncorrectValue("Non-string passed.'")
    
    def dump(self):
        return str(self.value)

class Number(BaseModelica):
    __ebnf__ = (
        Combine(Word(nums) + Optional(Literal(".") + Optional(Word(nums)))).setResultsName('mantissa') + 
        Optional((Literal("e") ^ Literal("E")) + Optional(Literal("+") ^ Literal("-")).setResultsName('exponent_sign') + Word(nums).setResultsName('exponent'))
        ).setParseAction(lambda s,l,t: Number(**dict(t)))

    mantissa = Decimal(0)
    exponent = Decimal(0)

    def __init__(self, mantissa="0", exponent_sign = "+", exponent = "0"):

        self.mantissa = Decimal(mantissa)
        self.exponent = Decimal(exponent)

        if exponent_sign is "-":
            self.exponent = -self.exponent


    def dump(self):
        return str(self.mantissa) + (("e" + str(self.exponent)) if self.exponent !=Decimal(0) else "")

