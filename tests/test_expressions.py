import unittest

from expressions import Annotation, StringComment, Comment, Subscript, ArraySubscripts

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


if __name__ == '__main__':
    unittest.main()
