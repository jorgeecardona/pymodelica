from base import ModelicaBase, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward
from pyparsing import Literal, delimitedList

from tokens import String, Ident


class Expression(ModelicaBase):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)

class Expression(ModelicaBase):
    pass

class SipleExpression(ModelicaBase):
    pass

class LogicalExpression(ModelicaBase):
    pass

class LogicalTerm(ModelicaBase):
    pass

class LogicalFactor(ModelicaBase):
    pass

class Relation(ModelicaBase):
    pass

class RelOp(ModelicaBase):
    pass

class ArithmeticExpresion(ModelicaBase):
    pass

class AddOp(ModelicaBase):
    pass

class Term(ModelicaBase):
    pass

class MulOp(ModelicaBase):
    pass

class Factor(ModelicaBase):
    pass

class Primary(ModelicaBase):
    pass

class Name(ModelicaBase):

    def __init__(self, names):
        self.names = names

    def dump(self):
        return ".".join(map(str, self.names))

class ComponentReference(ModelicaBase):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)

class FunctionCallArgs(ModelicaBase):
    pass

class FunctionArguments(ModelicaBase):
    pass

class NamedArguments(ModelicaBase):
    pass

class NamedArgument(ModelicaBase):
    pass

class OutputExpressionList(ModelicaBase):
    pass

class ExpressionList(ModelicaBase):
    pass

class ArraySubscripts(ModelicaBase):
    pass

class Subscript(ModelicaBase):
    pass

class Comment(ModelicaBase):
    # Internal data
    def __init__(self, comment, annotation = None):
        self.comment = comment
        self.annotation = annotation

    def dump(self, indent = 0):
        s = str(self.comment)

        if hasattr(self, 'annotation'):
            s += " %s"%(self.annotation)

        return s

class StringComment(ModelicaBase):

    def __init__(self, comments):
        self.comments = comments
        
    def dump(self, indent = 0):
        return " + ".join(map(str, self.comments))

class Annotation(ModelicaBase):
    def __init__(self, modification):
        self.modification = modification

    def dump(self):
        return "annotation %s" % (self.modification)

class ClassModification(ModelicaBase):
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
    action = lambda s,l,t: Annotation(**dict(t))
    )
