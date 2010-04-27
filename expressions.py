from base import BaseModelica, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward
from pyparsing import Literal, delimitedList

from tokens import String, Ident


class Expression(BaseModelica):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)

class Expression(BaseModelica):
    pass

class SipleExpression(BaseModelica):
    pass

class LogicalExpression(BaseModelica):
    pass

class LogicalTerm(BaseModelica):
    pass

class LogicalFactor(BaseModelica):
    pass

class Relation(BaseModelica):
    pass

class RelOp(BaseModelica):
    pass

class ArithmeticExpresion(BaseModelica):
    pass

class AddOp(BaseModelica):
    pass

class Term(BaseModelica):
    pass

class MulOp(BaseModelica):
    pass

class Factor(BaseModelica):
    pass

class Primary(BaseModelica):
    pass

class Name(BaseModelica):

    def __init__(self, names):
        self.names = names

    def dump(self):
        return ".".join(map(str, self.names))

class ComponentReference(BaseModelica):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)

class FunctionCallArgs(BaseModelica):
    pass

class FunctionArguments(BaseModelica):
    pass

class NamedArguments(BaseModelica):
    pass

class NamedArgument(BaseModelica):
    pass

class OutputExpressionList(BaseModelica):
    pass

class ExpressionList(BaseModelica):
    pass

class ArraySubscripts(BaseModelica):
    pass

class Subscript(BaseModelica):
    pass

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

class StringComment(BaseModelica):

    def __init__(self, comments):
        self.comments = comments
        
    def dump(self, indent = 0):
        return " + ".join(map(str, self.comments))

class Annotation(BaseModelica):
    pass

class ClassModification(BaseModelica):
    __ebnf__ = Literal("1")


StringComment.ebnf(
    syntax = Ident.ebnf() + ZeroOrMore(Literal(".").suppress() + Ident.ebnf()),
    action = lambda s, l, t: Name(list(t))
    )

Expression.ebnf(
    syntax = Ident.ebnf()("identifier"),
    action = lambda s,l,t: Expression(**dict(t))
    )

ComponentReference.ebnf(
    syntax = Ident.ebnf()("identifier"),
    action = lambda s,l,t: ComponentReference(**dict(t))
    )

Comment.ebnf(
    syntax = StringComment.ebnf()("comment") + Optional(Annotation.ebnf())("annotation"),
    action = lambda s, l, t: Comment(**dict(t))
    )

StringComment.ebnf(
    syntax = Optional(delimitedList(String.ebnf(), delim="+")),
    action = lambda s,l,t: StringComment(list(t))
    )

Annotation.ebnf(
    syntax = Literal("annotation") + ClassModification.ebnf()('modification'),
    action = lambda s,l,t: Annotation(t['modification'])
    )
