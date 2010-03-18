from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward
from pyparsing import Literal

from tokens import String, Ident

class Name(BaseModelica):
    __ebnf__ = Forward()
    __ebnf__ << (Ident.__ebnf__.setResultsName("basename") + Optional(Literal(".").suppress() + __ebnf__.setResultsName("names"))).setParseAction(lambda s, l, t: Name(**t))

    basename = Ident("")
    names = []
    def __init__(self, basename, names):
        self.basename = basename
        self.names = names

    def dump(self):
        return "%s.%s"%(self.basename, self.names)

class ClassModification(BaseModelica):
    __ebnf__ = Literal("1")

class StringComment(BaseModelica):
    __ebnf__ = (String.__ebnf__ + ZeroOrMore(Literal("+").suppress() + String.__ebnf__)).setParseAction(lambda s, l, t: StringComment(t))

    comments = []

    def __init__(self, comments):
        self.comments = comments
        
    def dump(self):
        return " + ".join(map(str, self.comments))

class Annotation(BaseModelica):
    __ebnf__ = Literal("annotation") + ClassModification.__ebnf__
