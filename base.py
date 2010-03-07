
class NonImplemented(Exception):
    pass

class IncorrectValue(Exception):
    pass

class ParseError(Exception):
    pass

class BaseModelica:
    """
    BaseModelica
    ============

    This class is the base of all modelica entities. It has two methods:

    * **load(cls, string)** It creates an element based on the string passed.

    * **dump(self)** It return the element in string modelica format.

    """
    __ebnf__ = None
    
    @classmethod
    def load(cls, string):
        # This reads a string and return the element created.
        try:
            return cls.__ebnf__.parseString(string)[0]
        except:
            raise ParseError()
    
    def dump(self):
        raise NonImplemented

    def __str__(self):
        return self.dump()

