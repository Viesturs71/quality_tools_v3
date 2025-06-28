# apps/standards/views.py

from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import (
    StandardCategory, Standard, StandardSection,
    StandardDocument, StandardDocumentLink, StandardCompliance
)


@login_required
def search_standards(request):
    query = request.GET.get('q', '')
    standards = Standard.objects.filter(title__icontains=query)
    return render(request, 'standards/search.html', {'standards': standards, 'query': query})

class StandardCategoryListView(LoginRequiredMixin, ListView):
    model = StandardCategory
    template_name = 'standards/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

class StandardListView(LoginRequiredMixin, ListView):
    model = Standard
    template_name = 'standards/standard_list.html'
    context_object_name = 'standards'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        if cat := self.request.GET.get('category'):
            qs = qs.filter(category_id=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = StandardCategory.objects.all()
        return ctx

class StandardDetailView(LoginRequiredMixin, DetailView):
    model = Standard
    template_name = 'standards/standard_detail.html'
    context_object_name = 'standard'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sections'] = self.object.sections.filter(parent=None).order_by('order','code')
        return ctx

class StandardSectionDetailView(LoginRequiredMixin, DetailView):
    model = StandardSection
    template_name = 'standards/section_detail.html'
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['subsections']    = self.object.subsections.all().order_by('order','code')
        ctx['requirements']   = self.object.requirements.all().order_by('order','code')
        links                  = self.object.document_links.select_related('document')
        ctx['document_links'] = links
        total = links.count()
        compliant = links.filter(compliance_status='compliant').count()
        ctx['compliance_percentage'] = (compliant/total*100) if total else 0
        ctx['available_documents']   = StandardDocument.objects.filter(is_active=True)
        return ctx

class StandardDocumentListView(LoginRequiredMixin, ListView):
    model = StandardDocument
    template_name = 'standards/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

class StandardDocumentDetailView(LoginRequiredMixin, DetailView):
    model = StandardDocument
    template_name = 'standards/document_detail.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['standard_links'] = self.object.standard_links.select_related('standard_section')
        ctx['available_sections'] = StandardSection.objects.all()
        return ctx

class ComplianceReportView(LoginRequiredMixin, TemplateView):
    template_name = "standards/compliance_report.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        standards_data = []
        for std in Standard.objects.filter(is_active=True):
            sections = StandardSection.objects.filter(standard=std)
            section_ids = sections.values_list('id', flat=True)
            stats = StandardDocumentLink.objects.filter(
                standard_section_id__in=section_ids
            ).aggregate(
                total=Count('id'),
                compliant=Count(Case(When(compliance_status='compliant', then=1), output_field=IntegerField())),
                partial=Count(Case(When(compliance_status='partial', then=1), output_field=IntegerField())),
                non_compliant=Count(Case(When(compliance_status='non_compliant', then=1), output_field=IntegerField())),
                in_progress=Count(Case(When(compliance_status='in_progress', then=1), output_field=IntegerField())),
            )
            total = stats['total']
            pct   = (stats['compliant']/total*100) if total else 0
            standards_data.append({
                'standard': std,
                'sections_count': sections.count(),
                'links_by_status': stats,
                'compliance_percentage': round(pct,1),
            })
        ctx['standards_data'] = standards_data
        return ctx

# if you still need the old FBVs, just import and render from the models above.
