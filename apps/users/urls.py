from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # Add this line
    path('register/', views.register, name='register'),
    path('settings/', views.settings_view, name='settings'),  # Add this line
    path('documents/', views.user_documents, name='user_documents'),  # Add this line
    path('my-profile/', views.my_profile, name='my_profile'),  # Add this line
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Add this line
    path('activity-log/', views.activity_log, name='activity_log'),  # Add this line
]
