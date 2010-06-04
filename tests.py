import unittest
from tokens import IDENT, QIDENT, STRING, UNSIGNED_INTEGER, UNSIGNED_NUMBER
from base import IncorrectValue, ParseError


class testTokensLoad(unittest.TestCase):
    def setUp(self):
        pass

    def test_ident(self):
        self.assertTrue(IDENT.load("algo").value == "algo")
        self.assertTrue(IDENT.load("Algo").value == "Algo")
        self.assertTrue(IDENT.load("_algo").value == "_algo")
        self.assertTrue(IDENT.load("  _algo  ").value == "_algo")
        self.assertTrue(IDENT.load("  'algo'  ").value == "'algo'")

        self.assertRaises(ParseError, lambda: IDENT.load("1algo"))


    def test_qident(self):
        self.assertTrue(IDENT.load("'algoas'").value == "'algoas'")


    def test_string(self):
        self.assertTrue(STRING.load(""" "algo" """).value == "algo")
        self.assertTrue(STRING.load(""" "algo y algo" """).value == "algo y algo")
        self.assertTrue(STRING.load(""" "algo es \\"algo\\"" """).value == '''algo es "algo"''')
        
    def test_integer(self):
        self.assertTrue(UNSIGNED_INTEGER.load(" 123     ").value == 123)


    def test_number(self):
        self.assertEqual(UNSIGNED_NUMBER.load("  12e-12").dump(), "12e-12")
        self.assertEqual(UNSIGNED_NUMBER.load("  12E+12").dump(), "12e12")


    def test_expression(self):
        pass

    def test_equation(self):
        pass

class testTokens(unittest.TestCase):
    def setUp(self):
        pass

    def test_ident(self):

        self.assertTrue(isinstance(IDENT("algo"), IDENT))
        self.assertTrue(isinstance(IDENT("_algo"), IDENT))
        self.assertTrue(isinstance(IDENT("Algo"), IDENT))

        self.assertRaises(Exception, lambda: IDENT(" algo asi "))

    def test_qident(self):

        self.assertTrue(isinstance(QIDENT("'algo'"), QIDENT))
        self.assertTrue(isinstance(QIDENT("'_algo'"), QIDENT))
        self.assertTrue(isinstance(QIDENT("'Algo'"), QIDENT))

        self.assertRaises(Exception, lambda: QIDENT("' algo asi "))



class testTokensDumps(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_ident(self):
        self.assertEqual(IDENT("algo").dump(), "algo") 

    def test_string(self):
        self.assertEqual(STRING("algo y algo").dump(), '''"algo y algo"''') 

    def test_integer(self):
        self.assertEqual(UNSIGNED_INTEGER("12").dump(), '''12''') 

        

if __name__ == '__main__':
    unittest.main()
