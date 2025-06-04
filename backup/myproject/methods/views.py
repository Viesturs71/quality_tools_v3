# methods/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import MethodDetailForm, MethodInitialForm
from .models import MetozuRegistrs


class MethodListView(LoginRequiredMixin, ListView):
    model = MetozuRegistrs
    template_name = 'methods/method_list.html'
    context_object_name = 'methods'
    login_url = 'login'

class MethodCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MetozuRegistrs
    form_class = MethodInitialForm
    template_name = 'methods/method_initial_form.html'
    success_message = "Metode %(name)s veiksmīgi izveidota!"
    login_url = 'login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class MethodDetailView(LoginRequiredMixin, DetailView):
    model = MetozuRegistrs
    template_name = 'methods/method_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MethodDetailForm(instance=self.object)
        return context

class MethodUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MetozuRegistrs
    form_class = MethodDetailForm
    template_name = 'methods/method_detail.html'
    success_message = "Metodes dati veiksmīgi atjaunināti!"
    login_url = 'login'

@login_required
def method_list(request):
    methods = Method.objects.all()
    return render(request, 'methods/method_list.html', {'methods': methods})

