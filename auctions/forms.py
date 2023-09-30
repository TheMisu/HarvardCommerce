from auctions.models import Listing
from django import forms

# Form for creating a new listing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_price', 'picture', 'category']