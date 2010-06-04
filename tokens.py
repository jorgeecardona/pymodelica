#from pyparsing import Word, nums, Literal, alphas, alphanums, QuotedString, Group
#from base import BaseModelica, IncorrectValue, NonImplemented

#from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Suppress
#from pyparsing import nums, alphas, alphanums, printables

#from string import printable

#from decimal import Decimal

#s_escape = Literal("\\'") ^ "\\\"" ^ "\\?" ^ "\\\\" ^ "\\a" ^ "\\b" ^ "\\f" ^ "\\n" ^ "\\r" ^ "\\t" ^ "\\v"

# def unescape(string):
#     return string\
#         .replace("\\\"","\"")\
#         .replace("\\'","'")\
#         .replace("\\\\", "\\")\
#         .replace("\\r", chr(13))\
#         .replace("\\n", chr(10))\
#         .replace("\\t", chr(9))

# def escape(string):
#     return string\
#         .replace("\"","\\\"")\
#         .replace("'","\\'")\
#         .replace("\\","\\\\")\
#         .replace(chr(13),"\\r")\
#         .replace(chr(10),"\\n")\
#         .replace(chr(9),"\\t")

# class QIdent(BaseModelica):

#     def __init__(self, value= None):
#         if type(value) is str:
#             self.value = value
#         else:
#             raise IncorrectValue("Non-string passed.")

#     def dump(self):
#         return "'" + self.value + "'"

# class Ident(BaseModelica):
#     def __init__(self, value=None):
#         if isinstance(value, (str, QIdent)):
#             self.value = str(value)
#         else:
#             raise Exception("Non-string or QIdent passed.")

#     def dump(self, indent = 0):
#         return str(self.value)    

#     def __repr__(self):
#         return "IDENT: %s"%str(self)


# class String(BaseModelica):
#     def __init__(self, value=None):
#         # Receive a string with the escaping elements.
        
#         if type(value) is str:
#             self.value = value
#         else:
#             raise IncorrectValue("Non-string passed.")

#     def dump(self):
#         return '"' + escape(self.value) + '"'
                
# class Integer(BaseModelica):
#     __ebnf__ = Word(nums).setParseAction(lambda s, l, t: Integer(t[0]))
    
#     def __init__(self, value=0):
#         if type(value) is str:
#             self.value = Decimal(value)
#         else:
#             raise IncorrectValue("Non-string passed.'")
    
#     def dump(self):
#         return str(self.value)

#     def __repr__(self):
#         return "INTEGER: %s"%str(self)

# class Number(BaseModelica):

#     mantissa = Decimal(0)
#     exponent = Decimal(0)

#     def __init__(self, mantissa="0", exponent_sign = "+", exponent = "0"):

#         self.mantissa = Decimal(mantissa)
#         self.exponent = Decimal(exponent)

#         if exponent_sign is "-":
#             self.exponent = -self.exponent


#     def dump(self):
#         return str(self.mantissa) + (("e" + str(self.exponent)) if self.exponent !=Decimal(0) else "")


#     def __repr__(self):
#         return "NUMBER: %s"%str(self)


# # EBNF Syntax here.

# # IDENT Syntax and action
# Ident.ebnf(
#     syntax = Word(alphas + "_", alphanums + "_") ^ QIdent.ebnf(),

#     action = lambda s, l, t: Ident(t[0])
#     )

# # QIDENT Syntax and action
# QIdent.ebnf(
#     syntax = (
#         Suppress("'") + 
#         Combine(OneOrMore(CharsNotIn("\\'") ^ s_escape )) + 
#         Suppress("'")
#         ),

#     action = lambda s, l, t: QIdent(t[0])
#     )

# String.ebnf(
#     syntax = (
#         Suppress('"') + 
#         Combine(ZeroOrMore(CharsNotIn("\\\"") ^ s_escape )) +
#         Suppress('"')
#         ),
    
#     action = lambda s, l, t: String(t[0])
#     )

# Number.ebnf(
#     syntax = (
#         Combine(Word(nums) + Optional(Literal(".") + Optional(Word(nums)))).setResultsName('mantissa') + 
#         Optional((Literal("e") ^ Literal("E")) + Optional(Literal("+") ^ Literal("-")).setResultsName('exponent_sign') + Word(nums).setResultsName('exponent'))
#         ).setParseAction(lambda s,l,t: Number(**dict(t)))

#     syntax = 

from pyparsing import Word, nums, alphas, Suppress, OneOrMore, CharsNotIn
from base import BaseModelica as ModelicaBase

class IDENT(ModelicaBase):
    def __init__(self, value):
        if isinstance(value, (unicode, str)):
            if value == value.strip():
                self.value = unicode(value)
                return
            
        raise Exception("Non string value")

    def dump(self):
        return "%s" % (self.value)

class QIDENT(ModelicaBase):
    def __init__(self, value):
        if isinstance(value, (unicode, str)):
            if (value[0] == value[-1] == "'"):
                self.value = unicode(value[1:-1])
                return

        raise Exception("Non string value")

    def dump(self):
        return "'%s'" % (self.value)
            

class NONDIGIT:
    pass

class STRING:
    pass

class SCHAR:
    pass

class QCHAR:
    pass

class SESCAPE:
    pass

class DIGIT:
    pass

class UNSIGNED_INTEGER:
    pass

class UNSIGNED_NUMBER:
    pass

NONDIGIT = alphas + '_'
DIGIT = nums

IDENT.ebnf(
    syntax=Word(NONDIGIT , DIGIT + NONDIGIT) ^ QIDENT.ebnf(),
    action=lambda s,l,t: IDENT(t[0])
    )

QIDENT.ebnf(
    syntax=Suppress("'") + OneOrMore(CharsNotIn('\\"')) + Suppress("'"),
    action=lambda s,l,t: QIDENT(t[0])
    )

# EBNF Syntax and action
