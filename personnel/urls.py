from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    # Default index view
    path('', views.index, name='index'),
    
    # Staff management views
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    
    # Qualification management views
    path('qualifications/', views.qualification_list, name='qualification_list'),
    path('qualifications/<int:qualification_id>/', views.qualification_detail, name='qualification_detail'),
    
    # Training management views
    path('training/', views.training_list, name='training_list'),
    path('training/<int:training_id>/', views.training_detail, name='training_detail'),
]
