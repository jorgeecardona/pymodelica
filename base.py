from pyparsing import Forward

class NonImplemented(Exception):
    pass

class IncorrectValue(Exception):
    pass

class ParseError(Exception):
    pass

class BaseModelica(object):
    """
    BaseModelica
    ============

    This class is the base of all modelica entities. It has two methods:

    * **load(cls, string)** It creates an element based on the string passed.

    * **dump(self)** It return the element in string modelica format.

    """

    @classmethod
    def ebnf(cls, syntax = None):

        if syntax is None:

            if not hasattr(cls, '__ebnf__'):
                cls.__ebnf__ = Forward()

            return cls.__ebnf__

        else:
            if not hasattr(cls, '__ebnf__'):
                cls.__ebnf__ = syntax
            else:
                cls.__ebnf__ << syntax

            return cls.__ebnf__
                

        


    

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

