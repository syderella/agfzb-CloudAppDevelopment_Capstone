from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealers_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

review_num = 0
dealerships = []
# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {
        "title": "About Us"
    }
    return render(request, "djangoapp/about_us.html", context)


# Create a `contact` view to return a static contact page

def contact(request):
    context = {
    "title": "Contact Us"
    }
    return render(request, "djangoapp/contact_us.html", context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # context["message"] = "Login Successful"
            return redirect("djangoapp:index")
        context["message"] = "Invalid username or password"
        return render(request, "djangoapp/index.html", context)
    return render(request, "djangoapp/index.html", context)




# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {
        "title": "User Registration"
    }
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        password = request.POST["psw"]
        if User.objects.filter(username=username):
            context["message"] = "User already exists.. please log in"
        else:
            user = User.objects.create_user(
                username=username, first_name=first_name,
                last_name=last_name, password=password
                 )
            login(request, user)
            return redirect("djangoapp:index")
    return render(request, "djangoapp/registration.html", context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    global dealerships
    context = {}
    if request.method == "GET":
        url = "https://8fd1fa9c.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, "djangoapp/index.html", context)

def get_dealer(dealer_id):
    for dealer in dealerships:
        if dealer.id == dealer_id:
            return dealer

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    global review_num
    dealer = get_dealer(dealer_id)
    context = {
        "title": "Dealer Reviews",
        "dealer": dealer,
        "dealer_id": dealer_id
    }
    if request.method == "GET":
        url = "https://8fd1fa9c.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealers_reviews_from_cf(url, dealer_id)
        review_num = len(reviews)
        context["review_list"] = reviews
        return render(request, "djangoapp/dealer_details.html", context) 


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

@login_required
def add_review(request, dealer_id):
    global review_num
    cars = CarModel.objects.all()
    dealer = get_dealer(dealer_id)
    context = {
        "dealer_id": dealer_id,
        "cars": cars,
        "dealer": dealer
    }
    if request.method == "POST":
        url = "https://8fd1fa9c.us-south.apigw.appdomain.cloud/api/review"
        
        if not review_num: 
            reviews = get_dealers_reviews_from_cf(url, dealer_id)
            review_num = len(reviews) 
        review_num += 1

        car_idx = int(request.POST["car"])-1
        selected_car = cars[car_idx]
        purchase_check = False
        if request.POST.get("purchasecheck"):
            purchase_check = True

        review = {
            "time": datetime.utcnow().isoformat(),
            "id": review_num,
            "name": request.user.username,
            "dealership": dealer_id,
            "review": request.POST["content"],
            "purchase": purchase_check,
            "purchase_date": request.POST.get("purchasedate"),
            "car_make": selected_car.carmake.name ,
            "car_model": selected_car.name,
            "car_year": selected_car.year
        }
        print(review)
        # json_payload = { "review": review }
        # response = post_request(url, json_payload, dealerId=dealer_id)
        # return HttpResponse(response)
     
    return render(request, "djangoapp/add_review.html", context)

