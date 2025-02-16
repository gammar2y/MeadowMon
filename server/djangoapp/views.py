import json
import logging
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from djangoapp.product import Products
from djangoapp.cards import Cards
from djangoapp.populate import initiate
from djangoapp.restapis import get_request
from djangoapp.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from djangoapp.models import CartItem, Product
from django.conf import settings
import os

# logger instance
logger = logging.getLogger(__name__)

def index(request):
    # Path to the products.json file
    json_file_path = os.path.join(settings.BASE_DIR, 'database/data/products.json')
    
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Extract products from the JSON data
    products = data.get('products', [])
    
    # Pass the products to the template
    return render(request, 'index.html', {'products': products})

def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    return render(request, 'cart.html', {'cart_items': cart_items})

def add_to_cart(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
    return redirect('cart')

def update_cart(request, cart_item_id, quantity):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart')

def products(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'products': all_products})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the home page or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def get_product(request):
    count = Products.objects.count()
    if count == 0:
        initiate()

    product_list = Products.objects.select_related('category').all()
    products = [
        {
            "name": product.name,
            "price": product.price,
            "category": product.category.name,
            "description": product.description,
            "image": product.image.url
        }
        for product in product_list
    ]
    return JsonResponse({"products": products})

def login_user(request):
    """
    Handles user login.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the home page or any other page

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to the home page or any other page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def registration(request):
    """
    Handles user registration.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        User.objects.get(username=username)
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username, first_name=first_name,
            last_name=last_name, password=password, email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})


def product_requests(request):
    """
    Handles product requests.
    """
    data = json.loads(request.body)
    submission = data['requests']
    card_request = {
        "request": submission,
    }
    file_name = "requests.json"

    with open(file_name, 'w') as json_file:
        json.dump(submission, json_file, indent=4)
def product_detail(request, id):

    if id:
        endpoint = f"/fetchProduct/{id}"
        product = get_request(endpoint)
        return JsonResponse({"status": 200, "product": product})
    return JsonResponse({"status": 400, "message": "Bad Request"})

def submit_order(request):
    """
    Handles order submission.
    """
    data = json.loads(request.body)
    order_details = data.get('orderDetails', {})
    # Process the order details here
    return JsonResponse({"status": "Order submitted successfully", "orderDetails": order_details})