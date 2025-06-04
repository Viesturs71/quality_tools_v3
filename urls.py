from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from quality_docs import views
from quality_docs.views import document_list


# Pagaidu sākumskats, ja dashboard/home.html ir galvenā lapa
def home(request):
    from django.shortcuts import render
    return render(request, 'dashboard/home.html')

urlpatterns = [
    path("", home, name="home"),

    # Autentifikācija
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),

    # Dokumenti
    path("documents/", document_list, name="documents"),
    path("documents/<int:pk>/", views.DocumentDetailView.as_view(), name="document_detail"),
    path("quality_docs/", include("quality_docs.urls", namespace="quality_docs")),

    # Personāls, Iekārtas u.c.
    path("personnel/", include("personnel.urls", namespace="personnel")),
    path("equipment/", include("equipment.urls", namespace="equipment")),
    path("company/", include("company.urls", namespace="company")),
    path("standards/", include("standards.urls", namespace="standards")),

    # Dashboard
    path("dashboard/", include("dashboard.urls")),

    # Admins (Custom Admin)
    path("manage/", include(("accounts.admin_urls", "accounts"), namespace="custom_admin")),

    # Valodas & Rosetta
    path("i18n/", include("django.conf.urls.i18n")),
    path("rosetta/", include("rosetta.urls")),

    # API dokumentācija
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Mediju failiem attīstības režīmā
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
