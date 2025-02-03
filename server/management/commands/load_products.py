from django.core.management.base import BaseCommand
from djangoapp.models import Product
import json

class Command(BaseCommand):
    help = 'Load products from a JSON file'

    def handle(self, *args, **kwargs):
        with open('path/to/products.json') as f:
            products = json.load(f)
            for product_data in products:
                Product.objects.create(**product_data)
            self.stdout.write(self.style.SUCCESS('Successfully loaded products'))