from django.urls import path
from . import views

app_name = 'standards'  # Ensure this is defined

urlpatterns = [
    path('management/', views.management, name='management'),  # Ensure this path exists
]
