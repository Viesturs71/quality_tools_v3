from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import MethodInitialForm, MethodDetailForm
from apps.methods.models import MetozuRegistrs


class MethodListView(ListView):
    model = MetozuRegistrs
    template_name = 'methods/method_list.html'
    context_object_name = 'methods'


class MethodDetailView(DetailView):
    model = MetozuRegistrs
    template_name = 'methods/method_detail.html'


class MethodCreateView(CreateView):
    model = MetozuRegistrs
    form_class = MethodInitialForm
    template_name = 'methods/method_form.html'

    def get_success_url(self):
        return reverse('methods:method_list')


class MethodUpdateView(UpdateView):
    model = MetozuRegistrs
    form_class = MethodDetailForm
    template_name = 'methods/method_form.html'

    def get_success_url(self):
        return reverse('methods:method_detail', kwargs={'pk': self.object.pk})


def method_initial_view(request):
    if request.method == 'POST':
        form = MethodInitialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('methods:method_detail')
    else:
        form = MethodInitialForm()
    return render(request, 'methods/method_initial.html', {'form': form})


def method_detail_view(request):
    if request.method == 'POST':
        form = MethodDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('methods:method_success')
    else:
        form = MethodDetailForm()
    return render(request, 'methods/method_detail.html', {'form': form})


def method_success_view(request):
    return render(request, 'methods/method_success.html')