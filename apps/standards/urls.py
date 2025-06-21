from django.urls import path
from . import views

app_name = 'standards'

urlpatterns = [
    # Example URL pattern
    path('', views.standards_list, name='standards_list'),
    path('list/', views.standard_list, name='standard_list'),  # Add this line
    path('search/', views.standard_search, name='standard_search'),  # Add this line
]
