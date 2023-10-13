from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.forms import ListingForm
from django.contrib.auth.decorators import login_required


from .models import User, Listing


def index(request):
    # get the available listings
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    """
    This view is used to either diplay a page on which the user can fill in a form to
    create a listing or to submit the data in the form and save it in the DB.
    """
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False) # saves the data but doesn't update the db
            new_listing.save() # updates the db
            request.user.created.add(new_listing)   # relates the newly created listing to the user
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()
        return render(request, "auctions/create.html", {
        "form": form
        })

def listing(request, title):
    """
    This view is used to display the page of any individual listing.
    """
    listing = Listing.objects.get(title=title)
    user = request.user

    # used when the user clicks the submit button in order to add/remove
    # the listing from their watchlist
    if request.method == "POST":
        if listing in user.watchlist.all():
            # remove the listing if it was already in the users watchlist
            user.watchlist.remove(listing)
            return render(request, "auctions/listing.html", {
                "title": title,
                "listing": listing,
                "msg": "Add to Watchlist"
            }) 
        else:           
            # add the listing to the user's watchlist
            user.watchlist.add(listing)
            return render(request, "auctions/listing.html", {
                "title": title,
                "listing": listing,
                "msg": "Remove from Watchlist"
            })

    else:
        if listing in user.watchlist.all():
            return render(request, "auctions/listing.html", {
                "title": title,
                "listing": listing,
                "msg": "Remove from Watchlist"
            }) 
        else:           
            return render(request, "auctions/listing.html", {
                "title": title,
                "listing": listing,
                "msg": "Add to Watchlist"
            })
    
def watchlist(request):
    """
    This view is used to load and display the user's watchlist.
    """
    user = request.user
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.created.all()
    })