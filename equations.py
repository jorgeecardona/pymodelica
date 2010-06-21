from expressions import Expression, ComponentReference
from pyparsing import Optional, Literal, ZeroOrMore, Forward, Suppress, delimitedList

from tokens import IDENT
from base import ModelicaBase, hasLiteral

class EquationSection(ModelicaBase):
    def __init__(self, initial = False, equations = []):
        self.initial = initial
        self.equations = equations

    def dump(self, indent = 0):
        msg =  (" " * indent)
        msg += ("initial " if self.initial else "")
        msg += "equation"
        for eq in self.equations:
            msg += "\n" + (" " * indent) + eq.dump(indent + 2) + ";"

        return msg

class AlgorithmSection(ModelicaBase):
    def __init__(self, initial = False, algorithms = []):
        self.initial = initial
        self.algorithms = algorithms

    def dump(self, indent = 0):
        msg =  (" " * indent)
        msg += ("initial " if self.initial else "")
        msg += "algorithm"
        for eq in self.algorithms:
            msg += "\n" + (" " * indent) + eq.dump(indent + 2) + ";"

        return msg

class Equation(ModelicaBase):
    __ebnf__ = Literal("ja").setParseAction(lambda s, l, t: Equation())

    def dump(self, indent = 0):
        return " " * indent + "ja"


class Equation(ModelicaBase):
    def __init__(self, 
                 simple_expression = None, expression = None, 
                 if_equation = None, 
                 for_equation = None, 
                 connect_clause = None, 
                 when_equation = None, 
                 function_identifier = None, function_args = None,
                 comment = None):

        # Test for first kind: simple_expression = expression.
        if (type(simple_expression) is SimpleExpression) and (type(expression) is Expression):
            self.simple_expression = simple_expression
            self.expression = expression
            self.type = 'equation'

        elif type(if_equation) is IfEquation:
            self.if_equation = if_equation
            self.type = 'if'

        elif type(for_equation) is IfEquation:
            self.for_equation = for_equation
            self.type = 'for'

        elif type(connect_clause) is ConnectClause:
            self.connect_clause = connect_clause
            self.type = 'connect'

        elif type(when_equation) is WhenEquation:
            self.when_equation = when_equation
            self.type = 'when'
            
        elif (type(function_identifier) is Identifier) and (type(function_args) is FunctionCallArgs):
            self.function_identifier = function_identifier
            self.function_args
            self.type = 'function'

        else:
            raise Exception("Incorrect type of equation.")

        self.comment = comment


    def dump(self, indent = 0):
        if self.type is 'if':
            return "%s %s"%(self.if_equation.dump(indent), str(self.comment))

        elif self.type is 'for':
            return "%s %s"%(self.for_equation.dump(indent), str(self.comment))

        elif self.type is 'when':
            return "%s %s"%(self.when_equation.dump(indent), str(self.comment))

        elif self.type is 'connect':
            return "%s %s"%(self.connect_clause.dump(indent), str(self.comment))

        elif self.type is 'equation':
            return "%s = %s %s"%(self.simple_expression.dump(indent), str(self.expression), str(self.comment))

        elif self.type is 'function':
            return  "%s%s %s"%(self.function_identifier.dump(identifier), str(self.function_args), str(self.comment))

        else:
            raise Exception("Equation without type.")

class Equation(ModelicaBase):
    pass
        
class Statement(ModelicaBase):
    pass


class EquationArray(ModelicaBase):
    def __init__(self, equations=[]):
        self.equations = equations

    def dump(self):
        return ";\n".join(map(str, self.equations))

class StatementArray(ModelicaBase):
    def __init__(self, statements=[]):
        self.statements = statements

    def dump(self):
        return ";\n".join(map(str, self.statements))

class FunctionCallEquation(Equation):
    def __init__(self, identifier, args, comment = None):
        self.identifier = identifier
        self.args = args
        self.comment = comment

    def dump(self, indent = 0):
        ret = "%s%s"%(self.identifier, self.args)
        if type(self.comment) is Comment:
            ret += " %s"%(str(self.comment))            
        return ret
        

class IfEquation(Equation):
    def __init__(self, first_expression, first_equations, else_expressions = [], else_equations = [], comment = None):
        self.first_expression = first_expression
        self.first_equations = first_equations
        self.else_expressions = else_expressions
        self.else_equations = else_equations
        self.comment = comment

    def dump(self, indent = 0):
        msg = " " * indent + "if %s then\n"%(str(self.first_expression))
        msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", self.first_equations))

        for expression, equations in zip(else_expressions, else_equations):
            msg += "\n" + " " * indent + "elseif %s then\n"%(str(expression))
            msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", equations))
        
        if len(else_expressions) < len(else_equations):
            msg += "\n" + " " * indent + "else\n"
            msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", else_equations[-1]))

        msg += "\n" + " " * indent + "end if"

        if type(self.comment) is Comment:
            msg += " %s"%(str(self.comment))            
        return msg


