import decimal
from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100, null=False)
    tags = models.CharField(max_length=50, null=True)
    local_highlight = models.CharField(max_length=500, null=True)

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

# add lunch buddy groups to user profile
# user will need to create group and add users
# watch tutorial for room creation and user addition
class LunchBuddies(models.Model):
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='participants')

    def __str__(self):
        return self.name