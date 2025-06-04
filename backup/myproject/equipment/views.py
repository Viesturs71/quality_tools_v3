# equipment/views.py
from __future__ import annotations

# ──────────────────────
#  Standarta Django
# ──────────────────────
from datetime import date, timedelta

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
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .forms import EquipmentDocumentForm, EquipmentForm, MaintenanceRecordForm

# ──────────────────────
#  Lokālie importi
# ──────────────────────
from .models import Equipment, EquipmentType
from .serializers import (
    EquipmentSerializer,  # Change this from EquipmentRegistrySerializer
)

#   → Department ir obligāts tikai tad,
#     ja aplikācija “company” ir reģistrēta
HAS_DEPARTMENT = "company" in settings.INSTALLED_APPS
if HAS_DEPARTMENT:
    try:
        from django.apps import apps

        Department = apps.get_model("company", "Department")
    except (ImportError, LookupError):
        HAS_DEPARTMENT = False
        Department = None  # type: ignore

# Pievienojam noturīgu importu
try:
    from personnel.models import Department
    HAS_DEPARTMENT = True
except ImportError:
    HAS_DEPARTMENT = False

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
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Use only valid fields for select_related
        try:
            queryset = queryset.select_related('equipment_type', 'department')
        except:
            pass

        # Filter by department if specified
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Try to get departments - handle safely
        departments = []
        
        # First check if we have Department from the HAS_DEPARTMENT check earlier
        if HAS_DEPARTMENT and Department:
            try:
                departments = Department.objects.all()
            except Exception:
                pass
        
        # If we still don't have departments, check if it's in our own app
        if not departments:
            try:
                from equipment.models import Department
                departments = Department.objects.all()
            except (ImportError, AttributeError):
                pass
                
        context['departments'] = departments

        context['selected_department'] = self.request.GET.get('department')
        return context


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = "equipment/equipment_detail.html"
    context_object_name = "equipment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = self.object.documents.all()
        context["maintenance_records"] = self.object.maintenance_records.all()
        return context


class EquipmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "equipment.add_equipment"
    model = Equipment
    form_class = EquipmentForm
    template_name = "equipment/equipment_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, _("Equipment successfully created."))
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Equipment added successfully."))
        return reverse_lazy("equipment:equipment_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        ctx.update(
            {
                "page_title": _("Add new equipment"),
                "today_date": today,
                "next_week": today + timedelta(days=7),
                "next_month": today + relativedelta(months=1),
                "next_quarter": today + relativedelta(months=3),
                "next_year": today + relativedelta(years=1),
            }
        )
        return ctx


class EquipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "equipment.change_equipment"
    model = Equipment
    form_class = EquipmentForm
    template_name = "equipment/equipment_form.html"

    def form_valid(self, form):
        messages.success(self.request, _("Equipment successfully updated."))
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Equipment updated successfully."))
        return reverse_lazy("equipment:equipment_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_measuring_instrument"] = self.object.is_measuring_instrument
        return context


class EquipmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "equipment.delete_equipment"
    model = Equipment
    template_name = "equipment/equipment_confirm_delete.html"
    success_url = reverse_lazy("equipment:index")

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Equipment successfully deleted."))
        return super().delete(request, *args, **kwargs)


# ──────────────────────
#  Vienkāršs funkciju skats (atstāts)
# ──────────────────────
@login_required
def equipment_list(request):
    """Vienkārša funkcija – saraksta skats (paliek saderībai)."""
    return render(
        request,
        "equipment/equipment_list.html",
        {"page_title": _("Equipment list")},
    )
# ════════════════════════════════════════
#  Iekārtu tipu (kategoriju) skati
# ════════════════════════════════════════
class EquipmentTypeListView(LoginRequiredMixin, ListView):
    """
    Parāda visas iekārtu kategorijas / tipus.
    URL:  /equipment/categories/
    """
    model = EquipmentType
    template_name = "equipment/equipmenttype_list.html"
    context_object_name = "equipment_type_list"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = _("Equipment categories")
        return ctx


class EquipmentTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "equipment.add_equipmenttype"
    model = EquipmentType
    fields = ["name", "description"]          # vai tavs pilnais lauku saraksts
    template_name = "equipment/equipmenttype_form.html"
    success_url = reverse_lazy("equipment:category_list")


class EquipmentTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "equipment.change_equipmenttype"
    model = EquipmentType
    fields = ["name", "description"]
    template_name = "equipment/equipmenttype_form.html"
    success_url = reverse_lazy("equipment:category_list")


@login_required
def equipment_detail(request, pk):
    """Display details for a specific equipment item"""
    equipment = get_object_or_404(Equipment, pk=pk)

    # Get related maintenance records
    maintenance_records = []  # You'll need to implement this model

    # Get status history
    status_history = []  # You'll need to implement this model

    # Calculate date references for status indicators
    today = timezone.now().date()
    in_30_days = today + timezone.timedelta(days=30)

    context = {
        'equipment': equipment,
        'maintenance_records': maintenance_records,
        'status_history': status_history,
        'today': today.isoformat(),
        'in_30_days': in_30_days.isoformat(),
    }

    return render(request, 'equipment/detail.html', context)


@login_required
def equipment_create(request):
    """Create new equipment item"""
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, _("Equipment added successfully."))
            return redirect('equipment:detail', pk=equipment.pk)
    else:
        form = EquipmentForm()

    context = {
        'form': form,
        'title': _('Add New Equipment'),
    }

    return render(request, 'equipment/form.html', context)


@login_required
def equipment_update(request, pk):
    """Update existing equipment item"""
    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, _("Equipment updated successfully."))
            return redirect('equipment:detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)

    context = {
        'form': form,
        'equipment': equipment,
        'title': _('Edit Equipment'),
    }

    return render(request, 'equipment/form.html', context)


@login_required
def equipment_delete(request, pk):
    """Delete equipment item"""
    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == 'POST':
        equipment.delete()
        messages.success(request, _("Equipment deleted successfully."))
        return redirect('equipment:index')

    context = {
        'equipment': equipment,
    }

    return render(request, 'equipment/delete_confirm.html', context)


@login_required
def add_document(request, equipment_id):
    """Add document to equipment"""
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        form = EquipmentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.equipment = equipment
            document.save()
            messages.success(request, _("Document added successfully."))
            return redirect('equipment:detail', pk=equipment_id)
    else:
        form = EquipmentDocumentForm()

    context = {
        'form': form,
        'equipment': equipment,
        'title': _('Add Document'),
    }

    return render(request, 'equipment/document_form.html', context)


@login_required
def add_maintenance(request, equipment_id):
    """Add maintenance record to equipment"""
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.equipment = equipment
            maintenance.save()
            messages.success(request, _("Maintenance record added successfully."))
            return redirect('equipment:detail', pk=equipment_id)
    else:
        form = MaintenanceRecordForm()

    context = {
        'form': form,
        'equipment': equipment,
        'title': _('Add Maintenance Record'),
    }

    return render(request, 'equipment/maintenance_form.html', context)
