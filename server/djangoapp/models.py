from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    set = models.CharField(max_length=255)
    description = models.TextField()
    card_type = models.CharField(max_length=255)
    bodyType = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    image_url = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)  # Add this field

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

@receiver(post_save, sender=Order)
def upload_order(sender, instance, created, **kwargs):
    if created:
        order_data = {
            'order_id': instance.id,
            'user_id': instance.user.id,
            'total_price': float(instance.total_price),
            'order_items': [
                {
                    'product_id': item.product.id,
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'total': float(item.price * item.quantity)
                }
                for item in instance.items.all()
            ]
        }
        # Upload order data to remote server
        try:
            response = requests.post('https://example.com/api/orders', json=order_data)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f'Failed to upload order: {e}')

        # Update product quantity
        for item in instance.items.all():
            item.product.quantity -= item.quantity
            item.product.save()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class CardModel(models.Model):
    card = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CARD_TYPES = [
        ('Graded', 'Graded'),
        ('Singles', 'Singles'),
        ('Boxes','Boxes')
    ]
    type = models.CharField(max_length=10, choices=CARD_TYPES, default='PACK')

    def __str__(self):
        return self.name