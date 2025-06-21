"""
Authentication and user account management URLs with i18n support.
"""

from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.translation import gettext_lazy as _
from apps.company.admin import custom_admin_site  # Ensure this matches the definition
from . import views

app_name = "accounts"

urlpatterns = custom_admin_site.get_urls()
urlpatterns = [
    # 👤 User registration & profile
    path(
        "register/",
        views.register,
        name="register",
    ),
    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    # 🔐 Login / Logout
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            extra_context={"page_title": _("Login")}
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="accounts/logged_out.html",
            extra_context={"page_title": _("Logged out")}
        ),
        name="logout",
    ),

    # 🔒 Password change
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            extra_context={"page_title": _("Change password")}
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html",
            extra_context={"page_title": _("Password changed")}
        ),
        name="password_change_done",
    ),

    # 🔁 Password reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            extra_context={"page_title": _("Reset password")}
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
            extra_context={"page_title": _("Password reset sent")}
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            extra_context={"page_title": _("Set new password")}
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
            extra_context={"page_title": _("Password reset complete")}
        ),
        name="password_reset_complete",
    ),
]
