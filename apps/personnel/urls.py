from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    path('list/', views.personnel_list, name='personnel_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('my-profile/', views.my_profile, name='my_profile'),  # Add this line
    path('my-trainings/', views.my_trainings, name='my_trainings'),  # Add this line
    path('my-qualifications/', views.my_qualifications, name='my_qualifications'),  # Add this line
]

