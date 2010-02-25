"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import unittest
from yandexmarket import utils
#from django.test import TestCase

class SimpleTest(unittest.TestCase):
    fixtures = []
    
    def setUp(self):
        self.yml = utils.YMLGenerator('http://example.com')
        


__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

