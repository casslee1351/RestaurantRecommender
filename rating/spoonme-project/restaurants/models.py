from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=False)
    rating = models.CharField(max_length=10)
    review = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.restaurant, self.rating, self.user.id
