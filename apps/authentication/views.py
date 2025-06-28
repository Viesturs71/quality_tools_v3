from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import CustomAuthenticationForm


def login_view(request):
    """
    Custom login view with remember me functionality.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # If remember_me is True, set session expiry to 30 days
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
            else:
                request.session.set_expiry(0)  # Close browser session
                
            login(request, user)
            messages.success(request, _('Login successful.'))
            
            # Redirect to the next page if provided, otherwise go to profile
            next_page = request.GET.get('next', 'users:profile')
            return redirect(next_page)
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    """
    Logout view that redirects to login page with success message.
    """
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('authentication:login')
