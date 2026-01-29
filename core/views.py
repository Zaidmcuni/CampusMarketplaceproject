from django.shortcuts import render



def home_view(request):
    return render(request,'home.html')

from django.shortcuts import render
from listings.models import Listings

def home(request):
   listings = Listings.objects.filter(is_sold=False).order_by("-createdat")[:6]
   return render(request, "home.html", {"listings": listings})
