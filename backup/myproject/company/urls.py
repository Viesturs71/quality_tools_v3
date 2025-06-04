### 📄 company/urls.py**

from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

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

# 📦 API maršrutu reģistrācija ar DefaultRouter
router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),  # 🚀 CRUD maršruti uzņēmumiem
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),  # 📄 Swagger dokumentācija
]
