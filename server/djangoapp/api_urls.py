from django.urls import path
from . import api_views

urlpatterns = [
    path('fetchProduct/<int:id>/', api_views.fetch_product, name='fetch_product'),
]