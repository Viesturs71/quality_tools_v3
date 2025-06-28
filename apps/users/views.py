from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def home_view(request):
    """
    Homepage view. Used by your project URLs for '' (i.e. /).
    """
    return render(request, 'home.html')

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    """Custom login view with enhanced template."""
    template_name = 'users/login.html'

def logout_view(request):
    """Log the user out and redirect to the home page."""
    logout(request)
    return redirect('home')

@login_required
def settings_view(request):
    """User settings view for system configurations."""
    return render(request, 'users/settings.html', {'page_title': 'Settings'})

@login_required
def user_documents(request):
    """View for displaying user-specific documents."""
    return render(request, 'users/user_documents.html', {'page_title': 'My Documents'})

@login_required
def activity_log(request):
    """View for displaying the user's activity log."""
    return render(request, 'users/activity_log.html', {'page_title': 'Activity Log'})

@login_required
def profile(request):
    """
    Main profile view for editing personal information.
    This backs both "/users/profile/" and the alias endpoints below.
    """
    # Ensure the user has a profile object
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })

# Aliases so that the URL names match what's in your urls.py:
@login_required
def my_profile(request):
    return profile(request)

@login_required
def edit_profile(request):
    return profile(request)
