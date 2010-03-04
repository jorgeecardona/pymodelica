import unittest

class testTokens(unittest.TestCase):
    def setUp(self):
        pass

    def testInteger(self):
        from Modelica import Integer

        self.assertTrue(Integer.load(" 123     ").value == 123)


    def testIntegerList(self):
        from Modelica import IntegerList

        integer_list = IntegerList.load("    123,   124 ,45  ,  4")

        self.assertTrue(integer_list.integers[0].value == 123)
        self.assertTrue(integer_list.integers[1].value == 124)
        self.assertTrue(integer_list.integers[2].value == 45)
        self.assertTrue(integer_list.integers[3].value == 4)
        
    def testReal(self):
        from Modelica import Real

        pass

    def testString(self):
        from Modelica import String

        pass

    def testExpression(self):
        from Modelica import Expression

        pass

    def testEquation(self):
        from Modelica import Equation

        pass



if __name__ == '__main__':
    unittest.main()
