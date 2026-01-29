from django.shortcuts import render



def home_view(request):
    return render(request,'home.html')

from django.shortcuts import render
from listings.models import Listings

def home(request):
    listings = Listings.objects.all().order_by("-createdat")[:6]
    print(f"🚀 HOME VIEW: Found {listings.count()} listings")
    return render(request, "home.html", {"listings": listings})
    listings = Listings.objects.filter(is_solf = False).order_by("-createdat")[:6]
    return render
