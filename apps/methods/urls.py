from django.urls import path
from . import views

app_name = 'methods'

urlpatterns = [
    path('', views.MethodListView.as_view(), name='method_list'),
    path('create/', views.MethodCreateView.as_view(), name='method_create'),
    path('<int:pk>/', views.MethodDetailView.as_view(), name='method_detail'),
    path('<int:pk>/update/', views.MethodUpdateView.as_view(), name='method_update'),
    path('initial/', views.method_initial_view, name='method_initial'),
    path('detail/', views.method_detail_view, name='method_detail_form'),
    path('success/', views.method_success_view, name='method_success'),  # Optional success page
]
