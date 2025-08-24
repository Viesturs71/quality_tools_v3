import secrets
from django.db import models
from django.utils import timezone

class Token(models.Model):
    key = models.CharField(max_length=40, unique=True, db_index=True)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Token({self.user}, {self.key})"