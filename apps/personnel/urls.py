from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = 'personnel'

urlpatterns = [
    path('', lambda request: redirect('personnel:employee_list'), name='personnel_home'),
    # Employee views (class-based)
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Legacy and user-specific views
    # path('list/', views.PersonnelListView.as_view(), name='personnel_list'),
    path('my-profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('my-trainings/', views.MyTrainingsView.as_view(), name='my_trainings'),
    path('my-qualifications/', views.MyQualificationsView.as_view(), name='my_qualifications'),
]

