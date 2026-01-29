from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listings

def listings_list(request):
    """Redirect to home - home = all listings"""
    return redirect('/')

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        residence = request.POST.get("residence")
        image = request.FILES.get("image")
        
        # NEW: Handle optional price
        price = request.POST.get("price")
        if price == "":
            price = None
        
        listing = Listings.objects.create(
            title=title,
            description=description or "",
            price=price,
            category=category,
            residence=residence,
            image=image,
            seller=request.user,
        )
        messages.success(request, "Listing created successfully!")
        return redirect("listing_detail", pk=listing.pk)
    
    context = {
        "category_choices": Listings.CATEGORY_CHOICES,
        "residence_choices": Listings.RESIDENCE_CHOICES,
    }
    return render(request, "create_listing.html", context)

def listing_detail(request, pk):
    listing = get_object_or_404(Listings, pk=pk)
    return render(request, "listing_detail.html", {"listing": listing})

def search_results(request):
    query = request.GET.get("q", "")
    listings = Listings.objects.filter(
        title__icontains=query, 
        is_sold=False
    ).order_by("-createdat")
    return render(request, "search_results.html", {"listings": listings, "query": query})

# --- NEW FUNCTIONS ---

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listings, pk=pk)

    if request.user != listing.seller:
        messages.error(request, "You are not allowed to edit this listing.")
        return redirect('home')

    if request.method == "POST":
        listing.title = request.POST.get("title")
        listing.description = request.POST.get("description")
        listing.category = request.POST.get("category")
        listing.residence = request.POST.get("residence")
        
        # NEW: Handle optional price logic for edits
        price = request.POST.get("price")
        if price == "":
            listing.price = None
        else:
            listing.price = price
        
        if request.FILES.get("image"):
            listing.image = request.FILES.get("image")
            
        listing.save()
        messages.success(request, "Listing updated successfully!")
        return redirect("listing_detail", pk=listing.pk)

    context = {
        "listing": listing,
        "category_choices": Listings.CATEGORY_CHOICES,
        "residence_choices": Listings.RESIDENCE_CHOICES,
    }
    return render(request, "edit_listings.html", context)

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listings, pk=pk)

    if request.user != listing.seller:
        messages.error(request, "You can't delete someone else's listing!")
        return redirect('home')

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted.")
        return redirect('home')
    
    return redirect('listing_detail', pk=pk)

@login_required
def mark_sold(request, pk):
    listing = get_object_or_404(Listings, pk=pk)
    
    if request.user == listing.seller:
        listing.is_sold = True
        listing.save()
        messages.success(request, "Item marked as sold!")
    
    return redirect('listing_detail', pk=pk)