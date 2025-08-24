# apps/standards/views.py

from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from .utils import check_document_compliance, check_standard_compliance, get_overall_compliance_report
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

class ComplianceReportView(TemplateView):
    template_name = "standards/compliance_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compliance_data'] = get_overall_compliance_report()
        return context

def document_compliance_check(request, document_id):
    """
    API endpoint to check compliance for a specific document.
    """
    compliance_data = check_document_compliance(document_id)
    if compliance_data:
        return JsonResponse(compliance_data, safe=False)
    else:
        return JsonResponse({'error': 'Document not found'}, status=404)

def standard_compliance_check(request, standard_section_id):
    """
    API endpoint to check compliance for a specific standard section.
    """
    compliance_data = check_standard_compliance(standard_section_id)
    if compliance_data:
        return JsonResponse(compliance_data, safe=False)
    else:
        return JsonResponse({'error': 'Standard section not found'}, status=404)
                in_progress=Count(Case(
                    When(compliance_status='in_progress', then=1),
                    output_field=IntegerField()
                ))
            )
            total = links_by_status['total']
            compliant = links_by_status['compliant']
            compliance_percentage = (compliant / total * 100) if total > 0 else 0
            standards_data.append({
                'standard': standard,
                'sections_count': len(sections),
                'links_by_status': links_by_status,
                'compliance_percentage': round(compliance_percentage, 1)
            })
        ctx['standards_data'] = standards_data
        return ctx

def check_compliance(standard_section_id, document_id):
    """
    Returns compliance status for given standard section and document.
    """
    try:
        link = StandardDocumentLink.objects.get(
            standard_section_id=standard_section_id,
            document_id=document_id
        )
        return {
            'compliance_status': link.compliance_status,
            'notes': link.notes,
            'created_at': link.created_at,
            'updated_at': link.updated_at,
            'created_by': link.created_by,
        }
    except StandardDocumentLink.DoesNotExist:
        return None

# if you still need the old FBVs, just import and render from the models above.
