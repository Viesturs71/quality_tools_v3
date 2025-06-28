from django.db import models
from django.contrib.auth.models import AbstractUser
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
