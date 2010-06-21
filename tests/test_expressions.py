import unittest

from expressions import Annotation, StringComment, Comment, Subscript, ArraySubscripts, ExpressionList, OutputExpressionList, NamedArgument, NamedArguments

class testExpressions(unittest.TestCase):
    def setUp(self):
        pass

    def test_annotation(self):
        annotation = Annotation.load("  annotation   1")
        self.assertEqual(annotation.dump(), "annotation 1")
        
    def test_string_comment(self):
        string_comment = StringComment.load(' "comment1"  ')
        self.assertEqual(string_comment.dump(),  '"comment1"')

        string_comment = StringComment.load(' "comment1"  +  "comment2" ')
        self.assertEqual(string_comment.dump(),  '"comment1" + "comment2"')

    def test_comment(self):
        comment = Comment.load(' "comment1"  +  "comment2" ')
        self.assertEqual(comment.dump(), '"comment1" + "comment2"')

        comment = Comment.load(' "comment1"  +  "comment2"    annotation    1  ')
        self.assertEqual(comment.dump(), '"comment1" + "comment2" annotation 1')

    def test_subscript(self):
        subscript = Subscript.load(":")
        self.assertEqual(subscript.dump(), ":")

        subscript = Subscript.load("i")
        self.assertEqual(subscript.dump(), "i")

    def test_array_subscripts(self):
        array_subscripts = ArraySubscripts.load("[:]")
        self.assertEqual(array_subscripts.dump(), "[:]")

        array_subscripts = ArraySubscripts.load("[i]")
        self.assertEqual(array_subscripts.dump(), "[i]")

        array_subscripts = ArraySubscripts.load("[i,j,k]")
        self.assertEqual(array_subscripts.dump(), "[i, j, k]")

    def test_expression_list(self):
        expression_list = ExpressionList.load("i")
        self.assertEqual(expression_list.dump(), "i")

        expression_list = ExpressionList.load("i,  j")
        self.assertEqual(expression_list.dump(), "i, j")

        expression_list = ExpressionList.load(" i  ,  j   ,   k ")
        self.assertEqual(expression_list.dump(), "i, j, k")

    def test_output_expression_list(self):
        output_expression_list = OutputExpressionList.load("i")
        self.assertEqual(output_expression_list.dump(), "i")

        output_expression_list = OutputExpressionList.load("i,  j")
        self.assertEqual(output_expression_list.dump(), "i, j")

        output_expression_list = OutputExpressionList.load(" i  ,  j   ,   k ")
        self.assertEqual(output_expression_list.dump(), "i, j, k")

    def test_named_argument(self):
        named_argument = NamedArgument.load("algo   =   i")
        self.assertEqual(named_argument.dump(), "algo = i")


    def test_named_arguments(self):
        named_arguments = NamedArguments.load("algo   =   i")
        self.assertEqual(named_arguments.dump(), "algo = i")
        
        named_arguments = NamedArguments.load("algo   =   i, otro   =  j")
        self.assertEqual(named_arguments.dump(), "algo = i, otro = j")

    def test_function_arguments(self):
        function_arguments = FunctionArguments.load("i")
        self.assertEqual(function_arguments.dump(), "i")

        function_arguments = FunctionArguments.load("i, i")
        self.assertEqual(function_arguments.dump(), "i, i")

        function_arguments = FunctionArguments.load("i for i in j")
        self.assertEqual(function_arguments.dump(), "i for i in j")

        function_arguments = FunctionArguments.load("algo = i")
        self.assertEqual(function_arguments.dump(), "algo = i")

    
        

if __name__ == '__main__':
    unittest.main()
