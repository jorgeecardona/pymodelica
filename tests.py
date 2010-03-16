import unittest
from tokens import Ident, String, Integer, Number
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


    def testNumber(self):
        self.assertEqual(Number.load("  12e-12").dump(), "12e-12")
        self.assertEqual(Number.load("  12E+12").dump(), "12e12")


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
