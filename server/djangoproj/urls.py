from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('requests/', TemplateView.as_view(template_name="index.html")),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search_view, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('calculate_tax/', views.calculate_tax, name='calculate_tax'),
    path('calculate_shipping/', views.calculate_shipping, name='calculate_shipping'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('order_confirmation/', TemplateView.as_view(template_name="index.html")),
    path('get_product/', views.products, name="products.html"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('products/', views.products, name='products'),
    path('', views.index, name='index'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),
    path('admin/', admin.site.urls),
    path('api/', include('djangoapp.api_urls')),  # Include the api_urls.py
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)