import unittest
from tokens import Ident, String, Integer, IntegerList
from base import IncorrectValue, ParseError


class testTokensLoad(unittest.TestCase):
    def setUp(self):
        pass

    def testIdent(self):
        self.assertTrue(Ident.load("algo").value == "algo")
        self.assertTrue(Ident.load("Algo").value == "Algo")
        self.assertTrue(Ident.load("_algo").value == "_algo")
        self.assertTrue(Ident.load("  _algo  ").value == "_algo")
        self.assertTrue(Ident.load("  'algo'  ").value == "'algo'")

        self.assertRaises(ParseError, lambda: Ident.load("1algo"))


    def testQIdent(self):
        self.assertTrue(Ident.load("'algoas'").value == "'algoas'")


    def testString(self):
        self.assertTrue(String.load(""" "algo" """).value == "algo")
        self.assertTrue(String.load(""" "algo y algo" """).value == "algo y algo")
        self.assertTrue(String.load(""" "algo es \\"algo\\"" """).value == '''algo es "algo"''')
        
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

class testTokensDumps(unittest.TestCase):
    def setUp(self):
        pass
    
    def testIdent(self):
        self.assertEqual(Ident("algo").dump(), "algo") 

    def testString(self):
        self.assertEqual(String("algo y algo").dump(), '''"algo y algo"''') 

    def testInteger(self):
        self.assertEqual(Integer("12").dump(), '''12''') 

        

if __name__ == '__main__':
    unittest.main()
