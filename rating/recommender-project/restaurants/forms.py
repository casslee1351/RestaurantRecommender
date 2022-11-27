from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Rating, Restaurant


class RatingForm(ModelForm):
    query_set = Restaurant.objects.all()
    restaurant = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-group', 'id': 'ddl'}), queryset=query_set)
    rating = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-group', 'type': 'range', 'id': 'rating', 'name': 'rating', 'step': '0.5', 'min': '1', 'max': '10', "value": "5.0",  "oninput": "this.nextElementSibling.value = this.value"}))
    review = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'review', 'rows': '5', 'placeholder': "Write your review..."}), required=False)

    class Meta:
        model = Rating
        fields = ['restaurant', 'rating', 'review']


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=15, min_length=2, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class RestaurantCreationForm(ModelForm):
    name = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=50, required=False)
    local_highlight = forms.CharField(widget=forms.Textarea, max_length=250, required=False)

    class Meta:
        model = Restaurant
        fields = '__all__'

class RestaurantUpdateForm(ModelForm):
    name = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=50, required=False)
    local_highlight = forms.CharField(widget=forms.Textarea, max_length=250, required=False)

    class Meta:
        model = Restaurant
        fields = '__all__'
