from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Changed from 'profile' to 'profile_view' to match the actual view function name
    path('profile/', views.profile_view, name='profile'),
    path('activity-log/', views.activity_log, name='activity_log'),
]
