"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import heroku

from django.test import TestCase
from models import OurUser, Inst
from tasks import create_instance, init_tutorial
from django.conf import settings


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HerokuTest(TestCase):
    def setUp(self):
        self.cloud = heroku.from_key(settings.HEROKU_KEY)
        if 'rocket-1-1' in [x.name for x in self.cloud.apps]:
            self.cloud.apps['rocket-1-1'].destroy()

        self.user = OurUser.objects.get(id=1)
        self.name = create_instance(self.user)

    def test_status(self):
        inst = Inst.objects.get(app=self.name)
        self.assertEqual(inst.status, 'new')

    def test_exists(self):
        names = [x.name for x in self.cloud.apps]
        self.assertIn(self.name, names)

    def test_init_tutorial(self):
        inst = Inst.objects.get(app=self.name)
        init_tutorial(inst, 1)


