import decimal
from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=100, null=False)
    tags = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "restaurant"

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=False)
    rating = models.DecimalField(decimal_places=1, max_digits=3)
    review = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.restaurant, str(self.rating), self.user.id
