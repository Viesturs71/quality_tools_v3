from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import Account

class Subscription(models.Model):
    """
    Subscription model for account billing and plan management.
    """
    PLAN_CHOICES = [
        ('basic', _('Basic')),
        ('standard', _('Standard')),
        ('premium', _('Premium')),
        ('enterprise', _('Enterprise')),
    ]

    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('suspended', _('Suspended')),
        ('cancelled', _('Cancelled')),
        ('trial', _('Trial')),
    ]

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name=_('Account')
    )
    plan = models.CharField(
        _('Plan'),
        max_length=20,
        choices=PLAN_CHOICES,
        default='basic'
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='trial'
    )
    max_users = models.PositiveIntegerField(_('Maximum Users'), default=5)
    max_storage_gb = models.PositiveIntegerField(_('Maximum Storage (GB)'), default=1)
    monthly_price = models.DecimalField(
        _('Monthly Price'),
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    trial_ends_at = models.DateTimeField(_('Trial Ends At'), null=True, blank=True)
    next_billing_date = models.DateTimeField(_('Next Billing Date'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f"{self.account.name} - {self.get_plan_display()}"

    @property
    def is_trial(self):
        return self.status == 'trial'

    @property
    def is_active(self):
        return self.status == 'active'
