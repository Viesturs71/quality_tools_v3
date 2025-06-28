from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.views.i18n import set_language as django_set_language


def custom_set_language(request):
    """
    Custom view to set the language preference and display a confirmation page.
    Extends Django's built-in set_language view to provide feedback to the user.
    
    This is useful during testing to verify language changes work correctly.
    """
    # First, call Django's built-in set_language view to handle the language setting
    response = django_set_language(request)
    
    # If it's not a redirect (which means something went wrong), return the response as is
    if not isinstance(response, HttpResponseRedirect):
        return response
        
    # Get redirect URL
    next_url = request.POST.get('next', request.GET.get('next'))
    if ((next_url or request.accepts('text/html')) and
            not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            )):
        next_url = request.META.get('HTTP_REFERER')
        if not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
            next_url = '/'
            
    # Get the current language
    current_language = translation.get_language()
    
    # Render the success template with the current language code
    context = {
        'LANGUAGE_CODE': current_language,
        'redirect_url': next_url,
    }
    return render(request, 'language_change_success.html', context)