from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard/home view
    path('', views.home_view, name='home'),

    # Dashboard view
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Ensure the 'dashboard' view is defined

    # Index view
    path('index/', views.index_view, name='index'),
]
