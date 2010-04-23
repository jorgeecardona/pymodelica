from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward
from pyparsing import Literal

from tokens import String, Ident

class Name(BaseModelica):

    def __init__(self, names):
        self.names = names

    def dump(self):
        return ".".join(map(str, self.names))

class ClassModification(BaseModelica):
    __ebnf__ = Literal("1")

class StringComment(BaseModelica):

    def __init__(self, comments):
        self.comments = comments
        
    def dump(self, indent = 0):
        return " + ".join(map(str, self.comments))

class Annotation(BaseModelica):
    __ebnf__ = Literal("annotation") + ClassModification.__ebnf__


class Comment(BaseModelica):
    # Internal data
    def __init__(self, comment, annotation = None):
        self.comment = comment
        self.annotation = annotation

    def dump(self, indent = 0):
        s = str(self.comment)

        if hasattr(self, 'annotation'):
            s += " %s"%(self.annotation)

        return s

class Expression(BaseModelica):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)


class ComponentReference(BaseModelica):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)

StringComment.ebnf(
    syntax = Ident.ebnf() + ZeroOrMore(Literal(".").suppress() + Ident.ebnf()),
    action = lambda s, l, t: Name(list(t))
    )

Expression.ebnf(
    syntax = Ident.ebnf().setResultsName("identifier"),
    action = lambda s,l,t: Expression(**dict(t))
    )

ComponentReference.ebnf(
    syntax = Ident.ebnf().setResultsName("identifier"),
    action = lambda s,l,t: ComponentReference(**dict(t))
    )

Comment.ebnf(
    syntax = StringComment.ebnf().setResultsName("comment") + Optional(Annotation.ebnf()).setResultsName("annotation"),
    action = lambda s, l, t: Comment(**dict(t))
    )
