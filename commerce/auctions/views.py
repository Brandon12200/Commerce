from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages

from .models import Listing, User, Bid, Comment


def index(request):
    categories = ('electronics', 'fashion', 'books', 'home', 'toys', 'sports', 'food')

    return render(request, "auctions/index.html", {
        "listings":Listing.objects.filter(is_closed=False),
        "categories":categories
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
    
class NewListingForm(forms.Form):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('books', 'Books'),
        ('home', 'Home'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('food', 'Food'),
    )
    title = forms.CharField(label = "Title")
    description = forms.CharField(widget = forms.Textarea, label = "Description", max_length = 3000)
    image = forms.URLField(max_length = 2000, required = False)
    category = forms.ChoiceField(choices = CATEGORY_CHOICES)
    current_bid = forms.FloatField(initial = 0.0)


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            new_listing = Listing(
                category = form.cleaned_data['category'],
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                image = form.cleaned_data['image'],
                current_bid = form.cleaned_data['current_bid'],
                seller = request.user
            )
            new_listing.save()
            return redirect('index')
        else:
            print(form.errors)
            messages.error(request, "Please provide all information to create a new listing")
    else:
        form = NewListingForm()

    return render(request, 'auctions/create_listing.html', {
        "form":form
    })

class NewBidForm(forms.Form):
    bid_amount = forms.FloatField(initial=0.0)

def view_listing(request, listing):
    most_recent_bid = Bid.objects.filter(item=listing).order_by('-placed_at').first()
    comments = Comment.objects.filter(item=listing)
    user = request.user

    if user.is_authenticated:
        watchlist = user.watchlist.all()
    else:
        watchlist = None

    return render(request, 'auctions/listing.html', {
        "listing":Listing.objects.get(id = listing),
        "most_recent_bid":most_recent_bid,
        "comments":comments,
        "watchlist":watchlist
    })

@login_required
def place_bid(request, listing_id):
    listing = Listing.objects.get(id = listing_id)

    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']

            if bid_amount > listing.current_bid:
                new_bid = Bid.objects.create(item = listing, amount = bid_amount, bidder = request.user)
                listing.current_bid = bid_amount
                listing.save()
            else:
                messages.error(request, "Please place a bid greater than the current bid.")

                return redirect('view_listing', listing = listing_id)
    return redirect('view_listing', listing = listing_id)

@login_required
def end_listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)

    if request.user == listing.seller:
        listing.is_closed = True
        listing.save()
        messages.success(request, "Listing has been ended.")
    else:
        messages.error(request, "You don't have permission to end this listing.")
    
    return redirect('view_listing', listing = listing.id)

class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

@login_required
def add_comment(request, listing_id):
    listing = Listing.objects.get(id = listing_id)

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            new_comment = Comment.objects.create(item = listing, comment = comment, commenter = request.user)
        else:
            messages.error(request, "Please enter a comment.")
        
        return redirect('view_listing', listing = listing.id)
    
    return redirect('view_listing', listing = listing_id)

def category_listings(request, category):

    categories = ('electronics', 'fashion', 'books', 'home', 'toys', 'sports', 'food')

    return render(request, "auctions/index.html", {
        "listings":Listing.objects.filter(is_closed = False, category = category),
        "categories":categories
    })

@login_required
def watchlist_add(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    user = request.user

    user.watchlist.add(listing)
    return redirect('view_listing', listing = listing_id)

@login_required
def watchlist_remove(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    user = request.user

    user.watchlist.remove(listing)
    return redirect('view_listing', listing = listing_id)

@login_required
def view_watchlist(request):

    user = request.user
    watchlist = user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {
        "watchlist":watchlist
    })

def categories(request):
    categories = ('electronics', 'fashion', 'books', 'home', 'toys', 'sports', 'food')
    return render(request, 'auctions/categories.html', {
        "categories":categories
    })



