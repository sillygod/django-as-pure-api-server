from django.test import TestCase

from injury.models import Injury


class InjuryTestCase(TestCase):


    def setUp(self):
        pass

    def test_create(self):
        work = Injury.objects.create(name="work")
        actress = Injury.objects.create(name="actress", parent=work)
        woman = Injury.objects.create(name='woman', parent=actress)
        throat = Injury.objects.create(name='throat', parent=work)
