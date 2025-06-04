#urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from accounts.custom_admin import custom_admin_site
from quality_docs.views import document_list  # Izlabots imports

urlpatterns = [
    path("", views.home_view, name="home"),
    path('quality_docs/', include('quality_docs.urls', namespace='quality_docs')),
    path("documents/", document_list, name="documents"),  # Izlabots
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("admin/", custom_admin_site.urls),
    path("personnel/", include("personnel.urls", namespace="personnel")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("rosetta/", include("rosetta.urls")),  # ✅ Rosetta ceļš
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('equipment/', include('equipment.urls', namespace='equipment')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
