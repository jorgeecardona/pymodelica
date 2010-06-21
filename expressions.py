from base import ModelicaBase, IncorrectValue, NonImplemented, hasLiteral

from pyparsing import CharsNotIn, Combine, OneOrMore, ZeroOrMore, Optional, Forward, Suppress
from pyparsing import Literal, delimitedList, Or, ParseExpression, ParserElement

from tokens import STRING, IDENT
#from equations import ForIndices

### B.2.1 Stored Definition

class StoredDefinition(ModelicaBase):
    def __init__(self, within=False, within_name=None, final=False, definition=None):
        self.within = within
        self.final = final
        self.definition = definition

    def dump(self):
        ret = ''
        if self.within:
            if isinstance(self.within_name, Name):
                ret += 'within %s;\n' % (self.within_name)
            else:
                ret += 'within;\n'

        if self.final:
            ret += 'final %s;' % self.definition
        else:
            ret += '%s;' % self.definition

        return ret


### B.2.2 Class Definition

class ClassDefinition(ModelicaBase):
    pass


### B.2.3 Extends



### B.2.4 Component Clause



### B.2.5 Modification



### B.2.6 Equations


# B.2.6 Equations
class ForIndices(ModelicaBase):
    def __init__(self, indices = []):
        self.indices = indices

    def dump(self, indent = 0):
        return ", ".join(map(str, self.indices))

class ForIndex(ModelicaBase):
    def __init__(self, identifier, expression = None):
        self.identifier = identifier
        self.expression = expression

    def dump(self, indent = 0):
        if isinstance(self.expression, Expression):
            msg = "%s in %s"%(self.identifier, self.expression)
        else:
            msg = "%s" % (self.identifier)

        return msg

# B.2.7 Expressions

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
    def __init__(self, *arguments):
        self.arguments = arguments

    def dump(self, indent = 0):
        return ", ".join(map(str, self.arguments))

class NamedArgument(ModelicaBase):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        
    def dump(self):
        return "%s = %s" % (self.identifier, self.expression)

class OutputExpressionList(ModelicaBase):
    def __init__(self, expressions):
        self.expressions = expressions
        
    def dump(self, indent = 0):
        return ", ".join(map(str, self.expressions))

class ExpressionList(ModelicaBase):
    def __init__(self, expressions):
        self.expressions = expressions
        
    def dump(self, indent = 0):
        return ", ".join(map(str, self.expressions))

class ArraySubscripts(ModelicaBase):
    def __init__(self, subscripts):
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

### B.2.1 Stored Definition

StoredDefinition.ebnf(
    syntax = (
        Optional(hasLiteral('within') + Optional(Name.name('within_name')) + Suppress(';')) + 
        Optional(hasLiteral('final') + ClassDefinition.name('definition') + Suppress(';'))
        ),
    action = lambda s,l,t: StoredDefinition(**dict(t))
    )

### B.2.2 Class Definition

ClassDefinition.ebnf(
    )

### B.2.3 Extends



### B.2.4 Component Clause



### B.2.5 Modification



### B.2.6 Equations

ForIndices.ebnf(
    syntax = delimitedList(ForIndex.names('indices'), delim=','),
    action = lambda s,l,t: ForIndices(**dict(t))
    )

ForIndex.ebnf(
    syntax = IDENT.name("identifier") + Optional(Suppress('in') + Expression.name('expression')),
    action = lambda s, l, t: ForIndex(**dict(t))
    )


### B.2.7 Expressions

FunctionArguments.ebnf(
    syntax = Or(Expression.name('expression') + Optional(Or(Suppress(',') + FunctionArguments.name("arguments"), Suppress('for') + ForIndices.name('for_indices'))), NamedArguments.name('arguments')),
    action = lambda s,l,t: FunctionArguments(**dict(t))
    )

Expression.ebnf(
    syntax = IDENT.name("identifier"),
    action = lambda s,l,t: Expression(**dict(t))
    )

NamedArguments.ebnf(
    syntax = delimitedList(NamedArgument.ebnf(), delim=","),
    action = lambda s,l,t: NamedArguments(*list(t))
    )

NamedArgument.ebnf(
    syntax = IDENT.name('identifier') + Suppress("=") + Expression.name('expression'),
    action = lambda s,l,t: NamedArgument(**dict(t))
    )

OutputExpressionList.ebnf(
    syntax = delimitedList(Expression.names('expressions'), delim=","),
    action = lambda s,l,t: OutputExpressionList(**dict(t))
    )

ExpressionList.ebnf(
    syntax = delimitedList(Expression.names('expressions'), delim=","),
    action = lambda s,l,t: ExpressionList(**dict(t))
    )

ArraySubscripts.ebnf(
    syntax = Suppress("[") + delimitedList(Subscript.names('subscripts'), delim=",") + Suppress("]"),
    action = lambda s,l,t: ArraySubscripts(**dict(t))
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
#    action = lambda s,l,t: Annotation(**dict(t))
    )
