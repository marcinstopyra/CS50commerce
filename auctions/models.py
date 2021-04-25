from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    photo = models.URLField()
    # allow photo field to be empty
    photo.blank = True
    current_price = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # watchlist indicates WHO? (user) saved it to his/her the wishlist
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_items")
    status_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='winner')
    category = models.ForeignKey(Categories, default=1, on_delete=models.CASCADE, related_name='listings')

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    made_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField()
    times = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    def __str__(self):
        return f"{self.made_by}"


class Comments(models.Model):
    made_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    made_on = models.ForeignKey(Listings, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
