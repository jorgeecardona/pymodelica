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

class Class(ModelicaBase):
    pass

class Model(ModelicaBase):
    pass

class Record(ModelicaBase):
    pass

class Block(ModelicaBase):
    pass

class Connector(ModelicaBase):
    pass

class Type(ModelicaBase):
    pass

class Package(ModelicaBase):
    pass

class Function(ModelicaBase):
    pass

class Operator(ModelicaBase):
    pass

class ClassSpecifier(ModelicaBase):
    def __init__(self, class_name, comment=None, composition=None, base_prefix=None, base_name=None, base_subscripts=None, base_modification=None):
        pass
    pass

class BasePrefix(ModelicaBase):
    pass

class EnumList(ModelicaBase):
    pass

class EnumerationLiteral(ModelicaBase):
    pass

class Composition(ModelicaBase):
    pass

class LanguageSpecification(ModelicaBase):
    pass

class ExternalFunctionCall(ModelicaBase):
    pass

class ElementList(ModelicaBase):
    pass

class Element(ModelicaBase):
    pass

class ImportClause(ModelicaBase):
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

class SimpleExpression(ModelicaBase):
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
    def __init__(self, expressions=None, for_expression=None, for_indices=None, arguments=[]):
        self.expressions = expressions
        self.for_expression = for_expression
        self.for_indices = for_indices
        self.arguments = arguments

    def dump(self):

        elements = []
        if isinstance(self.expressions, ExpressionList):
            elements.append('%s' % (self.expressions))

        if isinstance(self.for_expression, Expression):
            if isinstance(self.for_indices, ForIndices):
                elements.append('%s for %s' % (self.for_expression, self.for_indices))
                    
        if isinstance(self.arguments, NamedArguments):
            elements.append('%s' % (self.arguments))

        return ', '.join(elements)        

class NamedArguments(ModelicaBase):
    def __init__(self, arguments):
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
    syntax = (
        Class.name('definition')
        )
    )

Class.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('class') + ClassSpecifier.name('specification')
        )
    )

Model.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('model') + ClassSpecifier.name('specification')
        )
    )

Record.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('record') + ClassSpecifier.name('specification')
        )
    )

Block.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('block') + ClassSpecifier.name('specification')
        )
    )

Connector.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Optional(hasLiteral('expandable')) +
        Suppress('connector') + ClassSpecifier.name('specification')
        )
    )

Type.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('type') + ClassSpecifier.name('specification')
        )
    )

Package.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('package') + ClassSpecifier.name('specification')
        )
    )

Function.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('function') + ClassSpecifier.name('specification')
        )
    )

Operator.ebnf(
    syntax = (
        Optional(hasLiteral('encapsulated')) +
        Optional(hasLiteral('partial')) + 
        Suppress('operator') + Optional(
            hasLiteral('function') ^ hasLiteral('record')
            ) + ClassSpecifier.name('specification')
        )
    )

ClassSpecifier.ebnf(
    syntax = Or(
        (
            IDENT.name('class_name') + StringComment.name('comment') + 
            Composition.name('composition') + 
            Suppress('end') + IDENT.name('class_name')
            ),
        (
            IDENT.name('class_name') + Suppress('=') + 
            BasePrefix.name('base_prefix') + Name.name('base_name') + 
            Optional(ArraySubscripts.name('base_subscripts')) + 
            Optional(ClassModification.name('base_modification')) +
            Comment.name('comment')
            ),
        
        )
    )

### B.2.3 Extends



### B.2.4 Component Clause



### B.2.5 Modification



### B.2.6 Equations

ForIndices.ebnf(
    syntax = delimitedList(ForIndex.names('indices'), delim=','),
    )

ForIndex.ebnf(
    syntax = IDENT.name("identifier") + Optional(Suppress('in') + Expression.name('expression')),
    )


### B.2.7 Expressions

Name.ebnf(
    syntax = delimitedList(IDENT.names('names'), delim='.')
    )

ComponentReference.ebnf(
    syntax = delimitedList(IDENT.names('names') + Optional(ArraySubscripts.names('subscripts')), delim='.')
    )

FunctionCallArgs.ebnf(
    syntax = Suppress('(') + Optional(FunctionArguments.name('arguments')) + Suppress(')')
    )

FunctionArguments.ebnf(
    syntax = Or([
            NamedArguments.name('arguments'),
            Expression.name('for_expression') + Suppress('for') + ForIndices.name('for_indices'),
            ExpressionList.name('expressions'),
            ExpressionList.name('expressions') + Suppress(',') + NamedArguments.name('arguments'),
            ExpressionList.name('expressions') + Suppress(',') + 
            Expression.name('for_expression') + Suppress('for') + ForIndices.name('for_indices')
            ])
    
#    syntax = Or(
#        Expression.name('expression') + Optional(Or(Suppress(',') + FunctionArguments.name("arguments"), Suppress('for') + ForIndices.name('for_indices'))), 
#        NamedArguments.name('arguments')
#        )
    )

Expression.ebnf(
    syntax = IDENT.name("identifier")
    )

NamedArguments.ebnf(
    syntax = delimitedList(NamedArgument.names('arguments'), delim=","),
    )

NamedArgument.ebnf(
    syntax = IDENT.name('identifier') + Suppress("=") + Expression.name('expression'),
    )

OutputExpressionList.ebnf(
    syntax = delimitedList(Expression.names('expressions'), delim=","),
    )

ExpressionList.ebnf(
    syntax = delimitedList(Expression.names('expressions'), delim=","),
    )

ArraySubscripts.ebnf(
    syntax = Suppress("[") + delimitedList(Subscript.names('subscripts'), delim=",") + Suppress("]"),
    )

Subscript.ebnf(
    syntax = Suppress(":") ^ Expression.name("expression"),
    )

ComponentReference.ebnf(
    syntax = IDENT.name("identifier"),
    )

Comment.ebnf(
    syntax = StringComment.name("comment") + Optional(Annotation.name("annotation")),
    )

StringComment.ebnf(
    syntax = delimitedList(STRING.names('comments'), delim="+"),
    )

Annotation.ebnf(
    syntax = Literal("annotation") + ClassModification.name('modification'),
    )
