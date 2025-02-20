from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product

def fetch_product(request, id):
    product = get_object_or_404(Product, id=id)
    product_data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'image_url': product.image_url,
    }
    return JsonResponse(product_data)