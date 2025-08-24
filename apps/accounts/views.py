# accounts/views.py
"""
Views for the accounts app.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models

from .forms import (
    CustomUserCreationForm as RegistrationForm,  # Alias the existing form
    LoginForm, 
    ProfileForm, 
    AccountSettingsForm,
    AccountForm,
    SubscriptionForm
)
from .models import CustomUser, UserProfile, Account, Subscription, AccountMembership


def register(request):
    """
    User registration.
    Validates and saves registration data.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _(f"Account successfully created! Welcome, {user.username}!"))
            return redirect(reverse_lazy("accounts:login"))
        else:
            messages.error(request, _("Registration failed. Please check the entered data."))
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('accounts:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile(request):
    """
    User profile view. Accessible only to authenticated users.
    """
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def profile_update(request):
    """Update user profile information."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def account_settings(request):
    """User account settings view."""
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Account settings updated successfully.'))
            return redirect(reverse('accounts:settings'))
    else:
        form = AccountSettingsForm(instance=request.user)
    
    return render(request, 'accounts/settings.html', {
        'form': form,
        'title': _('Account Settings')
    })


# Keep other view functions...

@login_required
def dashboard(request):
    """Display user dashboard."""
    return render(request, 'accounts/dashboard.html')

def account_verification(request):
    """Handle account verification."""
    # Implementation logic here
    return render(request, 'accounts/verification.html', )

def activate_account(request, uidb64, token):
    """Activate user account via email confirmation."""
    # Implementation logic here
    return redirect('accounts:login')

@login_required
def user_list(request):
    """Display list of users (admin only)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:dashboard')
    
    users = CustomUser.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def user_detail(request, user_id):
    """Display user details (admin only)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'accounts/user_detail.html', {'user_obj': user})

@login_required
def edit_user(request, user_id):
    """Edit user details (admin only)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:dashboard')
    
    # Implementation logic here
    return render(request, 'accounts/edit_user.html')

@login_required
def delete_user(request, user_id):
    """Delete user (admin only)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:dashboard')
    
    # Implementation logic here
    return redirect('accounts:user_list')

@login_required
def user_profile(request):
    """
    View for user profile page with edit functionality.
    """
    # Get or create the user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully'))
            return redirect('accounts:user_profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_view(request):
    """
    View for displaying and editing user profile.
    """
    # Get or create profile for the current user
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated successfully.'))
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)

class AccountDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_accounts = Account.objects.filter(
            models.Q(owner=self.request.user) | 
            models.Q(members=self.request.user)
        ).distinct()
        
        context['user_accounts'] = user_accounts
        context['total_accounts'] = user_accounts.count()
        return context

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "accounts/list.html"
    context_object_name = 'accounts'
    paginate_by = 20

    def get_queryset(self):
        return Account.objects.filter(
            models.Q(owner=self.request.user) | 
            models.Q(members=self.request.user)
        ).distinct()

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = "accounts/detail.html"
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership'] = AccountMembership.objects.filter(
            account=self.object,
            user=self.request.user
        ).first()
        return context

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = "accounts/form.html"
    success_url = reverse_lazy('accounts:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = "accounts/form.html"

    def get_success_url(self):
        return reverse_lazy('accounts:detail', kwargs={'pk': self.object.pk})

class BillingView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/billing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        account = get_object_or_404(Account, id=account_id, owner=self.request.user)
        subscription = getattr(account, 'subscription', None)
        
        context['account'] = account
        context['subscription'] = subscription
        return context

class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        account = get_object_or_404(Account, id=account_id)
        
        # Check if user has admin access to this account
        membership = AccountMembership.objects.filter(
            account=account,
            user=self.request.user,
            role__in=['admin', 'manager']
        ).first()
        
        if not membership and account.owner != self.request.user:
            raise PermissionDenied
        
        context['account'] = account
        context['membership'] = membership
        return context
