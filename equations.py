from pyparsing import Optional, Literal, ZeroOrMore, Forward
from base import BaseModelica, hasLiteral
from expressions import Expression, ComponentReference

from tokens import Ident

class EquationSection(BaseModelica):
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

class AlgorithmSection(BaseModelica):
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

class Equation(BaseModelica):
    __ebnf__ = Literal("ja").setParseAction(lambda s, l, t: Equation())

    def dump(self, indent = 0):
        return " " * indent + "ja"


class Equation(BaseModelica):
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

class Equation(BaseModelica):
    pass
        
class Statement(BaseModelica):
    pass

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

class ForIndices(BaseModelica):
    __ebnf__ = Forward()
    def __init__(self, indices = []):
        self.indices = indices

    def dump(self, indent = 0):
        return ", ".join(map(str, self.indices))


class ForIndex(BaseModelica):
    def __init__(self, identifier, expression = None):
        self.identifier = identifier
        self.expression = expression if isinstance(expression, Expression) else None

    def dump(self, indent = 0):
        msg = str(self.identifier)
        if self.expression is not None:
            msg += " in %s"%(self.expression)
        return msg

class WhileStatement(BaseModelica):
    
    def __init__(self, expression, statements = []):
        self.expression = expression
        self.statements = statements

        def dump(self, indent = 0):
            msg = "while %s loop\n%s\nend while"%(
                self.expression,
                "\n".join(lambda x: "  %s;"%(x), self.statements)
                ) 
            return msg

class WhenEquation(BaseModelica):

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

class WhenStatement(BaseModelica):

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

class ConnectClause(BaseModelica):
    pass


EquationSection.ebnf(
    syntax = (
        Optional(hasLiteral("initial")) + Literal("equation") +
        ZeroOrMore(Equation.ebnf() + Supress(";"))("equations")
        ),
    
    action = lambda s,l,t: EquationSection(initial = t['initial'], equations = list(t['equations']))
    )

AlgorithmSection.ebnf(
    syntax = (
        Optional(hasLiteral("initial")) + Literal("algorithm") +
        ZeroOrMore(Statement.ebnf() + Supress(";"))("statements")
        ),
    
    action = lambda s,l,t: EquationSection(initial = t['initial'], equations = list(t['statements']))
    )

Equation.ebnf(
    )

Statement.ebnf(
    )

IfEquation.ebnf(
    syntax = (
        Literal("if") + Expression.ebnf().setResultsName("expressions",listAllMatches=True) + Literal("then") + 
        
        ZeroOrMore(Equation.ebnf() + Supress(";")).setResultsName("equations",listAllMatches = True) + 
        
        ZeroOrMore( Literal("elseif") + Expression.ebnf().setResultsName("expressions",listAllMatches=True) + Literal("then") +
                    ZeroOrMore(Equation.ebnf() + Supress(";")).setResultsName("equations",listAllMatches = True)) + 
        
        Optional(Literal("else") +
                 ZeroOrMore(Equation.ebnf() + Supress(";")).setResultsName("equations", listAllMatches = True)) +
        Literal("end") + Literal("if")
        ),
    
    action = lambda s, l, t: IfEquation(expressions = t["expressions"], equations = t["equations"])
    )

IfStatement.ebnf(
    syntax = (
        Literal("if") + Expression.ebnf().setResultsName("expressions",listAllMatches=True) + Literal("then") + 
        
        ZeroOrMore(Statement.ebnf() + Supress(";")).setResultsName("statements",listAllMatches = True) + 
        
        ZeroOrMore( Literal("elseif") + Expression.ebnf().setResultsName("expressions",listAllMatches=True) + Literal("then") +
                    ZeroOrMore(Statement.ebnf() + Supress(";")).setResultsName("statements",listAllMatches = True)) + 
        
        Optional(Literal("else") +
                 ZeroOrMore(Statement.ebnf() + Supress(";")).setResultsName("statements", listAllMatches = True)) +
        Literal("end") + Literal("if")
        ),
    
    action = lambda s, l, t: IfStatement(expressions = t["expressions"], statements = t["statements"])
    )

ForEquation.ebnf(
    syntax = (
        Literal("for") + ForIndices.ebnf()("indices") + Literal("loop") + 
        ZeroOrMore( Equation.ebnf() + Supress(";"))("equations") + 
        Literal("end") + Literal("for")
        ),

    action = lambda s, l, t: ForEquation(**dict(t))
    )

ForStatement.ebnf( 
    syntax = (
        Literal("for") + ForIndices.ebnf()("indices") + Literal("loop") + 
        ZeroOrMore( Statement.ebnf() + Supress(";"))("statements") + 
        Literal("end") + Literal("for")
        ),

    action = lambda s, l, t: ForStatement(**dict(t))
    )

ForIndices.ebnf(
    syntax = ForIndex.ebnf + ZeroOrMore(Supress(",") + ForIndex.ebnf()),

    action = lambda s,l,t: ForIndices(t)
    )

ForIndex.ebnf(
    syntax = Ident.ebnf().setResultsName("identifier"),

    action = lambda s, l, t: ForIndex(**dict(t))
    )

WhileStatement.ebnf(
    syntax = (
        Literal("while") + Expression.ebnf()("expression") + Literal("then") + 
        ZeroOrMore(Statement.ebnf() + Supress(";"))("statements") + 
        Literal("end") + Literal("while")
        ),

    action = lambda s,l,t: WhileStatement(**dict(t))
    )

WhenEquation.ebnf(
    syntax = (
        Literal("when") + Expression.ebnf()("expression") + Literal("then") + 
        
        ZeroOrMore(Equation.ebnf() + Supress(";"))("equations") + 
        Optional( Literal("elsewhen") + Expression.ebnf()("expression_else") + Literal("then") + 
                  ZeroOrMore(Equation.ebnf() + Supress(";"))("equations_else")) + 
        Literal("end") + Literal("when")
        ),

    action = lambda s,l,t: WhenEquation(**dict(t))
    )

WhenStatement.ebnf(
    syntax = (
        Literal("when") + Expression.ebnf()("expression") + Literal("then") + 
        ZeroOrMore(Statement.ebnf() + Supress(";"))("statements") + 
        Optional( Literal("elsewhen") + Expression.ebnf()("expression_else") + Literal("then") + 
                  ZeroOrMore(Statement.ebnf() + Supress(";"))("statements_else")) + 
        Literal("end") + Literal("when")
        ),

    action = lambda s,l,t: WhenStatement(**dict(t))
    )

ConnectClause.ebnf(
    syntax = (
        Literal("connect") + Literal("(") + 
        ComponentReference.ebnf()("component_1") + Literal(",") + 
        ComponentReference.ebnf()("component_2") + Literal(")")
        ),
    
    action = lambda s,l,t: ConnectClause(**dict(t))
    )
