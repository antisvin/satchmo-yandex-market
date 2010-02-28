"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import datetime
from django import test
from xml.etree import ElementTree as et
from yandexmarket import utils
#from django.test import TestCase

class SimpleTest(test.TestCase):
    fixtures = ['sample-store-data.yaml', 'products.yaml', 'test-config.yaml']
    
    def setUp(self):
        self.yml = utils.YMLGenerator('example.com')
        self.mock = et.Element('mock')
        
    def test_get_root(self):
        date = datetime.datetime(2010, 1, 2, 3, 45)
        elt = self.yml.get_root_elt(date)
        elt.append(self.mock)
        self.assertEquals(
            et.tostring(elt),
            '<yml_catalog date="2010-01-02 03:45"><mock /></yml_catalog>')

    def test_get_shop(self):
        elt = self.yml.get_shop_elt(self.mock)
        self.assertEquals(
            et.tostring(self.mock),
            ('<mock><shop><name>My Site - Trunk</name>'
             '<company>example.com</company><url>http://example.com/</url>'
             '</shop></mock>'))

    def test_get_categories(self):
        pass

    def test_get_offers(self):
        pass

    
