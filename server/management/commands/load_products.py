import json
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoapp.models import Product

class Command(BaseCommand):
    help = 'Load products from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = settings.BASE_DIR / 'database/data/products.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data['products']:
                Product.objects.create(
                    id=item['product_id'],
                    name=item['name'],
                    price=item['price'],
                    image_url=item.get('image_url', 'default.jpg'),  # Add a default image URL if not provided
                    description=item.get('description', ''),
                    card_type=item.get('card_type', ''),
                    bodyType=item.get('bodyType', ''),
                    year=item.get('year', '')
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))