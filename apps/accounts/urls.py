"""
Authentication and user account management URLs with i18n support.
"""

from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.translation import gettext_lazy as _
from apps.company.admin import custom_admin_site  # Ensure this matches the definition
from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication URLs
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="accounts:login"
        ),
        name="logout",
    ),
    path(
        "register/",
        views.register,
        name="register",
    ),

    # Password management
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change_form.html",
            success_url="accounts:password_change_done"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # Password reset URLs
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url="accounts:password_reset_done",
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
            success_url="accounts:password_reset_complete",
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

    # User profile URLs
    path(
        "profile/",
        views.profile_view,  # Updated to use the correct view function name
        name="user_profile",
    ),
    path(
        "profile/edit/",
        views.profile_update,
        name="edit_profile",
    ),
    path(
        "profile/settings/",
        views.account_settings,
        name="account_settings",
    ),

    # Account management
    path(
        "account/verification/",
        views.account_verification,
        name="account_verification",
    ),
    path(
        "account/activate/<uidb64>/<token>/",
        views.activate_account,
        name="activate_account",
    ),

    # User management (admin only)
    path(
        "users/",
        views.user_list,
        name="user_list",
    ),
    path(
        "users/<int:user_id>/",
        views.user_detail,
        name="user_detail",
    ),
    path(
        "users/<int:user_id>/edit/",
        views.edit_user,
        name="edit_user",
    ),
    path(
        "users/<int:user_id>/delete/",
        views.delete_user,
        name="delete_user",
    ),

    # Custom admin dashboard
    path("admin/", custom_admin_site.urls),

    # Account management views
    path("", views.AccountListView.as_view(), name="list"),
    path("dashboard/", views.AccountDashboardView.as_view(), name="dashboard"),
    path("create/", views.AccountCreateView.as_view(), name="create"),
    path("<int:pk>/", views.AccountDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.AccountUpdateView.as_view(), name="edit"),
    path("<int:account_id>/billing/", views.BillingView.as_view(), name="billing"),
    path("<int:account_id>/settings/", views.AccountSettingsView.as_view(), name="settings"),
]
