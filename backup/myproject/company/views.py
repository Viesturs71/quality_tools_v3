### 📄 company/views.py**

from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Company
from .serializers import CompanySerializer


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
