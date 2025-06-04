from django.urls import path
from django.views.generic import TemplateView

from .views import profile_view

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='user/user_home.html'), name='user_home'),
    path('dashboard/', TemplateView.as_view(template_name='user/dashboard.html'), name='dashboard'),
    path('profile/', profile_view, name='user_profile'),
    path('reports/', TemplateView.as_view(template_name='user/reports.html'), name='reports'),
]
