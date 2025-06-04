### 📄 company/views.py**

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from company.models import Company, Department
from company.serializers import CompanySerializer, DepartmentSerializer




class CompanyPagination(PageNumberPagination):
    """Pielāgota lapošana uzņēmumu sarakstam."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class CompanyViewSet(viewsets.ModelViewSet):
    """Uzņēmuma API skatījums ar meklēšanu, kārtošanu un lapošanu."""

    queryset = Company.objects.filter(is_active=True).order_by("name")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "registration_number", "address", "email", "phone"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name"]

    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        """
        Get departments for a specific company.
        """
        company = self.get_object()
        departments = company.departments.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def active_departments(self, request, pk=None):
        """
        Get only active departments for a specific company.
        """
        company = self.get_object()
        departments = company.departments.filter(is_active=True)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


@login_required
def company_list(request):
    """
    Display a list of companies the user has access to.
    """
    # Filter companies based on user permissions
    if request.user.is_superuser:
        companies = Company.objects.all()
    else:
        companies = Company.objects.filter(
            id__in=request.user.companies.values_list('id', flat=True)
        )

    context = {
        'companies': companies,
        'title': _('Companies')
    }

    return render(request, 'company/company_list.html', context)


@login_required
def company_detail(request, pk):
    """
    Display detailed information about a company.
    """
    company = get_object_or_404(Company, pk=pk)

    # Check if user has access to this company
    if not request.user.is_superuser and not request.user.companies.filter(id=pk).exists():
        return render(request, '403.html', {'message': _('You do not have access to this company.')})

    departments = company.departments.all()

    context = {
        'company': company,
        'departments': departments,
        'title': company.name
    }

    return render(request, 'company/company_detail.html', context)


@login_required
@permission_required('company.add_department', raise_exception=True)
def add_department(request, company_id):
    """
    Add a new department to a company.
    """
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        code = request.POST.get('code')
        parent_id = request.POST.get('parent')

        if not name:
            messages.error(request, _('Department name is required'))
            return redirect('company:company_detail', pk=company_id)

        # Create the department
        department = Department(
            company=company,
            name=name,
            code=code,
            is_active=True
        )

        if parent_id:
            parent = get_object_or_404(Department, id=parent_id, company=company)
            department.parent = parent

        department.save()
        messages.success(request, _('Department added successfully'))
        return redirect('company:company_detail', pk=company_id)

    # Get parent departments for dropdown
    parent_departments = company.departments.all()

    context = {
        'company': company,
        'parent_departments': parent_departments,
        'title': _('Add Department')
    }

    return render(request, 'company/add_department.html', context)
