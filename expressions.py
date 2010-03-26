from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward
from pyparsing import Literal

from tokens import String, Ident

class Name(BaseModelica):
    # EBNF Section
    __ebnf__ = Ident.__ebnf__ + ZeroOrMore(Literal(".").suppress() + Ident.__ebnf__)
    __ebnf__ = __ebnf__.setParseAction(lambda s, l, t: Name(list(t)))

    # Internal data
    names = []

    def __init__(self, names):
        self.names = names

    def dump(self):
        return ".".join(map(str, self.names))

class ClassModification(BaseModelica):
    __ebnf__ = Literal("1")

class StringComment(BaseModelica):
    # EBNF Section
    __ebnf__ = String.__ebnf__ + ZeroOrMore(Literal("+").suppress() + String.__ebnf__)
    __ebnf__ = __ebnf__.setParseAction(lambda s, l, t: StringComment(t))

    # Internal data
    comments = []

    def __init__(self, comments):
        self.comments = comments
        
    def dump(self, indent = 0):
        return " + ".join(map(str, self.comments))



class Annotation(BaseModelica):
    __ebnf__ = Literal("annotation") + ClassModification.__ebnf__



class Comment(BaseModelica):
    #EBNF Section
    __ebnf__ = StringComment.__ebnf__.setResultsName("comment") + Optional(Annotation.__ebnf__).setResultsName("annotation")
    __ebnf__ = __ebnf__.setParseAction(lambda s, l, t: Comment(**dict(t)))

    # Internal data
    def __init__(self, comment, annotation = None):
        self.comment = comment
        self.annotation = annotation

    def dump(self, indent = 0):
        s = str(self.comment)

        if hasattr(self, 'annotation'):
            s += " %s"%(self.annotation)

        return s
        