class IfStatement(Statement):
    def __init__(self, first_expression, first_statements, else_expressions = [], else_statements = [], comment = None):
        self.first_expression = first_expression
        self.first_statements = first_statements
        self.else_expressions = else_expressions
        self.else_statements = else_statements
        
        self.comment = comment

    def dump(self, indent = 0):
        msg = " " * indent + "if %s then\n"%(str(self.first_expression))
        msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", self.first_statements))

        for expression, statements in zip(else_expressions, else_statements):
            msg += "\n" + " " * indent + "elseif %s then\n"%(str(expression))
            msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", statements))
        
        if len(else_expressions) < len(else_statements):
            msg += "\n" + " " * indent + "else\n"
            msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", else_statements[-1]))

        msg += "\n" + " " * indent + "end if"

        if type(self.comment) is Comment:
            msg += " %s"%(str(self.comment))            
        return msg


class ForEquation(Equation):
    def __init__(self, indices, equations = [], comment = None):
        self.indices = indices
        self.equations = equations

        self.comment = comment

    def dump(self, indent = 0):
        msg = " " * indent + "for %s loop\n"%(str(self.indices))
        msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", self.equations))
        msg += "\n" + " " * indent + "end for"

        if type(self.comment) is Comment:
            msg += " %s"%(str(self.comment))            
        return msg


class ForStatement(Statement):
    def __init__(self, indices, statements = []):
        self.indices = indices
        self.statements = statements

    def dump(self, indent = 0):
        msg = " " * indent + "for %s loop\n"%(str(self.indices))
        msg += "\n".join(map(lambda x: " " * (indent + 2) + x.dump() + ";", self.statements))
        msg += "\n" + " " * indent + "end for"
        return msg

class ForIndices(ModelicaBase):
    def __init__(self, indices = []):
        self.indices = indices

    def dump(self, indent = 0):
        return ", ".join(map(str, self.indices))


class ForIndex(ModelicaBase):
    def __init__(self, identifier, expression = None):
        self.identifier = identifier
        self.expression = expression if isinstance(expression, Expression) else None

    def dump(self, indent = 0):
        msg = str(self.identifier)
        if self.expression is not None:
            msg += " in %s"%(self.expression)
        return msg

class WhileStatement(ModelicaBase):
    
    def __init__(self, expression, statements = []):
        self.expression = expression
        self.statements = statements

        def dump(self, indent = 0):
            msg = "while %s loop\n%s\nend while"%(
                self.expression,
                "\n".join(lambda x: "  %s;"%(x), self.statements)
                ) 
            return msg

class WhenEquation(ModelicaBase):

    def __init__(self, expression, statements = [], else_expression = None, else_statements = []):
        self.expression = expression
        self.statements = statements
        self.else_expression = else_expression
        self.else_statements = else_statements

    def dump(self, indent):
        msg = " " * indent + "when %s then\n"%(self.expression)
        msg += "\n".join(map(lambda x: " " * (indent + 2) + str(x) + ";", self.statements))
        msg += " " * indent + "end when" 

        return msg

class WhenStatement(ModelicaBase):

    def __init__(self, expression, equations = [], else_expression = None, else_equations = []):
        self.expression = expression
        self.equations = equations
        self.else_expression = else_expression
        self.else_equations = else_equations

    def dump(self, indent):
        msg = " " * indent + "when %s then\n"%(self.expression)
        msg += "\n".join(map(lambda x: " " * (indent + 2) + str(x) + ";", self.equations))
        msg += " " * indent + "end when"

        return msg

class ConnectClause(ModelicaBase):
    pass


EquationSection.ebnf(
    syntax = Optional(hasLiteral("initial")) + Suppress("equation") + ZeroOrMore(Equation.ebnf() + Suppress(";"))('equations'),
    action = lambda s,l,t: EquationSection(**dict(t))
    )

AlgorithmSection.ebnf(
    syntax = Optional(hasLiteral("initial")) + Literal("algorithm") + ZeroOrMore(Statement.ebnf() + Suppress(";"))('statements'),
    action = lambda s,l,t: AlgorithmSection(**dict(t))
    )

Equation.ebnf(
    )

Statement.ebnf(
    )

