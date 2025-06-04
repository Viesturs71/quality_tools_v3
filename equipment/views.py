# equipment/views.py
from __future__ import annotations

# ──────────────────────
#  Standarta Django
# ──────────────────────
from datetime import date, timedelta
from django.db.models import Q

# ──────────────────────
#  Trešo pušu bibliot.
# ──────────────────────
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import EquipmentRegistry

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

# ──────────────────────
#  Lokālie importi
# ──────────────────────
# Import forms after models to avoid circular imports
from .models import (
    Equipment, 
    EquipmentDocument, 
    MaintenanceRecord, 
    EquipmentType, 
    Department
)
from .forms import EquipmentDocumentForm, EquipmentForm, MaintenanceRecordForm
from .serializers import (
    EquipmentSerializer,  # Change this from EquipmentRegistrySerializer
)

#   → Department ir obligāts tikai tad,
#     ja aplikācija "company" ir reģistrēta
HAS_DEPARTMENT = "company" in settings.INSTALLED_APPS
if HAS_DEPARTMENT:
    try:
        from django.apps import apps
        CompanyDepartment = apps.get_model("company", "Department")
    except (ImportError, LookupError):
        HAS_DEPARTMENT = False
        CompanyDepartment = None  # type: ignore

# Pievienojam noturīgu importu
try:
    from personnel.models import Department as PersonnelDepartment
    HAS_PERSONNEL_DEPARTMENT = True
except ImportError:
    HAS_PERSONNEL_DEPARTMENT = False

# ──────────────────────
#  API (DRF) – saglabāts
# ──────────────────────
class EquipmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class EquipmentViewSet(viewsets.ModelViewSet):
    """API endpoint that allows equipment to be viewed or edited."""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer  # Updated from EquipmentRegistrySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = EquipmentPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "equipment_name",
        "model_manufacturer",
        "inventory_number",
        "serial_number",
        "inspection_institution",
    ]
    ordering_fields = [
        "next_inspection_date",
        "inspection_frequency",
        "created_at",
        "updated_at",
    ]
    ordering = ["next_inspection_date"]


# ════════════════════════════════════════════════════════════════════════
#  HTML Skati
# ════════════════════════════════════════════════════════════════════════
class EquipmentListView(LoginRequiredMixin, ListView):
    """View for listing all equipment."""
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 10
    
    def get_queryset(self):
        """Filter queryset based on search parameters."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        department_filter = self.request.GET.get('department', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(inventory_number__icontains=search_query) |
                Q(serial_number__icontains=search_query)
            )
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        if department_filter:
            queryset = queryset.filter(department_id=department_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['status_choices'] = Equipment.STATUS_CHOICES
        return context


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    """View for displaying equipment details."""
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'
    
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['documents'] = self.object.documents.all()
        context['maintenance_records'] = self.object.maintenance_records.all().order_by('-maintenance_date')
        context['document_form'] = EquipmentDocumentForm()
        context['maintenance_form'] = MaintenanceRecordForm()
        return context


class EquipmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """View for creating new equipment."""
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    permission_required = 'equipment.add_equipment'
    
    def get_success_url(self):
        """Redirect to equipment detail view after successful creation."""
        return reverse_lazy('equipment:equipment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        """Process the form if it's valid."""
        messages.success(self.request, _('Equipment created successfully.'))
        return super().form_valid(form)

class EquipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """View for updating existing equipment."""
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    permission_required = 'equipment.change_equipment'
    
    def get_success_url(self):
        """Redirect to equipment detail view after successful update."""
        return reverse_lazy('equipment:equipment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        """Process the form if it's valid."""
        messages.success(self.request, _('Equipment updated successfully.'))
        return super().form_valid(form)

class EquipmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """View for deleting equipment."""
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment:equipment_list')
    permission_required = 'equipment.delete_equipment'
    
    def delete(self, request, *args, **kwargs):
        """Delete the equipment and show a success message."""
        messages.success(request, _('Equipment deleted successfully.'))
        return super().delete(request, *args, **kwargs)


@login_required
def add_equipment_document(request, equipment_id):
    """View for adding a document to equipment."""
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    
    if request.method == 'POST':
        form = EquipmentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.equipment = equipment
            document.save()
            messages.success(request, _('Document added successfully.'))
            return redirect('equipment:equipment_detail', pk=equipment_id)
    else:
        form = EquipmentDocumentForm()
    
    return render(request, 'equipment/document_form.html', {
        'form': form,
        'equipment': equipment
    })

@login_required
def delete_equipment_document(request, document_id):
    """View for deleting an equipment document."""
    document = get_object_or_404(EquipmentDocument, pk=document_id)
    equipment_id = document.equipment.id
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, _('Document deleted successfully.'))
        return redirect('equipment:equipment_detail', pk=equipment_id)
    
    return render(request, 'equipment/document_confirm_delete.html', {
        'document': document
    })

@login_required
def add_maintenance_record(request, equipment_id):
    """View for adding a maintenance record to equipment."""
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.equipment = equipment
            record.save()
            messages.success(request, _('Maintenance record added successfully.'))
            return redirect('equipment:equipment_detail', pk=equipment_id)
    else:
        form = MaintenanceRecordForm()
    
    return render(request, 'equipment/maintenance_form.html', {
        'form': form,
        'equipment': equipment
    })

@login_required
def delete_maintenance_record(request, record_id):
    """View for deleting a maintenance record."""
    record = get_object_or_404(MaintenanceRecord, pk=record_id)
    equipment_id = record.equipment.id
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, _('Maintenance record deleted successfully.'))
        return redirect('equipment:equipment_detail', pk=equipment_id)
    
    return render(request, 'equipment/maintenance_confirm_delete.html', {
        'record': record
    })

class MyEquipmentListView(ListView):
    model = EquipmentRegistry
    template_name = 'equipment/my_equipment_list.html'
    context_object_name = 'registry_entries'

    def get_queryset(self):
        return EquipmentRegistry.objects.filter(user=self.request.user)