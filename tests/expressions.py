import unittest

from expressions import Annotation


class testExpressions(unittest.TestCase):
    def setUp(self):
        pass


    def test_annotation(self):
        self.assertEqual(Annotation.load("annotation ja").dump, )
