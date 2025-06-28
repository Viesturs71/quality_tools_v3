from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class StandardRevision(models.Model):
    """
    Tracks revisions and changes to standard sections or requirements.
    """
    # Generic Foreign Key to allow linking to either section or requirement
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('standardsection', 'standardrequirement')
        }
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Revision data
    changed_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='standard_revisions',
        verbose_name=_('Changed By')
    )
    change_type = models.CharField(
        _('Change Type'),
        max_length=20,
        choices=[
            ('create', _('Create')),
            ('update', _('Update')),
            ('delete', _('Delete')),
        ],
        default='update'
    )
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    previous_value = models.TextField(_('Previous Value'), blank=True)
    new_value = models.TextField(_('New Value'), blank=True)
    diff = models.TextField(_('Differences'), blank=True)
    change_reason = models.TextField(_('Change Reason'), blank=True)

    class Meta:
        verbose_name = _('Standard Revision')
        verbose_name_plural = _('Standard Revisions')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.content_object} - {self.get_change_type_display()} - {self.timestamp}"
