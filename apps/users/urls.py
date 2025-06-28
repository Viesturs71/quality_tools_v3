from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/',         views.CustomLoginView.as_view(), name='login'),
    path('logout/',        views.logout_view,               name='logout'),
    path('register/',      views.register,                  name='register'),

    # Profile endpoints
    path('profile/',       views.profile,                   name='profile'),
    path('my-profile/',    views.my_profile,                name='my_profile'),
    path('profile/edit/',  views.edit_profile,              name='edit_profile'),

    # Other user‐specific pages
    path('settings/',      views.settings_view,             name='settings'),
    path('documents/',     views.user_documents,            name='user_documents'),
    path('activity-log/',  views.activity_log,              name='activity_log'),

   ]
