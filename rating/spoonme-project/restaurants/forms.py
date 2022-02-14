from attr import attrs
from django import forms
from django.forms import ModelForm
from .models import Rating, Restaurant


class RatingForm(ModelForm):
    query_set = Restaurant.objects.all()
    restaurant = forms.ModelChoiceField(
        widget=forms.Select(attrs={'id': 'ddl'}), queryset=query_set)
    rating = forms.DecimalField(widget=forms.NumberInput(
        attrs={'type': 'range', 'name': 'rating', 'step': '0.5', 'min': '1', 'max': '10', "value": "5.0",  "oninput": "this.nextElementSibling.value = this.value"}))

    class Meta:
        model = Rating
        fields = ['restaurant', 'rating']
