import json
import requests
import logging
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from djangoapp.product import Products
from djangoapp.cards import Cards
from djangoapp.populate import initiate
from djangoapp.forms import SearchForm
from djangoapp.restapis import get_request
from djangoapp.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from djangoapp.models import CartItem, Product, Order, OrderItem
from django.contrib import messages
from django.conf import settings
from djangoapp.utils import DecimalEncoder
from decimal import Decimal
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

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    if product.quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Handle the case where the user tries to add more than the available quantity
            messages.warning(request, "Maximum Quantity")
    else:
        # Handle the case where the product is out of stock
        messages.error(request, "Out of Stock! Check back soon.")
    return redirect('cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)

        order_items = []
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            order_items.append({
                'product_id': item.product.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.product.price),
                'total': float(item.product.price * item.quantity)
            })
            item.delete()  # Remove the item from the cart

        # Collect billing and shipping information
        billing_info = {
            'card_number': request.POST['card_number'],
            'card_expiry': request.POST['card_expiry'],
            'card_cvc': request.POST['card_cvc']
        }
        shipping_address = {
            'address': request.POST['address'],
            'city': request.POST['city'],
            'state': request.POST['state'],
            'zip_code': request.POST['zip_code']
        }

        # Process payment using transaction API
        payment_data = {
            'card_number': billing_info['card_number'],
            'card_expiry': billing_info['card_expiry'],
            'card_cvc': billing_info['card_cvc'],
            'amount': total_price,
            'currency': 'USD'
        }
        try:
            response = requests.post('https://example.com/api/transactions', json=payment_data)
            response.raise_for_status()
            payment_response = response.json()
            if payment_response['status'] != 'success':
                return render(request, 'checkout.html', {'error': 'Payment failed. Please try again.'})
        except requests.RequestException as e:
            return render(request, 'checkout.html', {'error': f'Payment failed: {e}'})

        # Create the order data
        order_data = {
            'order_id': order.id,
            'user_id': request.user.id,
            'total_price': float(total_price),
            'order_items': order_items,
            'billing_info': billing_info,
            'shipping_address': shipping_address
        }

        # Save the order data to a JSON file
        json_file_path = os.path.join(settings.BASE_DIR, 'orders', f'order_{order.id}.json')
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        with open(json_file_path, 'w') as json_file:
            json.dump(order_data, json_file, indent=4, cls=DecimalEncoder)

        return redirect('order_confirmation', order_id=order.id)
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def search_view(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'search_results.html', {'form': form, 'products': products})

def get_fedex_oauth_token():
    url = "https://apis-sandbox.fedex.com/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': 'l75723e60ed5cb4a7891f8ed2514c46ca2',
        'client_secret': 'b145cb90a17d444583cfab086ca5f60c'
    }
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    response_data = response.json()
    
    if response.status_code == 200 and 'access_token' in response_data:
        return response_data['access_token']
    else:
        logger.error(f"Failed to get OAuth token: {response_data}")
        raise KeyError("access_token not found in the response or invalid credentials")

def calculate_shipping(request):
    zip_code = request.GET.get('zip_code')
    origin_postal_code = '80917'

    try:
        # Get OAuth token
        access_token = get_fedex_oauth_token()
    except KeyError as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Correct FedEx API URL for rate quotes
    fedex_api_url = 'https://apis-sandbox.fedex.com/rate/v1/rates/quotes'

    payload = {
        "accountNumber": "203687906",
        "requestedShipment": {
            "shipper": {
                "address": {
                    "postalCode": origin_postal_code,
                    "countryCode": "US"
                }
            },
            "recipient": {
                "address": {
                    "postalCode": zip_code,
                    "countryCode": "US"
                }
            },
            "packageCount": 1,
            "requestedPackageLineItems": [
                {
                    "weight": {
                        "units": "LB",
                        "value": 1.0
                    }
                }
            ]
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(fedex_api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            shipping_cost = data['rateReplyDetails'][0]['ratedShipmentDetails'][0]['totalNetCharge']['amount']
            return JsonResponse({'shipping_cost': shipping_cost})
        except (ValueError, KeyError, IndexError) as e:
            return JsonResponse({'error': 'Failed to parse shipping cost from response', 'details': str(e)}, status=500)
    else:
        # Log the response content for debugging
        logger.error(f"Failed to get shipping cost: {response.content}")
        return JsonResponse({'error': 'Failed to get shipping cost', 'status_code': response.status_code, 'details': response.content.decode('utf-8')}, status=response.status_code)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    if request.is_ajax():
        return JsonResponse({'success': True})
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def update_cart(request):
    if request.method == 'POST':
        for item in CartItem.objects.filter(user=request.user):
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('checkout')
    return redirect('cart')

def calculate_tax(request):
    total_price = float(request.GET.get('total_price', 0))
    tax_rate = 0.082  # Example tax rate of 7%
    tax_cost = total_price * tax_rate
    return JsonResponse({'tax_cost': tax_cost})

def products(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {'products': all_products})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

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
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

def submit_order(request):
    """
    Handles order submission.
    """
    data = json.loads(request.body)
    order_details = data.get('orderDetails', {})
    # Process the order details here
    return JsonResponse({"status": "Order submitted successfully", "orderDetails": order_details})