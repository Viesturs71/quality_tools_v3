from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .models import Widget, UserPreference


@login_required
def index_view(request):
    """
    Dashboard index view with the user's configured widgets.
    This is the main dashboard entry point.
    """
    user_pref, created = UserPreference.objects.get_or_create(
        user=request.user,
        defaults={'layout': {'type': 'grid', 'columns': 3}}
    )
    
    widgets = []
    for pos in user_pref.widget_positions.filter(is_visible=True):
        widgets.append({
            'widget': pos.widget,
            'position': {
                'x': pos.position_x,
                'y': pos.position_y,
                'width': pos.width,
                'height': pos.height
            }
        })
    
    context = {
        'page_title': _('Dashboard'),
        'user': request.user,
        'widgets': widgets,
        'layout': user_pref.layout,
        'theme': user_pref.theme
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def dashboard_view(request):
    """Dashboard overview with widgets."""
    context = {
        'page_title': _('Dashboard Overview'),
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_home(request):
    """Dashboard home view for unauthenticated users."""
    return render(request, 'dashboard/home.html')
