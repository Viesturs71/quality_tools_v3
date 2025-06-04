from django.urls import path

from . import views

app_name = 'audits'

urlpatterns = [
    path('', views.AuditListView.as_view(), name='audit_list'),
    path('create/', views.AuditCreateView.as_view(), name='audit_create'),
    path('<int:pk>/', views.AuditDetailView.as_view(), name='audit_detail'),
    path('<int:pk>/edit/', views.AuditUpdateView.as_view(), name='audit_edit'),
    path('<int:pk>/delete/', views.AuditDeleteView.as_view(), name='audit_delete'),
]
