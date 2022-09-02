import re
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator


from .models import Rating, Restaurant
from .forms import RatingForm, RegisterForm, RestaurantCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username or password does not exist.")

    context = {'page': page}
    return render(request, "restaurants/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    #form = RegisterForm()
    form = RegisterForm(request.POST)

    if request.method == "POST":
        # form = RegisterForm(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred.")

    context = {'form': form}
    return render(request, "restaurants/login_register.html", context)


def home(request):
    return render(request, "restaurants/home.html", {})


def restaurant(request, pk):

    restaurant = Restaurant.objects.get(id=pk)

    context = {'restaurant': restaurant}
    return render(request, "restaurants/restaurant.html", context)


def restaurantList(request):
    # want to add alphabetical option

    if request.method == "POST":
        search = request.POST['search']
        searched_restaurants = Restaurant.objects.filter(
            name__icontains=search)

        context = {'searched_restaurants': searched_restaurants,
                   'search': search}
        return render(request, "restaurants/restaurant-search.html", context)
    else:
        restaurants = Restaurant.objects.all()
        # change to show more per page (about 20?)
        paginator = Paginator(restaurants, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'restaurants': restaurants, 'page_obj': page_obj}
        return render(request, "restaurants/restaurant-list.html", context)


@login_required(login_url="login")
def ratings(request):
    user = request.user
    ratings = Rating.objects.filter(user=user).order_by('-updated')
    paginator = Paginator(ratings, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'ratings': ratings, 'user': user, 'page_obj': page_obj}
    return render(request, "restaurants/ratings.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    ratings = Rating.objects.filter(user=pk)
    context = {'user': user, 'ratings': ratings}
    return render(request, "restaurants/profile.html", context)


@ login_required(login_url="login")
def addRating(request):
    form = RatingForm()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            user_rating = form.save(commit=False)
            user_rating.user = request.user
            user_rating.save()
            return redirect('ratings')

    context = {'form': form}
    return render(request, "restaurants/rating-form.html", context)


@ login_required(login_url="login")
def updateRating(request, pk):
    rating = Rating.objects.get(id=pk)
    form = RatingForm(instance=rating)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
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
