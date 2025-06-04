# equipment/urls.py

from django.urls import path

from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.EquipmentListView.as_view(), name='index'),
    path('list/', views.EquipmentListView.as_view(), name='equipment-list'),
    path('create/', views.EquipmentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='delete'),
]
