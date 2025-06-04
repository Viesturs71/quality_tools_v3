# equipment/urls.py

"""
URL patterns for the equipment app.
"""

from django.urls import path

from . import views

app_name = 'equipment'  # This is needed for the namespace to work

urlpatterns = [
    # Equipment list and detail views
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    
    # Document handling
    path('<int:equipment_id>/documents/add/', views.add_equipment_document, name='add_document'),
    path('documents/<int:document_id>/delete/', views.delete_equipment_document, name='delete_document'),
    
    # Maintenance records
    path('<int:equipment_id>/maintenance/add/', views.add_maintenance_record, name='add_maintenance'),
    path('maintenance/<int:record_id>/delete/', views.delete_maintenance_record, name='delete_maintenance'),
    path('my-equipment/', views.MyEquipmentListView.as_view(), name='my_equipment_list'),
]
