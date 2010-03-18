from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward
from pyparsing import Literal

from tokens import String, Ident

class Name(BaseModelica):
    __ebnf__ = (Ident.__ebnf__ + ZeroOrMore(Literal(".").suppress() + Ident.__ebnf__)).setParseAction(lambda s, l, t: Name(list(t)))

    names = []
    def __init__(self, names):
        self.names = names

    def dump(self):
        return ".".join(map(str, self.names))

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
