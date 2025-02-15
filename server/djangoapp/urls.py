from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoproj import views

app_name = 'djangoapp'
urlpatterns = [
    path('api/register', views.registration, name='registration'),
    path('api/logout', views.logout, name='logout'),
    path('api/login', views.login_user, name='login'),
    path('api/requests', views.login_user, name='requests'),
    path('api/checkout', views.login_user, name='checkout'),
    path('api/cart', views.login_user, name='cart'),
    path('api/order_confirmation', views.login_user, name='order_confirmation'),
    path('api/get_product', views.get_product, name='getproduct'),
    path('api/get_product_details/', views.product_detail, name='get_product_details'),
    path('api/get_product/get_product_details/<int:id>', views.product_detail, name='product_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)