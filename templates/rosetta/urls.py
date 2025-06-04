from django.urls import path
from rosetta import views

urlpatterns = [
    path('', views.home, name='rosetta-home'),
    path('files/<str:po_filter>/<str:lang_id>/<int:idx>/', views.lang_sel, name='rosetta-file-detail'),
    path('files/<str:po_filter>/<str:lang_id>/', views.lang_sel, name='rosetta-language-selection'),
    path('files/<str:po_filter>/', views.lang_sel, name='rosetta-file-filter'),
]
