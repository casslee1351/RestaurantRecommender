from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),

    path("", views.home, name="home"),
    path("ratings", views.ratings, name="ratings"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),

    path("addrating/", views.addRating, name="addrating"),
    path("update-rating/<str:pk>/", views.updateRating, name="update-rating"),
    path("delete-rating/<str:pk>/", views.deleteRating, name="delete-rating"),
]
