from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listings.models import Listings
from .models import Profile  # Import Profile model

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Campus Marketplace, {user.username}! 🚀")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! 👋")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('home')
    logout(request)
    return redirect('home')

@login_required
def myaccount(request):
    user_listings = Listings.objects.filter(seller=request.user).order_by('-createdat')
    
    # Get the user's profile safely
    profile = getattr(request.user, 'profile', None)
    
    # Prepare avatar URL if it exists
    avatar_url = None
    if profile and profile.avatar:
        avatar_url = profile.avatar.url

    context = {
        'listings': user_listings,
        'profile': profile,
        'avatar_url': avatar_url,
        'RESIDENCE_CHOICES': Profile.RESIDENCE_CHOICES, # This populates your dropdown
    }
    return render(request, 'myaccount.html', context)

# --- NEW VIEW FOR UPDATING PROFILE ---
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile

        # 1. Update User info (First/Last Name)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        # 2. Update Profile info (Residence & Avatar)
        profile.residence = request.POST.get('residence')
        
        # Handle Image Upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('myaccount')

    return redirect('myaccount')