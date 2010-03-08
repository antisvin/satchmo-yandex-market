import datetime
from django.conf import settings
from satchmo_store.shop.models import Config
from xml.etree import ElementTree as et


class YMLGenerator(object):
    """
    Generates YML file for given domain.
    """
    
    header = '''
        <?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE yml_catalog SYSTEM "shops.dtd">
        '''

    def __init__(self, domain):
        """
        @domain: domain for which we generate data.
        @type domain: unicode
        """
        self.domain = domain
        self.config = Config.objects.get(site__domain=self.domain)
        
    def get_root_elt(self, date=None):
        """
        Create root element.

        @date: date and time to use. If not set, uses current datetime.
        @type date: datetime.datetime
        """
        if date is None:
            date = datetime.datetime.now()
        return et.Element("yml_catalog", date=date.strftime('%Y-%m-%d %H:%M'))

    def get_shop_elt(self):
        shop_elt = et.Element("shop")
        et.SubElement(shop_elt, "name").text = self.config.store_name
        et.SubElement(shop_elt, "company").text = self.config.site.name
        et.SubElement(shop_elt, "url").text = 'http://%s/' % self.domain

        return shop_elt

    def get_currencies_elt(self):
        currencies_elt = et.Element("currencies")
        et.SubElement(currencies_elt, "currency", id="RUR", rate="1")
        
        for currency in getattr(settings, 'YANDEXMARKET_CURRENCIES', ()):
            et.SubElement(
                currencies_elt, "currency", id=currency, rate="CBRF")

        return currencies_elt
    
    def get_categories_elt(self):
        categories_elt = et.Element("categories")
        top_categories = self.config.site.category_set.filter(
            parent__isnull=True, is_active=True)
        for top_category in top_categories:
            et.SubElement(
                categories_elt, "category", id=unicode(top_category.pk)
                ).text = top_category.name
            
            for subcategory in top_category.get_active_children():
                et.SubElement(
                    categories_elt, "category", id=unicode(subcategory.pk),
                    parentId=unicode(subcategory.parent.id)
                    ).text = subcategory.name

        return categories_elt

    def get_offers_elt(self):
        offers_elt = et.Element("offers")
        for product in self.config.site.product_set.filter(
            active=True, category__isnull=False):
            offer_elt = et.SubElement(
                offers_elt, "offer", id=unicode(product.id), available="true")
            et.SubElement(offer_elt, "url").text = ''.join((
                'http://', self.domain, product.get_absolute_url()))
            et.SubElement(offer_elt, "price").text = unicode(product.get_qty_price(1))
            et.SubElement(
                offer_elt, "currencyId"
                ).text = getattr(settings, 'YANDEXMARKET_DEFAULT_CURRENCY', 'RUR')

            category = product.category.all()[0]
            et.SubElement(offer_elt, "categoryId").text = unicode(category.pk)

            if product.productimage_set.count() > 0:
                img = product.productimage_set.order_by('sort')[0]
                et.SubElement(offer_elt, "picture").text = ''.join((
                    'http://', self.domain, img.picture.url))

            et.SubElement(offer_elt, "typePrefix").text = category.name
            et.SubElement(offer_elt, "name").text = product.name
            et.SubElement(offer_elt, "delivery").text = "true"

            if product.description:
                et.SubElement(offer_elt, "description").text = product.description

            et.SubElement(offer_elt, "available").text = unicode(
                product.items_in_stock > 0).lower()

            if product.short_description:
                et.SubElement(
                    offer_elt, "sales_notes").text = product.short_description
            et.SubElement(offer_elt, "downloadable").text = "false"

        return offers_elt
                
    def generate(self):
        """
        Returns YML representatio of all shops data.
        """
        root = self.get_root_elt()

        shop = self.get_shop_elt()
        root.append(shop)

        shop.append(self.get_currencies_elt())
        shop.append(self.get_categories_elt())
        shop.append(self.get_offers_elt())
        
        return self.header + et.tostring(root)
