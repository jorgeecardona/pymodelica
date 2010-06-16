from string import printable
from decimal import Decimal
from pyparsing import nums, alphas, alphanums
from pyparsing import Word, Literal, Suppress, OneOrMore, CharsNotIn, Combine, Optional

from base import BaseModelica as ModelicaBase

class IDENT(ModelicaBase):
    def __init__(self, value):
        if isinstance(value, (unicode, str)):
            if value.strip() != value:
                raise Exception("White spaces")
            self.value = unicode(value)
        elif isinstance(value, QIDENT):
            self.value = value
        else:
            raise Exception("Non string value")

    def dump(self):
        return "%s" % (self.value)

    def __lt__(self, o):
        return self.value < o.value

    def __le__(self, o):
        return self.value <= o.value

    def __gt__(self, o):
        return self.value > o.value

    def __ge__(self, o):
        return self.value >= o.value

    def __eq__(self, o):
        return self.value == o.value

    def __ne__(self, o):
        return self.value != o.value

class QIDENT(ModelicaBase):
    def __init__(self, value):
        if isinstance(value, (unicode, str)):
            
            self.value = unicode(value)
        else:
            raise Exception("Non string value")

    def dump(self):
        return "'%s'" % (self.value)

    def __lt__(self, o):
        return self.value < o.value

    def __le__(self, o):
        return self.value <= o.value

    def __gt__(self, o):
        return self.value > o.value

    def __ge__(self, o):
        return self.value >= o.value

    def __eq__(self, o):
        return self.value == o.value

    def __ne__(self, o):
        return self.value != o.value
            
class STRING(ModelicaBase):
    def __init__(self, value):
        if isinstance(value, (str, unicode)):
            self.value = value
            return

        raise Exception("Non string value")

    def dump(self):
        return "\"%s\"" % (self.value)

    def unescape(self):
        val = self.value
        val = val.replace("\\\"", "\"")
        val = val.replace("\\'", "'")
        val = val.replace("\\\\", "\\")
        val = val.replace("\\r", chr(13))
        val = val.replace("\\n", chr(10))
        val = val.replace("\\t", chr(9))        
        return val


class UNSIGNED_INTEGER(ModelicaBase):
    def __init__(self, value):
        self.value = Decimal(value)

    def dump(self):
        return "%s" % (self.value)

class UNSIGNED_NUMBER(ModelicaBase):
    def __init__(self, mantissa="0", exponent_sign = "+", exponent = "0"):
        self.mantissa = Decimal(mantissa)
        self.exponent = Decimal(exponent)
        if exponent_sign is "-":
            self.exponent = -self.exponent
        
    def dump(self):
        exponent = ("e%s" % (self.exponent)) if self.exponent != 0 else ""
        return "%s%s" % (self.mantissa, exponent)

NONDIGIT = alphas + '_'
DIGIT = nums
SCHAR = CharsNotIn("\\\"")
QCHAR = Word(alphanums + "!#$%&()*+,-./:;<>=?@[]^{}|~ ")
SESCAPE = Literal("\\'") ^ Literal("\\\"") ^ Literal("\\?") ^\
    Literal("\\") ^ Literal("\\a") ^ Literal("\\b") ^\
    Literal("\\f") ^ Literal("\\n") ^ Literal("\\r") ^\
    Literal("\\t") ^ Literal("\\v")

IDENT.ebnf(
    syntax=Word(NONDIGIT , DIGIT + NONDIGIT) ^ QIDENT.ebnf(),
    action=lambda s,l,t: IDENT(t[0])
    )

QIDENT.ebnf(
    syntax=Suppress("'") + OneOrMore(QCHAR ^ SESCAPE) + Suppress("'"),
    action=lambda s,l,t: QIDENT(t[0])
    )

STRING.ebnf(
    syntax=Suppress('"') + Combine(OneOrMore(SCHAR ^ SESCAPE)) + Suppress('"'),
    action=lambda s,l,t: STRING(t[0])
    )

UNSIGNED_INTEGER.ebnf(
    syntax=Word(nums),
    action=lambda s,l,t: UNSIGNED_INTEGER(t[0])
    )

UNSIGNED_NUMBER.ebnf(
    syntax = Combine(UNSIGNED_INTEGER.ebnf() + Optional(Literal(".") + Optional(UNSIGNED_INTEGER.ebnf()))).setResultsName("mantissa") + Optional((Literal("e") ^ Literal("E")) + Optional(Literal("+") ^ Literal("-")).setResultsName('exponent_sign') + Combine(UNSIGNED_INTEGER.ebnf()).setResultsName('exponent')),
    action=lambda s,l,t: UNSIGNED_NUMBER(**dict(t))
    )
