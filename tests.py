import unittest
from tokens import Ident, Integer, IntegerList
from base import IncorrectValue, ParseError


class testTokensLoad(unittest.TestCase):
    def setUp(self):
        pass

    def testIdent(self):
        self.assertTrue(Ident.load("algo").value == "algo")
        self.assertTrue(Ident.load("Algo").value == "Algo")
        self.assertTrue(Ident.load("_algo").value == "_algo")
        self.assertTrue(Ident.load("  _algo  ").value == "_algo")

        self.assertRaises(ParseError, lambda: Ident.load("1algo"))

    def testInteger(self):
        self.assertTrue(Integer.load(" 123     ").value == 123)


    def testIntegerList(self):

        integer_list = IntegerList.load("    123,   124 ,45  ,  4")

        self.assertTrue(integer_list.integers[0].value == 123)
        self.assertTrue(integer_list.integers[1].value == 124)
        self.assertTrue(integer_list.integers[2].value == 45)
        self.assertTrue(integer_list.integers[3].value == 4)
        
    def testReal(self):
        pass

    def testString(self):
        pass

    def testExpression(self):
        pass

    def testEquation(self):
        pass

class testTokens(unittest.TestCase):
    def setUp(self):
        pass

    def testIdent(self):

        self.assertTrue(isinstance(Ident("algo"), Ident))
        self.assertTrue(isinstance(Ident("_algo"), Ident))
        self.assertTrue(isinstance(Ident("Algo"), Ident))

        self.assertRaises(Exception, lambda: Ident(" algo asi "))
        

if __name__ == '__main__':
    unittest.main()
