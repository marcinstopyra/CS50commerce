from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import create_listing_form

from .models import User, Listings, Bids, Categories, Comments


def index(request):
    return render(request, "auctions/index.html", {
    "listings": Listings.objects.all()
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
def create_listing_view(request):
    if request.method == "POST":
        form = create_listing_form(request.POST)
        if form.is_valid():
            # getting info from the form
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            current_price = form.cleaned_data['start_bid']
            photo =  form.cleaned_data['photo']
            category = form.cleaned_data['category']
            creator_id = request.user.id
            # create a model object give it attributes and then save it
            listing = Listings(title=title, description=description, photo=photo, current_price=current_price, creator_id=creator_id, category=category)
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            print("ZLE")
            print(form.errors)
            return render(request, "auctions/create_listing.html", {
            "form": form
            })
    else:
        form = create_listing_form()
        return render(request, "auctions/create_listing.html", {
        "form": form
        })

def listing_view(request, title):
    # getting user watchlist items to check if the listing is among them
    user = request.user
    listing = Listings.objects.get(title=title)
    if user.is_anonymous:
        return render(request, "auctions/listing.html", {
        "listing": listing
        })
    
    watchlist_items = user.watchlist_items.all()
    watchlist_status = (listing in watchlist_items)
    comments = Comments.objects.filter(made_on=listing)
    return render(request, "auctions/listing.html", {
    "listing": listing,
    "watchlist_status": watchlist_status,
    "comments": comments
    })

def watchlist_view(request, username):
    user = User.objects.get(username=username)
    watchlist_items = user.watchlist_items.all()
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlist_items": watchlist_items
    })

def update_watchlist(request, title):
    action = request.GET.get('action')
    user = request.user
    listing = Listings.objects.get(title=title)
    if action == "add":
        listing.watchlist.add(user)
    elif action == "remove":
        listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse('listing_view', args=[title]))

@login_required
def make_bid(request, title):
    listing = Listings.objects.get(title=title)
    user = request.user
    bid_amount = float(request.POST.get('bid'))
    if bid_amount > listing.current_price:
        bid = Bids(made_by=user, price=bid_amount, listing=listing)
        bid.save()
        Listings.objects.filter(title=title).update(current_price=bid_amount)     
    return HttpResponseRedirect(reverse('listing_view', args=[title]))

@login_required
def close_listing(request, title):
    listing = Listings.objects.get(title=title)
    # query the bids that match the listing
    # then find the one that matches the highest bid(current_price)
    # get the winner name and the price he/she offered
    winning_bid = Bids.objects.filter(listing=listing, price=listing.current_price).values('made_by', 'price')
    # close listing 
    listing.status_active = False
    # check if there were no bids
    if not winning_bid:
        listing.save()
        return HttpResponseRedirect(reverse('listing_view', args=[title]))
    #convert query set to list
    list(winning_bid)
    # change userId in 'made_by' to User object and convert to list
    winning_bid[0]['made_by'] = User.objects.get(id=winning_bid[0]['made_by'])
    list(winning_bid)
    listing.winner = winning_bid[0]['made_by']
    listing.status_active = False
    listing.save()

    return HttpResponseRedirect(reverse('listing_view', args=[title]))

def categories_view(request):
    return render(request, 'auctions/categories.html', {
        'categories': Categories.objects.all()
    })

def category_view(request, name):
    category = Categories.objects.get(name=name)
    return render(request, 'auctions/category.html', {
        'listings': Listings.objects.filter(category=category),
        'category': category
    })    

@login_required
def make_comment(request, title):
    listing = Listings.objects.get(title=title)
    user = request.user
    comment_text = request.POST.get("comment")
    comment = Comments(made_by=user, made_on=listing, text=comment_text)
    comment.save()
    return HttpResponseRedirect(reverse('listing_view', args=[title]))