### 📄 company/urls.py**

from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from . import views
from .views import CompanyViewSet

# 🚀 Swagger/OpenAPI dokumentācijas konfigurācija
schema_view = get_schema_view(
    openapi.Info(
        title="Uzņēmumu API",
        default_version="v1",
        description="API dokumentācija uzņēmumu pārvaldībai",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

app_name = 'company'

# Configure REST API router
router = DefaultRouter()
router.register(r'api', CompanyViewSet)

urlpatterns = [
    # Regular views
    path('', views.company_list, name='company_list'),
    path('<int:pk>/', views.company_detail, name='company_detail'),
    
    # API endpoints
    path('', include(router.urls)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),  # 📄 Swagger dokumentācija
]
