from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model with additional fields
    """
    email = models.EmailField(_('Email address'), unique=True)
    phone_number = models.CharField(_('Phone number'), max_length=20, blank=True)
    
    # Fix the related_name clash with personnel.Employee.department
    department = models.ForeignKey(
        'company.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_users',  # Changed from 'employees' to 'custom_users'
        verbose_name=_('Department')
    )
    
    # Other fields...

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self):
        return self.username

class Account(models.Model):
    """
    Account model for company/organization account management.
    """
    name = models.CharField(_('Name'), max_length=200)
    code = models.CharField(_('Code'), max_length=50, unique=True)
    description = models.TextField(_('Description'), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_accounts',
        verbose_name=_('Account Owner')
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='AccountMembership',
        related_name='member_accounts',
        verbose_name=_('Members')
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ('name',)

    def __str__(self):
        return self.name

class AccountMembership(models.Model):
    """
    Through model for Account-User relationship with roles.
    """
    ROLE_CHOICES = [
        ('admin', _('Administrator')),
        ('manager', _('Manager')),
        ('user', _('User')),
        ('viewer', _('Viewer')),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name=_('Account')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    role = models.CharField(
        _('Role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )
    joined_at = models.DateTimeField(_('Joined At'), auto_now_add=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Account Membership')
        verbose_name_plural = _('Account Memberships')
        unique_together = ('account', 'user')

    def __str__(self):
        return f"{self.user} - {self.account} ({self.get_role_display()})"
