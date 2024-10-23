# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# from .populate import initiate
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# def logout_request(request):
# ...


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.load(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    # Check if the username or email already exists
    username_exist = User.objects.filter(username=username).exists()
    email_exist = User.objects.filter(email=email).exists()

    if not username_exist and not email_exist:
        # Create a new user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        # Log in the new user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        # If the user or email already exists
        error_message = "Already Registered"
        if email_exist:
            error_message = "Email Already Registered"
        data = {"userName": username, "error": error_message}
        return JsonResponse(data)


# ...


# Method to get the list of cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)  # For debugging purposes
    if count == 0:
        initiate()  # Make sure initiate() is defined somewhere to populate data if needed
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...
def analyze_review_sentiments(review_text):
    url = "https://sentianalyzer.1mu3rcgdbvsa.us-south.codeengine.appdomain.cloud/"  # Replace with the correct microservice URL
    payload = {"text": review_text}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return (
                response.json()
            )  # Assuming the response contains 'sentiment' attribute
        else:
            return {"sentiment": "neutral"}  # Default to neutral if microservice fails
    except requests.RequestException as e:
        return {"sentiment": "neutral"}  # Handle errors gracefully


# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id)
def get_dealer_reviews(request, dealer_id):
    endpoint = f"/fetchReviews/{dealer_id}"

    try:
        reviews = get_request(endpoint)
        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception as e:
        logger.error(f"Error fetching reviews for dealer {dealer_id}: {e}")
        return JsonResponse(
            {"status": 500, "message": "Internal Server Error"}, status=500
        )


# Get dealer details
# ...


def get_dealer_details(request, dealer_id):
    if dealer_id:
        # Construct the endpoint using the dealer_id
        endpoint = f"/fetchDealer/{dealer_id}"
        # Use get_request to fetch dealer details
        dealership = get_request(endpoint)
        # Return the dealership details as a JSON response
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        # Return a 400 Bad Request if dealer_id is missing
        return JsonResponse({"status": 400, "message": "Dealer ID not provided"})


# Create a `add_review` view to submit a review
# def add_review(request):
# ...
def add_review(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Load the data from the request body
        data = json.loads(request.body)
        try:
            # Call the post_request method to send the review
            response = post_request(data)
            print(response)  # Print the post response for debugging
            return JsonResponse(
                {"status": 200, "message": "Review posted successfully"}
            )
        except Exception as e:
            print(e)  # Print the error for debugging
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "User not authenticated"})
