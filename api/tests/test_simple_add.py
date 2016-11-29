from django.test import TestCase


class SimpleTestCase(TestCase):

    def SetUp(self):
        pass

    def test_one_plus_one(self):
        self.assertEqual(1+1, 2)
