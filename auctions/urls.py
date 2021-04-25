from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("listing/<str:title>", views.listing_view, name="listing_view"),
    path("watchlist/<str:username>", views.watchlist_view, name="watchlist"),
    path("listing/<str:title>/update_watchlist", views.update_watchlist, name="update_watchlist"),
    path("listing/<str:title>/make_bid", views.make_bid, name="make_bid"),
    path("listing/<str:title>/make_comment", views.make_comment, name="make_comment"),
    path("listing/<str:title>/close_listing", views.close_listing, name="close_listing"),
    path("categories", views.categories_view, name="categories_view"),
    path("categories/<str:name>", views.category_view, name="category_view")
]
