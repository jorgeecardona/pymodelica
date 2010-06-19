from base import ModelicaBase, IncorrectValue, NonImplemented

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward, Suppress
from pyparsing import Literal, delimitedList, Or, ParseExpression, ParserElement

from tokens import STRING, IDENT


class Expression(ModelicaBase):
    def __init__(self, identifier):
        self.identifier = identifier

    def dump(self, indent = 0):
        return str(self.identifier)

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
    def __init__(self, *subscripts):
        self.subscripts = subscripts
        
    def dump(self, indent = 0):
        return "[%s]" % (", ".join(map(str, self.subscripts)))

class Subscript(ModelicaBase):
    def __init__(self, expression=None):
        self.expression = expression

    def dump(self):
        if self.expression is None:
            msg = ":"
        else:
            msg = "%s" % (self.expression)

        return msg

class Comment(ModelicaBase):
    # Internal data
    def __init__(self, comment, annotation = None):
        self.comment = comment
        self.annotation = annotation

    def dump(self, indent = 0):
        s = str(self.comment)

        if hasattr(self, 'annotation'):
            if isinstance(self.annotation, Annotation):
                s += " %s"%(self.annotation)

        return s

class StringComment(ModelicaBase):

    def __init__(self, *comments):
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



Expression.ebnf(
    syntax = IDENT.name("identifier"),
    action = lambda s,l,t: Expression(**dict(t))
    )

ArraySubscripts.ebnf(
    syntax = Suppress("[") + delimitedList(Subscript.ebnf(), delim=",") + Suppress("]"),
    action = lambda s,l,t: ArraySubscripts(*list(t))
    )

Subscript.ebnf(
    syntax = Suppress(":") ^ Expression.name("expression"),
    action = lambda s,l,t: Subscript(**dict(t))
    )

ComponentReference.ebnf(
    syntax = IDENT.name("identifier"),
    action = lambda s,l,t: ComponentReference(**dict(t))
    )

Comment.ebnf(
    syntax = StringComment.name("comment") + Optional(Annotation.name("annotation")),
    action = lambda s, l, t: Comment(**dict(t))
    )

StringComment.ebnf(
    syntax = delimitedList(STRING.ebnf(), delim="+"),
    action = lambda s,l,t: StringComment(*list(t))
    )

Annotation.ebnf(
    syntax = Literal("annotation") + ClassModification.name('modification'),
    action = lambda s,l,t: Annotation(**dict(t))
    )
