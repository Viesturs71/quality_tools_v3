from django.contrib import admin
from .models import Profile, CustomPermission


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profils'


# Register models that belong to the users app
admin.site.register(CustomPermission)
admin.site.register(Profile)
