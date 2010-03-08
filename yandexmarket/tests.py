"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import datetime
from django import test
from django.conf import settings
from django.core import urlresolvers
from xml.etree import ElementTree as et
from yandexmarket import utils


class SimpleTest(test.TestCase):
    fixtures = (
        'sample-store-data.yaml', 'yandexmarket_products.yaml',
        'test-config.yaml')
    
    def setUp(self):
        self.yml = utils.YMLGenerator('example.com')
        self.mock = et.Element('mock')
        settings.YANDEXMARKET_CURRENCIES = ('USD', 'EUR')
        settings.YANDEXMARKET_DEFAULT_CURRENCY = 'USD'
        
    def test_get_root(self):
        date = datetime.datetime(2010, 1, 2, 3, 45)
        elt = self.yml.get_root_elt(date)
        elt.append(self.mock)
        self.assertEquals(
            et.tostring(elt),
            '<yml_catalog date="2010-01-02 03:45"><mock /></yml_catalog>')

    def test_get_shop(self):
        elt = self.yml.get_shop_elt()
        self.assertEquals(
            et.tostring(elt),
            ('<shop><name>My Site - Trunk</name><company>example.com</company>'
             '<url>http://example.com/</url></shop>'))

    def test_get_currencies(self):
        elt = self.yml.get_currencies_elt()
        self.assertEquals(
            et.tostring(elt),
            ('<currencies><currency id="RUR" rate="1" />'
             '<currency id="USD" rate="CBRF" />'
             '<currency id="EUR" rate="CBRF" /></currencies>'))

    def test_get_categories(self):
        elt = self.yml.get_categories_elt()
        self.assertEquals(
            et.tostring(elt),
            ('<categories><category id="3">Books</category>'
             '<category id="4" parentId="3">Fiction</category>'
             '<category id="8">Hardware</category></categories>'))
        
    def test_get_offers(self):
        elt = self.yml.get_offers_elt()
        self.assertEquals(
            et.tostring(elt),
            ('<offers>'
             '<offer available="false" id="3">'
             '<url>http://example.com/store/product/neat-book/</url>'
             '<price>5.00</price><currencyId>USD</currencyId>'
             '<categoryId>4</categoryId><typePrefix>Fiction</typePrefix>'
             '<name>A really neat book</name><model>nb123</model>'
             '<delivery>true</delivery>'
             '<description>A neat book.  You should buy it.</description>'
             '<downloadable>false</downloadable>'
             '</offer>'
             '<offer available="false" id="15">'
             '<url>http://example.com/store/product/neat-book-hard/</url>'
             '<price>5.00</price><currencyId>USD</currencyId>'
             '<categoryId>3</categoryId><typePrefix>Books</typePrefix>'
             '<name>A really neat book (Hard cover)</name>'
             '<model>nb234</model>'
             '<delivery>true</delivery><downloadable>false</downloadable>'
             '</offer>'
             '<offer available="true" id="30">'             
             '<url>http://example.com/store/product/satchmo-computer/</url>'
             '<price>123.00</price><currencyId>USD</currencyId>'
             '<categoryId>8</categoryId><typePrefix>Hardware</typePrefix>'
             '<name>satchmo computer</name>'
             '<model>satch-1</model>'
             '<delivery>true</delivery>'
             '<description>Satchmo computer. It does it all!</description>'
             '<sales_notes>Not much else to say.</sales_notes>'
             '<downloadable>false</downloadable></offer>'
             '</offers>'))
        
    def test_generate(self):
        """
        We simple concatenate tested elements here, so for now we just make
        sure that there's no runtime errors.
        """
        self.yml.generate()

    def test_no_settings(self):
        del settings.YANDEXMARKET_CURRENCIES
        del settings.YANDEXMARKET_DEFAULT_CURRENCY

        elt = self.yml.get_currencies_elt()
        self.assertEquals(
            et.tostring(elt),
            '<currencies><currency id="RUR" rate="1" /></currencies>')
        
        elt = self.yml.get_offers_elt()
        self.assertEquals(
            et.tostring(elt),
            ('<offers>'
             '<offer available="false" id="3">'
             '<url>http://example.com/store/product/neat-book/</url>'
             '<price>5.00</price><currencyId>RUR</currencyId>'
             '<categoryId>4</categoryId><typePrefix>Fiction</typePrefix>'
             '<name>A really neat book</name><model>nb123</model>'
             '<delivery>true</delivery>'
             '<description>A neat book.  You should buy it.</description>'
             '<downloadable>false</downloadable>'
             '</offer><offer available="false" id="15">'
             '<url>http://example.com/store/product/neat-book-hard/</url>'
             '<price>5.00</price><currencyId>RUR</currencyId>'
             '<categoryId>3</categoryId><typePrefix>Books</typePrefix>'
             '<name>A really neat book (Hard cover)</name>'
             '<model>nb234</model><delivery>true</delivery>'
             '<downloadable>false</downloadable></offer>'
             '<offer available="true" id="30">'
             '<url>http://example.com/store/product/satchmo-computer/</url>'
             '<price>123.00</price><currencyId>RUR</currencyId>'
             '<categoryId>8</categoryId><typePrefix>Hardware</typePrefix>'
             '<name>satchmo computer</name>'
             '<model>satch-1</model>'
             '<delivery>true</delivery>'
             '<description>Satchmo computer. It does it all!</description>'
             '<sales_notes>Not much else to say.</sales_notes>'
             '<downloadable>false</downloadable></offer>'
             '</offers>'))


class ViewTest(test.TestCase):
    fixtures = (
        'sample-store-data.yaml', 'yandexmarket_products.yaml',
        'test-config.yaml')
    
    def test_generate_yml_view(self):
        response = self.client.get(
            urlresolvers.reverse('generate_yml'), HTTP_HOST='example.com')
        self.failUnlessEqual(response.status_code, 200)
        
