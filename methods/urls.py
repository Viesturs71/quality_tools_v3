# methods/urls.py
# methods/urls.py
from django.urls import path

app_name = 'methods'  # Pievienojam namespace

urlpatterns = [
    path('', views.method_list, name='method_list'),
]
