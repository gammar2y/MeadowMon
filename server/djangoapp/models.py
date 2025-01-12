from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


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

