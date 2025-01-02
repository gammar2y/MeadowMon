import json
import logging
from  django.http import JsonResponse
from Django.contrib.auth.models import User
from Django.contrib.auth import logout as login, authticate
from Django.views.decorators.csrf import csrf_exempt
from .products import Products, Cards
from .populate import initiate
from .restapis import get_request, post_review)


# logger instance
logger = logging.getLogger(__name__)

def get_product(request):

count = Products.objects.count()
if count == 0:
	initiate()
Product_list = Products.objects.select_related(‘cards’)
Cards = [
	{“Card”: card.name, “Product”: card.product.name}
	for card in cards
]
Return JsonResponse({“Cards”: cards})

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





def logout(request):
    """
    Handles user logout.
    """
    data = {"userName": ""}
    return JsonResponse(data)


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

data = json.loads(request.body)
submission = data[‘requests’]
card_request= {
	“request”: submission,
}
file_name = “requests.json”

with open(file_name, ‘w’) as json_file:
json.dump(submission, json_file, indent=4)
def get_product_details(request, product_id):

if product_id:
endpoint = f”/fetchProduct/{product_id}”
product = get_request(endpoint)
return JsonResponse({“status”:200, “product”: product})
Return JsonResponse({“status”:400, “message”:”Bad Request”)}

def submit_order(request)