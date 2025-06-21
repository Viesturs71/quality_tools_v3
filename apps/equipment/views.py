from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Equipment


class EquipmentListView(ListView):
    """View to display list of equipment."""
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'


class EquipmentDetailView(DetailView):
    """View to display equipment details."""
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'


@login_required
def my_equipment(request):
    """View for displaying user-specific equipment."""
    return render(request, 'equipment/my_equipment.html', {'page_title': 'My Equipment'})


@login_required
def maintenance_list(request):
    """View for displaying a list of maintenance records."""
    return render(request, 'equipment/maintenance_list.html', {'page_title': 'Maintenance Records'})
