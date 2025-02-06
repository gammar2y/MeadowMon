from django.core.management.base import BaseCommand
from djangoapp.models import Product
import json
import os

class Command(BaseCommand):
    help = 'Load products from a JSON file'

    def handle(self, *args, **kwargs):
        # Construct the path to the JSON file
        json_file_path = os.path.join('database', 'data', 'products.json')

        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                products = data.get('products', [])
                for product_data in products:
                    if isinstance(product_data, dict):
                        required_fields = ['product_id', 'name', 'price', 'set', 'description', 'card_type', 'bodyType', 'year', 'image_url']
                        missing_fields = [field for field in required_fields if field not in product_data]
                        if not missing_fields:
                            self.stdout.write(self.style.SUCCESS(f"Product data: {product_data}"))
                            Product.objects.update_or_create(
                                product_id=product_data['product_id'],
                                defaults=product_data
                            )
                        else:
                            self.stdout.write(self.style.ERROR(f"Missing fields {missing_fields} in product data: {product_data}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Invalid data format: {product_data}"))
                self.stdout.write(self.style.SUCCESS('Successfully loaded products'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {json_file_path}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON"))