from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('my-equipment/', views.my_equipment, name='my_equipment'),  # Add this line
    path('maintenance/', views.maintenance_list, name='maintenance_list'),  # Add this line
]
