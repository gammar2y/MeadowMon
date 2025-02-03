from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    set = models.CharField(max_length=255)
    description = models.TextField()
    card_type = models.CharField(max_length=255)
    bodyType = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    image_url = models.URLField(max_length=200)

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