EquationArray.ebnf(
    syntax = ZeroOrMore(Equation.names('equations') + Suppress(";")),
    action = lambda s,l,t: EquationArray(**dict(t))
    )

StatementArray.ebnf(
    syntax = ZeroOrMore(Statement.names('statements') + Suppress(";")),
    action = lambda s,l,t: StatementArray(**dict(t))
    )

IfEquation.ebnf(
    syntax =\
        Suppress("if") + Expression.name('expressions') + Suppress('then') +\
        ZeroOrMore(Equation.ebnf() + Suppress(";")).setResultsName('equations',listAllMatches = True) +\
        ZeroOrMore( Suppress("elseif") + Expression.names('expressions') + Suppress('then') +
                    ZeroOrMore(Equation.ebnf() + Suppress(";")).setResultsName('equations',listAllMatches = True)) +\
        Optional(Literal("else") + ZeroOrMore(Equation.ebnf() + Suppress(";")).setResultsName('equations', listAllMatches = True)) +\
        Literal('end') + Literal("if"),
    action = lambda s, l, t: IfEquation(expressions = t['expressions'], equations = t['equations'])
    )

IfStatement.ebnf(
    syntax = (
        Literal("if") + Expression.ebnf().setResultsName('expressions',listAllMatches=True) + Literal('then') + 
        
        ZeroOrMore(Statement.ebnf() + Suppress(";")).setResultsName('statements',listAllMatches = True) + 
        
        ZeroOrMore( Literal("elseif") + Expression.ebnf().setResultsName('expressions',listAllMatches=True) + Literal('then') +
                    ZeroOrMore(Statement.ebnf() + Suppress(";")).setResultsName('statements',listAllMatches = True)) + 
        
        Optional(Literal("else") +
                 ZeroOrMore(Statement.ebnf() + Suppress(";")).setResultsName('statements', listAllMatches = True)) +
        Literal('end') + Literal("if")
        ),
    
    action = lambda s, l, t: IfStatement(expressions = t['expressions'], statements = t['statements'])
    )

ForEquation.ebnf(
    syntax = (
        Literal("for") + ForIndices.ebnf()("indices") + Literal("loop") + 
        ZeroOrMore( Equation.ebnf() + Suppress(";"))('equations') + 
        Literal('end') + Literal("for")
        ),

    action = lambda s, l, t: ForEquation(**dict(t))
    )

ForStatement.ebnf( 
    syntax = (
        Suppress("for") + ForIndices.name("indices") + Suppress("loop") + 
        ZeroOrMore( Statement.names('statements') + Suppress(";")) + 
        Suppress('end') + Suppress("for")
        ),

    action = lambda s, l, t: ForStatement(**dict(t))
    )

ForIndices.ebnf(
    syntax = delimitedList(ForIndex.names('indices'), delim=','),
    action = lambda s,l,t: ForIndices(**dict(t))
    )

ForIndex.ebnf(
    syntax = IDENT.name("identifier") + Optional(Suppress('in') + Expression.name('expression')),
    action = lambda s, l, t: ForIndex(**dict(t))
    )

WhileStatement.ebnf(
    syntax = (
        Suppress("while") + Expression.name("expression") + Suppress('loop') + 
        StatementArray.name('statements') +
        Suppress('end') + Suppress("while")
        ),
    action = lambda s,l,t: WhileStatement(**dict(t))
    )

WhenEquation.ebnf(
    syntax = (
        Suppress('when') + Expression.names('expressions') + Suppress('then') + 
        EquationArray.names('equations') + 
        ZeroOrMore( 
            Suppress("elsewhen") + Expression.names('expressions') + Suppress('then') + 
            EquationArray.names('equations')) +
        Suppress('end') + Suppress('when')
        ),
    action = lambda s,l,t: WhenEquation(**dict(t))
    )

WhenStatement.ebnf(
    syntax = (
        Suppress('when') + Expression.names('expressions') + Suppress('then') + 
        StatementArray.names('statements') + 
        ZeroOrMore( 
            Suppress("elsewhen") + Expression.names('expressions') + Suppress('then') + 
            StatementArray.name('statements')) +
        Suppress('end') + Suppress('when')
        ),
    action = lambda s,l,t: WhenStatement(**dict(t))
    )

ConnectClause.ebnf(
    syntax = (
        Suppress('connect') + Suppress('(') + 
        ComponentReference.name("component_1") + Suppress(',') + 
        ComponentReference.name("component_2") + Suppress(')')
        ),
    action = lambda s,l,t: ConnectClause(**dict(t))
    )
