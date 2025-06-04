# myproject/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

#from methods.models.metozu_registrs import MetozuRegistrs


@login_required
def home_view(request):
    return render(request, 'home.html')

def handler404(request, exception):
    """Custom 404 error handler."""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error handler."""
    return render(request, 'errors/500.html', status=500)
