from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.create_listing, name="new_listing"),
    path("view_listing/<int:listing>/", views.view_listing, name="view_listing"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("end_listing/<int:listing_id>", views.end_listing, name="end_listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("category_listings/<str:category>", views.category_listings, name="category_listings"),
    path("watchlist_add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("categories", views.categories, name="categories"),
]
