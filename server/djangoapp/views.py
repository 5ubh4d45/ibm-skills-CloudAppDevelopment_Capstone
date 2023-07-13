import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from djangoapp.models import CarModel

from djangoapp.restapis import get_dealer_reviews_from_cf, get_dealers_from_cf, get_dealers_from_cf_by_state, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request :HttpRequest):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request :HttpRequest):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request :HttpRequest):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # try authentication
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request=request, user=user)
            print(f"Log in user: {username}")
            return redirect('djangoapp:index')
        
        else:
            return redirect('djangoapp:register')
        
    else:
        redirect('djangoapp:register')


# Create a `logout_request` view to handle sign out request
def logout_request(request :HttpRequest):
    print(f"Log out user: {request.user.username}")
    
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request :HttpRequest):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    
    elif request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        user_exists = False

        try:
            user = User.objects.get(username=username)
            user_exists = True
            print(f"User Exists: {username}")
        except:
            print(f"New user: {username}")

        if not user_exists:
            user = User.objects.create_user(
                username=username,
                first_name=firstname,
                last_name=lastname,
                password=password
            )
            login(request=request, user=user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:register')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request : HttpRequest):
    context = {}
    if request.method == "GET":
        # return render(request, 'djangoapp/index.html', context)
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/330077d3-9d1d-4995-a6ca-bcdbccd5086f/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # dealerships = get_dealers_from_cf_by_state(url, "Texas")
        
        context["dealerships"] = dealerships

        # Return the index.html with dealers list
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request: HttpRequest, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/330077d3-9d1d-4995-a6ca-bcdbccd5086f/api/review"

        # Get dealer's reviewfrom the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)

        # inefficient way to get dealership details
        context["dealership"] = get_dealership_by_id(dealer_id)

        if (reviews is None or len(reviews) == 0):
            reviews = []
            context["dealership"] = None
        
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id

        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request: HttpRequest, dealer_id):
    context = {}
    cars = CarModel.objects.all()
    
    if request.method == "GET" and request.user.is_authenticated:

        cars_context = []
        for car in cars:
            cars_context.append(
                {
                    "model": car.name,
                    "make": car.carMake.name,
                    "year": car.year.strftime("%Y"),
                    "type": car.car_type
                }
            )

        context["cars"] = cars_context
        context["dealer_id"] = dealer_id
        context["dealership"] = get_dealership_by_id(dealer_id)

        return render(request, 'djangoapp/add_review.html', context)
    

    # only authenticated users can submit a review
    if request.method == "POST" and request.user.is_authenticated:
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/330077d3-9d1d-4995-a6ca-bcdbccd5086f/api/review"
        
        # Get dealer's review from POST request

        car_selected = request.POST["car_select"].split("-")
        car_model = car_selected[0]
        car_make = car_selected[1]
        car_year = car_selected[2]
        car_type = car_selected[3]

        purchase = request.POST["purchase_check"] == "on"
        # purchase_date = request.POST["purchase_date"]
        purchase_date = datetime.strptime(request.POST["purchase_date"], "%Y-%m-%d").strftime("%d/%m/%Y")
        
        review = {
            "id": uuid.uuid4().int,
            "name": request.user.first_name + " " + request.user.last_name,
            "dealership": dealer_id,
            "review": request.POST["review"],
            "purchase": purchase,
            "purchase_date": purchase_date,
            "car_model": car_model,
            "car_make": car_make,
            "car_year": car_year,
            "car_type": car_type
        }

        # body: dict = json.loads(request.body)

        # review = {
        #     "id": body["id"],
        #     "name": body["name"],
        #     "dealership": dealer_id,
        #     "review": body["review"],
        #     "purchase": body.get("purchasecheck", False),
        #     "purchase_date": body["purchasedate"],
        #     "car_make": body["car_make"],
        #     "car_model": body["car_model"],
        #     "car_year": body["car_year"]
        # }

        # review = {
        # "id": 1150,
        # "name": "lol Das",
        # "dealership": 19,
        # "review": "Loved the customer service.",
        # "purchase": True,
        # "another": "field",
        # "purchase_date": "12/03/2023",
        # "car_make": "Mahindra",
        # "car_model": "Scorpio",
        # "car_year": 2023
    # }

        json_payload = {"review": review}
        json_result = post_request(url, json_payload, dealerId=dealer_id)

        # review_result = json.dumps(json_result, indent=2)

        print(json.dumps(json_payload, indent=2))

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    
    return HttpResponse("Unauthorized", status=401)


def get_dealership_by_id(dealer_id):
    # fetching all dealerships and then filtering by id
    # can be improved by fetching only the required dealership
    url_d = "https://au-syd.functions.appdomain.cloud/api/v1/web/330077d3-9d1d-4995-a6ca-bcdbccd5086f/api/dealership"
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url_d)
    return [dealer for dealer in dealerships if dealer.id == dealer_id][0]