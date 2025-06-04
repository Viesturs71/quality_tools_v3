from django.urls import path

from . import views
from .views import EmployeeCreateView, EmployeeListView

app_name = 'personnel'

urlpatterns = [
    path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/create/', EmployeeCreateView.as_view(), name='add_employee'),  # ✅ Jābūt `add_employee`
    path('employee/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('', views.personnel_list, name='personnel_list'),
]
