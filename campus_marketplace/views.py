from django.shortcuts import render
from listings.views import listings_list  

def home(request):
   
    response = listings_list(request)
    listings = response.context_data['listings'] if hasattr(response, 'context_data') else []
    
    print(f"HOME VIEW: Found {len(listings)} listings")
    return render(request, "home.html", {"listings": listings[:6]})
