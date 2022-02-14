import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Rating, Restaurant
from .forms import RatingForm


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
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
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


@login_required(login_url="login")
def ratings(request):

    ratings = Rating.objects.all()
    context = {'ratings': ratings}
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
