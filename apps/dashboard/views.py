from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home_view(request):
    """Main dashboard home view."""
    context = {
        'page_title': 'Dashboard',
        'user': request.user,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_view(request):
    """Dashboard overview with widgets."""
    context = {
        'page_title': 'Dashboard Overview',
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def index_view(request):
    """Dashboard index view."""
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)


def dashboard_home(request):
    """Dashboard home view for unauthenticated users."""
    return render(request, 'dashboard/home.html')  # Ensure this template exists
