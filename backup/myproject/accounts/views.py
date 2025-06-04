# accounts/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import RegisterForm


def register(request):
    """
    User registration.
    Validates and saves registration data.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _(f"Account successfully created! Welcome, {user.username}!"))
            return redirect(reverse_lazy("accounts:login"))
        else:
            messages.error(request, _("Registration failed. Please check the entered data."))
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    """
    User profile view. Accessible only to authenticated users.
    """
    return render(request, "accounts/profile.html", {"user": request.user})
