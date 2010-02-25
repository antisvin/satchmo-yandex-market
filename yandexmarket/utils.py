import datetime
from satchmo_store.models import Config
from xml.etree import ElementTree as et


class YMLGenerator(objects):
    def __init__(self, domain):
        self.domain = domain
        self.config = None
        
    def get_header(self):
        """
        Returns YML header.
        """
        return '''
        <?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE yml_catalog SYSTEM "shops.dtd">
        '''

    def get_root_elt(self, date=None):
        if date is None:
            date = datetime.datetime.now()
        return et.Element("yml_catalog", date=date.strftime('%Y-%m-%d %H:%M'))

    def get_shop_elt(self, root):
        self.config = Config.objects.get(site__domain_name=self.domain)
        
        shop_elt = et.SubElement(root, "shop")
        et.SubElement(shop_elt, "name").text = self.config.store_name
        et.SubElement(shop_elt, "company").text = self.config.site.display_name
        et.SubElement(shop_elt, "url").text = self.domain_name

        return shop_elt
    
    def get_categories_elt(self, shop_elt):
        categories_elt = et.SubElement(shop_elt, "categories")
        top_categories = config.site.category_set.filter(
            parent__isnull=True, is_active=True)
        for top_category in top_categories:
            et.SubElement(
                categories_elt, "category", id=top_category.pk
                ).text = top_category.name
            
            for subcategory in top_category.get_active_children():
                et.SubElement(
                    categories_elt, "category", id=subcategory.pk
                    ).text = subcategory.name

        return categories_elt

    def get_offers_elt(self, shop_elt):
        offers_elt = et.SubElement(shop_elt, "offers")
        for product in self.config.product_set.filter(active=True):
            offer_elt = et.SubElement(
                offers_elt, "offer", id=product.id, available="true")
            et.SubElement(offer_elt, "url").text = ''.join((
                'http://', self.domain, product.get_absolute_url()))
            et.SubElement(offer_elt, "price").text = product.get_qty_price(1)
            et.SubElement(
                offer_elt, "currencyId"
                ).text = settings.YANDEX_DEFAULT_CURRENCY

            category = product.category_set.all()[0]
            et.SubElement(offer_elt, "categoryId").text = category.pk

            if self.productimage_set.count() > 0:
                img = self.productimage_set.order_by('sort')[0]
                et.SubElement(offer_elt, "picture").text = ''.join((
                    'http://', self.domain, img.picture.url))

            et.SubElement(offer_elt, "typePrefix").text = category.name
            et.SubElement(offer_elt, "name").text = product.name
            et.SubElement(offer_elt, "delivery").text = "true"
            et.SubElement(offer_elt, "description").text = product.description
            et.SubElement(offer_elt, "available").text = unicode(
                product.items_in_stock > 0).lower()
            et.SubElement(
                offer_elt, "sales_notes").text = product.short_description
            et.SubElement(offer_elt, "downloadable").text = "false"
                
    def generate():
        """
        Returns YML representatio of all shops data.
        """
