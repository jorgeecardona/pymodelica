import unittest

from expressions import Annotation, StringComment, Comment, Subscript

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


if __name__ == '__main__':
    unittest.main()
