from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Audit


class AuditListView(LoginRequiredMixin, ListView):
    model = Audit
    template_name = 'audits/audit_list.html'
    context_object_name = 'audits'

class AuditDetailView(LoginRequiredMixin, DetailView):
    model = Audit
    template_name = 'audits/audit_detail.html'

class AuditCreateView(LoginRequiredMixin, CreateView):
    model = Audit
    template_name = 'audits/audit_form.html'
    fields = ['title', 'description', 'date', 'status']
    success_url = reverse_lazy('audits:audit_list')

class AuditUpdateView(LoginRequiredMixin, UpdateView):
    model = Audit
    template_name = 'audits/audit_form.html'
    fields = ['title', 'description', 'date', 'status']
    success_url = reverse_lazy('audits:audit_list')

class AuditDeleteView(LoginRequiredMixin, DeleteView):
    model = Audit
    template_name = 'audits/audit_confirm_delete.html'
    success_url = reverse_lazy('audits:audit_list')
