from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):
    pass

# Auction Listing model
class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    curr_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    date_time_creation = models.DateTimeField(auto_now_add=True)
    picture = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=255, blank=True)

    # change the save method so that we can set curr_price = start_price
    def save(self, *args, **kwargs):
        if self.curr_price == 0.00:
            self.curr_price = self.starting_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# Bid model
class Bid(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    date_time_creation = models.DateTimeField(auto_now_add=True)

    # change the save method so that we can update the curr price
    # of a listing if this is the highest bid on that listing
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # find the highest bid on that particular listing
        highest_bid = Bid.objects.filter(listing=self.listing).order_by('-amount').first()
        if highest_bid:
            self.listing.curr_price = highest_bid.amount
            self.listing.save()

    def __str__(self):
        return str(self.amount)

# Comment model
class Comment(models.Model):
    comm = models.TextField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_time_creation = models.DateTimeField(auto_now_add=True)   
