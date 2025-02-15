import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoapp.models import Product
import logging

class Command(BaseCommand):
    help = 'Load products from a JSON file'

    def handle(self, *args, **kwargs):
        # Enable logging
        logging.basicConfig(level=logging.DEBUG)
        
        # Path to the products.json file
        json_file_path = os.path.join(settings.BASE_DIR, 'database/data/products.json')
        
        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Extract products from the JSON data
        products = data.get('products', [])
        
        # Load products into the database
        for product_data in products:
            try:
                Product.objects.update_or_create(
                    id=product_data['id'],
                    defaults={
                        'name': product_data['name'],
                        'price': product_data['price'],
                        'set': product_data['set'],
                        'description': product_data['description'],
                        'card_type': product_data['card_type'],
                        'bodyType': product_data['bodyType'],
                        'year': product_data['year'],
                        'image_url': product_data['image_url'],
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded product: {product_data["name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading product: {product_data["name"]}'))
                self.stdout.write(self.style.ERROR(str(e)))