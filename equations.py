from pyparsing import Optional, Literal, ZeroOrMore
from base import BaseModelica


class EquationSection(BaseModelica):
    pass

class AlgorithmSection(BaseModelica):
    pass

class Equation(BaseModelica):
    pass

class Statement(BaseModelica):
    pass

class IfEquation(BaseModelica):
    pass

class IfStatement(BaseModelica):
    def __init__(self, first_expression, first_statements, else_expressions = [], else_statements = []):
        self.first_expression = first_expression
        self.first_statements = first_statements
        self.else_expressions = else_expressions
        self.else_statements = else_statements

    def dump(self, indent = 0):
        msg = " " * indent + "if %s then\n"%(str(self.first_expression))
        msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", self.first_statements))

        for expression, statements in zip(else_expressions, else_statements):
            msg += " " * indent + "elseif %s then\n"%(str(expression))
            msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", statements))
        
        if len(else_expressions) < len(else_statements):
            
            
            

            
            

        

class ForEquation(BaseModelica):
    def __init__(self, indices, equations = []):
        self.indices = indices
        self.equations = equations

    def dump(self, indent = 0):
        msg = " " * indent + "for %s loop\n"%(str(self.indices))
        msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", self.equations))
        msg += "\n" + " " * indent + "end for"
        return msg


class ForStatement(BaseModelica):
    def __init__(self, indices, statements = []):
        self.indices = indices
        self.statements = statements

    def dump(self, indent = 0):
        msg = " " * indent + "for %s loop\n"
        msg += "\n".join(map(lambda x: x.dump(indent + 2) + ";", self.statements))
        msg += "\n" + " " * indent + "end for"
        return msg

class ForIndices(BaseModelica):
    def __init__(self, indices = []):
        self.indices = indices

    def dump(self, indent = 0):
        return ", ".join(map(str, indices))

class ForIndex(BaseModelica):
    def __init__(self, identifier, in_expression = None):
        self.identifier = identifier
        self.in_expression = in_expression if (type(in_expression) is Expression) else None

    def dump(self, indent = 0):
        msg = str(self.identifier)
        if self.in_expression is not None:
            msg += " in %s"%(self.in_expression)
        return msg

class WhileStatement(BaseModelica):
    pass

class WhenEquation(BaseModelica):
    pass

class WhenStatement(BaseModelica):
    pass

class ConnectClause(BaseModelica):
    pass


class Equation(BaseModelica):
    __ebnf__ = Literal("ja").setParseAction(lambda s, l, t: Equation())

    def dump(self, indent = 0):
        return " " * indent + "ja"



class EquationSection(BaseModelica):
    __ebnf__ = (Optional(Literal("initial").setParseAction(lambda s, l, t: [True]).setResultsName("initial")) + Literal("equation") + ZeroOrMore(Equation.__ebnf__ + Literal(";").suppress()).setResultsName("equations"))

    # Define parse action
    __ebnf__ = __ebnf__.setParseAction(
        lambda s, l, t: EquationSection(
            **dict(
                initial = t['initial'],
                equations = list(t['equations'])
                )
              )
        )

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


