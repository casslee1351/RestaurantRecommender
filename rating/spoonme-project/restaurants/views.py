import re
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Max, Min
import joblib

from .models import Rating, Restaurant
from .forms import RatingForm, RegisterForm, RestaurantCreationForm, RestaurantUpdateForm
from .decorators import unauthenticated_user

### ADD RECOMMENDATION TO BUTTON --> FILTER FOR USERS WITH RATINGS-- APPEAR IN MODAL?

@unauthenticated_user
def loginPage(request):
    page = 'login'

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # USERNAME AND PASSWORD VALIDATION
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                messages.error(request, "Username or password is incorrect.")
        except:
            messages.error(request, "Username or password is incorrect.")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')

    context = {'page': page}
    return render(request, "restaurants/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerUser(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        elif password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
        else:
            username = request.POST.get('username')
            username_count = User.objects.filter(username=username).count()
            if username_count > 0:
                messages.error(request, "Username already exists. Please choose a different one.")

    context = {'form': form}
    return render(request, "restaurants/login_register.html", context)

def home(request):
    ratings = Rating.objects.filter(user=request.user)
    context={'ratings': ratings}
    return render(request, "restaurants/home.html", context)

def restaurant(request, pk):
    restaurant = Restaurant.objects.get(id=pk)

    try:
        reviews = Rating.objects.filter(restaurant__id=pk)
        rating_count = Rating.objects.filter(restaurant__id=pk).count()
        rating_avg = Rating.objects.filter(restaurant__id=pk).aggregate(Avg('rating'))['rating__avg']

        context = {'restaurant': restaurant, 'ratingCount': rating_count, 'ratingAvg': rating_avg, 'reviews':reviews}
    except:
        context = {'restaurant': restaurant}
        redirect('restaurant/' + pk)
    
    return render(request, "restaurants/restaurant.html", context)

def allReviews(request, pk):
    restaurant = Restaurant.objects.get(id=pk)

    try:
        reviews = Rating.objects.filter(restaurant__id=pk)
        paginator = Paginator(reviews, 10)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2)

        context = {'restaurant': restaurant,  'reviews': reviews, 'page_obj': page_obj}

    except:
        context = {'restaurant': restaurant}
        redirect('restaurant/' + pk)
    return render(request, "restaurants/all-restaurant-reviews.html", context)


def restaurantList(request):
    if request.method == "POST":
        search = request.POST['search']
        searched_restaurants = Restaurant.objects.filter(
            name__icontains=search)

        context = {'searched_restaurants': searched_restaurants,
                   'search': search}
        return render(request, "restaurants/restaurant-search.html", context)
    else:
        restaurants = Restaurant.objects.all().order_by('name')
        paginator = Paginator(restaurants, 15)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2)

        context = {'restaurants': restaurants, 'page_obj': page_obj}
        return render(request, "restaurants/restaurant-list.html", context)


@login_required(login_url="login")
def ratings(request):
    user = request.user
    ratings = Rating.objects.filter(user=user)
    rating_count = Rating.objects.filter(user=user).count()

    paginator = Paginator(ratings, 5)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2)

    context = {'ratings': ratings, 'user': user, 'page_obj': page_obj, 'ratingCount': rating_count}
    return render(request, "restaurants/ratings.html", context)

@ login_required(login_url="login")
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    ratings = Rating.objects.filter(user=pk)
    rating_count = Rating.objects.filter(user=pk).count()
    rating_avg = Rating.objects.filter(user=pk).aggregate(Avg('rating'))['rating__avg']
    rating_max = Rating.objects.filter(user=pk).aggregate(Max('rating'))['rating__max']
    rating_min = Rating.objects.filter(user=pk).aggregate(Min('rating'))['rating__min']

    context = {'user': user, 'ratings': ratings, 'ratingCount': rating_count, 'ratingAvg': rating_avg, 'ratingMax':rating_max, 'ratingMin':rating_min}
    return render(request, "restaurants/profile.html", context)

@ login_required(login_url="login")
def addRating(request):
    # need to make reviews unique to user and restaurant?
    form = RatingForm()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            user_rating = form.save(commit=False)
            user_rating.user = request.user
            user_rating.save()
            return redirect('addrating')

    context = {'form': form}
    return render(request, "restaurants/rating-form.html", context)


@ login_required(login_url="login")
def updateRating(request, pk):
    rating = Rating.objects.get(id=pk)
    form = RatingForm(instance=rating)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating.rating = request.POST['rating']
            rating.review = request.POST['review']
            form.save()
            return redirect('ratings')

    context = {'form': form}
    return render(request, "restaurants/rating-form.html", context)

@ login_required(login_url="login")
def deleteRating(request, pk):
    rating = Rating.objects.get(id=pk)

    if request.method == 'POST':
        rating.delete()
        return redirect('ratings')
    return render(request, "restaurants/delete.html", {'rating': rating})

def addRestaurant(request):
    form = RestaurantCreationForm()

    if request.method == 'POST':
        form = RestaurantCreationForm(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            name.save()
            return redirect('addrestaurant')

    context = {'form': form}
    return render(request, "restaurants/restaurant-form.html", context)

@staff_member_required
def manageRestaurants(request):
    return render(request, "restaurants/manage-restaurants.html", {})

@staff_member_required
def deleteRestaurant(request, pk):
    restaurant = Restaurant.objects.get(id=pk)

    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurants')
    
    context={'restaurant': restaurant}
    return render(request, "restaurants/delete-restaurant.html", context)

@ login_required(login_url="login")
def updateRestaurant(request, pk):
    restaurant = Restaurant.objects.get(id=pk)
    form = RestaurantUpdateForm(instance=restaurant)

    if request.method == 'POST':
        form = RestaurantUpdateForm(request.POST, instance=restaurant)
        if form.is_valid():
            restaurant.name = request.POST['name']
            restaurant.tags = request.POST['tags']
            restaurant.local_highlight = request.POST['local_highlight']
            form.save()
            return redirect('restaurants')

    context = {'form': form}
    return render(request, "restaurants/update-restaurant.html", context)
