from pyparsing import Forward, Or, Literal, Suppress

class NonImplemented(Exception):
    pass

class IncorrectValue(Exception):
    pass

class ParseError(Exception):
    pass

class ModelicaBase(object):
    """
    Modelica Base Class
    ===================

    This class is the base of all modelica entities. It has two methods:

    * **load(cls, string)** It creates an element based on the string passed.

    * **dump(self)** It return the element in string modelica format.

    """
    @classmethod
    def load(cls, string):
        # This reads a string and return the element created.
        try:
            return cls.ebnf().parseString(string)[0]
        except:
            raise ParseError()
    
    def dump(self, indent = 0):
        raise NonImplemented

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return "%s: %s"%(str(self.__class__.__name__), str(self))

    @classmethod
    def ebnf(self, syntax = None, action = None):

        # Try to set the __ebnf__
        if not hasattr(self, '__ebnf__'):
            self.__ebnf__ = Forward()

        if syntax is not None:
            if action is None:
                self.__ebnf__ << syntax
                self.__ebnf__ = self.__ebnf__.setParseAction(lambda s,l,t: self(**dict(t)))
            else:
                self.__ebnf__ << syntax

        if action is not None:
            self.__ebnf__ = self.__ebnf__.setParseAction(action)

        return self.__ebnf__

    @classmethod
    def name(cls, name):
        return Or(cls.ebnf()).setResultsName(name)

    @classmethod
    def names(cls, name):
        return Or(cls.ebnf()).setResultsName(name, listAllMatches=True)

    @classmethod
    def __call__(cls, name=None):
        if name is None:
            return cls.ebnf()
        else:
            return cls.name(name)

def presenceBool(syntax):
    return syntax.setParseAction(lambda s,l,t:True)

def hasLiteral(name, variable=None):
    if variable is None:
        variable = name

    return presenceBool(Suppress(name))(variable)


def hasLiterals(names, variable=None):
    if variable is None:
        variable = "_".join(names)

    return presenceBool(names.reduce(lambda x,y: Suppress(x) + Suppress(y)))(variable)

