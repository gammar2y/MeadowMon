from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path(‘requests/’, TemplateView.as_view(template_name="index.html")),
    path(‘cart/’, TemplateView.as_view(template_name="index.html")),
    path(‘checkout/’, TemplateView.as_view(template_name="index.html")),
    path(‘order_confirmation/’, TemplateView.as_view(template_name="index.html")),
    path('get_product/', TemplateView.as_view(template_name="index.html")),
   
    path(
        'get_product_details/<int:product_id>',
        TemplateView.as_view(template_name="index.html")
    ),
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

