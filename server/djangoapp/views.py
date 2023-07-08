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


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

