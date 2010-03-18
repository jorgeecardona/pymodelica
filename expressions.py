from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional
from pyparsing import Literal

from tokens import String

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
