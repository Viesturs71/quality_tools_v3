from django.apps import apps
from django.urls import NoReverseMatch, reverse


def navigation(request):
    """
    Context processor that provides app_list for all templates
    """
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
        if models:  # Add only apps with models
            app_list.append({
                'verbose_name': app_config.verbose_name.title(),
                'models': models
            })
    return {'app_list': app_list}
