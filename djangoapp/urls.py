from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name= ‘djangoapp’
urlpatterns = [
	path(route=’register’, view=views.registration, name=’registration’),
	path(route=’logout’, view=views.logout, name=’logout’)
	path(route=’login’, view=views.login_user, name=’login’)
	path(route=’requests’ view=views.login_user, name=’requests’)
	path(route=’checkout’ view=views.login_user, name=’checkout’)
	path(route=’cart’ view=views.login_user, name=’cart’)
	path(route=’order_confirmation’ view=views.login_user, name=’order_confirmation’)
	path(route=’get_product’, view=views.get_product, name=’getproduct’)
	path(route=’get_product_details/’, view=views.get_product_details, name=’get_product_details’)
path(
	route=’get_product/get_product_details/<int:product_id>’,
	view=views.get_product_details,
	name=’product_details’
),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
