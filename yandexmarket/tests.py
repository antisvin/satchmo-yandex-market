"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import datetime
import unittest
from xml.etree import ElementTree as et
from yandexmarket import utils
#from django.test import TestCase

class SimpleTest(unittest.TestCase):
    fixtures = []
    
    def setUp(self):
        self.yml = utils.YMLGenerator('http://example.com')
        
    def test_get_root(self):
        date = datetime.datetime(2010, 1, 2, 3, 45)
        self.assertEquals(
            et.tostring(self.yml.get_root_elt(date)),
            '<yml_catalog date="2010-01-02 03:45" />')

