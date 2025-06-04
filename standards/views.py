from django.views.generic import TemplateView
from django.shortcuts import render

class StandardsManagementView(TemplateView):
    template_name = 'standards/management.html'  # Ensure this template exists

class StandardsRegistryView(TemplateView):
    template_name = 'standards/registry.html'

class StandardFormView(TemplateView):
    template_name = 'standards/standard_form.html'

def management(request):
    # Render the standards management page
    return render(request, 'standards/management.html')
