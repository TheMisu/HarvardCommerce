from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):
    pass

# Category model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Auction Listing model
class Listing(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    date_time_creation = models.DateTimeField(auto_now_add=True)
    picture = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")

    def __str__(self):
        return self.name
    
