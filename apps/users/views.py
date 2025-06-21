from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponse
from django.contrib.auth import logout
from .models.profile import Profile


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


@login_required
def profile(request):
    """User profile view."""
    # Ensure the user has a profile
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
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', context)


class CustomLoginView(LoginView):
    """Custom login view."""
    template_name = 'users/login.html'


def home_view(request):
    """Home page view."""
    return HttpResponse("Welcome to the Home Page")


def logout_view(request):
    """
    Log the user out and redirect to the home page.
    """
    logout(request)
    return redirect('home')  # Ensure 'home' is a valid URL name


@login_required
def settings_view(request):
    """User settings view."""
    return render(request, 'users/settings.html', {'page_title': 'Settings'})


@login_required
def user_documents(request):
    """View for displaying user-specific documents."""
    return render(request, 'users/user_documents.html', {'page_title': 'My Documents'})


@login_required
def my_profile(request):
    """View for displaying the user's profile."""
    return render(request, 'users/my_profile.html', {'page_title': 'My Profile'})


@login_required
def edit_profile(request):
    """View for editing the user's profile."""
    return render(request, 'users/edit_profile.html', {'page_title': 'Edit Profile'})


@login_required
def activity_log(request):
    """View for displaying the user's activity log."""
    return render(request, 'users/activity_log.html', {'page_title': 'Activity Log'})
