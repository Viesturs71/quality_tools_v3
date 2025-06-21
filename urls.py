from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

urlpatterns = [
    path('rosetta/', include('rosetta.urls')),  # Rosetta translation tool
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls', namespace='users')),
    # ...other app includes...
)
