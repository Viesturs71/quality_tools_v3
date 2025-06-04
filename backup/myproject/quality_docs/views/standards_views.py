# --- 3. standards_views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from quality_docs.models.standards import Standard


class StandardListView(ListView):
    model = Standard
    template_name = "quality_docs/standard_list.html"
    context_object_name = "standards"

@login_required
def standard_detail(request, pk):
    standard = get_object_or_404(Standard, pk=pk)
    return render(request, "quality_docs/standard_detail.html", {"standard": standard})
