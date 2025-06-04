# views.py
from django.apps import apps
from django.urls import NoReverseMatch, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def get_user_navigation():
    app_list = []
    for app_config in apps.get_app_configs():
        models = []
        for model in app_config.get_models():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            try:
                url = reverse(f"{app_label}:{model_name}_list")
            except NoReverseMatch:
                url = "#"
            models.append({
                'verbose_name_plural': model._meta.verbose_name_plural.title(),
                'url': url
            })
        app_list.append({
            'verbose_name': app_config.verbose_name.title(),
            'models': models
        })
    return app_list


@login_required
def user_home(request):
    app_list = get_user_navigation()
    return render(request, 'user_home.html', {'app_list': app_list, 'request': request})


def home(request):
    return render(request, 'dashboard/home.html')


def login_view(request):
    return render(request, 'accounts/login.html', {'request': request})
