from pyparsing import Optional, Literal, ZeroOrMore
from base import BaseModelica


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


