from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):
    pass

# Auction Listing model
class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    curr_price = models.DecimalField(max_digits=9, decimal_places=2)
    date_time_creation = models.DateTimeField(auto_now_add=True)
    picture = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
# Bid model
class Bid(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_time_creation = models.DateTimeField(auto_now_add=True)

# Comment model
class Comment(models.Model):
    comm = models.TextField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_time_creation = models.DateTimeField(auto_now_add=True)   
