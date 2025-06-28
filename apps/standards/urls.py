from django.urls import path
from . import views
from apps.standards.views import StandardListView

app_name = 'standards'

urlpatterns = [
    # Standard Categories
    path('categories/', views.StandardCategoryListView.as_view(), name='category_list'),
    
    # Standards
    path('', views.StandardListView.as_view(), name='standard_list'),
    path('<int:pk>/', views.StandardDetailView.as_view(), name='standard_detail'),
    
    # Standard Sections
    path('section/<int:pk>/', views.StandardSectionDetailView.as_view(), name='section_detail'),
    
    # Standard Documents
    path('documents/', views.StandardDocumentListView.as_view(), name='document_list'),
    path('documents/<int:pk>/', views.StandardDocumentDetailView.as_view(), name='document_detail'),
    
    # Compliance Reports
    path('compliance-report/', views.ComplianceReportView.as_view(), name='compliance_report'),
    path('search/', views.search_standards, name='standard_search'),
]
