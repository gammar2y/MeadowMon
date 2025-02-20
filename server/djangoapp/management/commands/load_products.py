import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoapp.models import Product
import logging
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Load products from a JSON file into both MongoDB and Django ORM'

    def handle(self, *args, **kwargs):
        # Enable logging
        logging.basicConfig(level=logging.DEBUG)

        # Path to the products.json file
        json_file_path = os.path.join(settings.BASE_DIR, 'database/data/products.json')

        # Verify the JSON file path
        self.stdout.write(self.style.SUCCESS(f"Loading products from: {json_file_path}"))

        # Read the JSON file
        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: The file {json_file_path} was not found."))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error: Failed to decode JSON file. {str(e)}"))
            return

        # Extract products from the JSON data
        products = data.get('products', [])

        # Verify the products data
        self.stdout.write(self.style.SUCCESS(f"Found {len(products)} products in the JSON file."))

        # Load products into the Django ORM
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
                        'quantity': product_data['quantity'],
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded product into Django ORM: {product_data["name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading product into Django ORM: {product_data["name"]}'))
                self.stdout.write(self.style.ERROR(str(e)))

        # MongoDB connection URI
        uri = "mongodb+srv://meadowmonbusiness:NXVwZOXBQChb01uj@meadowmon.zcf42.mongodb.net/MeadowMon?retryWrites=true&w=majority"

        # Connect to MongoDB
        client = MongoClient(uri)
        db = client.MeadowMon
        products_collection = db.products

        # Load products into MongoDB
        for product_data in products:
            try:
                products_collection.update_one(
                    {'id': product_data['id']},
                    {'$set': product_data},
                    upsert=True
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded product into MongoDB: {product_data["name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading product into MongoDB: {product_data["name"]}'))
                self.stdout.write(self.style.ERROR(str(e)))

        self.stdout.write(self.style.SUCCESS("Products have been loaded into both Django ORM and MongoDB."))