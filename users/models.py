from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model to provide additional functionality.
    Using the AbstractUser as base to retain all Django's default user fields.
    """
    # Add any additional fields here if needed

    def __str__(self):
        return self.username
