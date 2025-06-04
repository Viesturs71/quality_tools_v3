# myproject/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

#from methods.models.metozu_registrs import MetozuRegistrs


@login_required
def home_view(request):
    return render(request, 'home.html')
