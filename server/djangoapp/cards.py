from django.db import models
from .category import Category

class Cards(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/cards/')
    year = models.IntegerField(default=2021)  # Added year field

    @staticmethod
    def get_cards_by_id(ids):
        return Cards.objects.filter(id__in=ids)

    @staticmethod
    def get_all_cards():
        return Cards.objects.all()

    @staticmethod
    def get_all_cards_by_categoryid(category_id):
        if category_id:
            return Cards.objects.filter(category=category_id)
        else:
            return Cards.get_all_cards()