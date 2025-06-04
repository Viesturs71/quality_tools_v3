from django.urls import path
from . import views

urlpatterns = [
    # Documents Register view
    path('register/', views.documents_register, name='documents_register'),
    path('register/section/<int:section_id>/', views.section_documents, name='section_documents'),
    path('register/document/<int:document_id>/', views.document_detail, name='document_detail'),
]