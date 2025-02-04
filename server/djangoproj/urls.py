from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('requests/', TemplateView.as_view(template_name="index.html")),
    path('cart/', views.cart, name='cart'),  # Updated to use the view function
    path('checkout/', TemplateView.as_view(template_name="index.html")),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/<int:quantity>/', views.update_cart, name='update_cart'),
    path(
        'order_confirmation/', TemplateView.as_view(template_name="index.html")
        ),
    path('get_product/', TemplateView.as_view(template_name="index.html")),
    path(
        'get_product_details/<int:product_id>/', TemplateView.as_view(template_name="index.html")
        ),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('products/', views.products, name='products'),  # Added URL pattern for products page
    path('', views.index, name='index'),  # Updated to use the view function
    
    path(
        'favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')
        ),
    
    path('admin/', admin.site.urls),

    path('api/', include('djangoapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

