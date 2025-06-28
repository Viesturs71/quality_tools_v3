from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.dashboard_home, name='home'),
    path('overview/', views.dashboard_view, name='overview'),
]

