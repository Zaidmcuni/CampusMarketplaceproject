from django.urls import path
from . import views


urlpatterns = [
    path("", views.listings_list, name="listings_list"),
    path("create/", views.create_listing, name="create_listing"),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
    path("search/", views.search_results, name="search_results"),
    path("<int:pk>/edit/", views.edit_listing, name="edit_listing"),
    path("<int:pk>/delete/", views.delete_listing, name="delete_listing"),
    path("<int:pk>/sold/", views.mark_sold, name="mark_sold"),
]

