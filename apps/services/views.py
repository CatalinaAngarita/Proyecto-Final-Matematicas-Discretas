from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Service, ServiceCategory, NailApplicationType
from .forms import ServiceForm, ServiceCategoryForm, NailApplicationTypeForm


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:list')


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'
    success_url = reverse_lazy('services:list')


class ServiceCategoryListView(LoginRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'services/category_list.html'
    context_object_name = 'categories'


class ServiceCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'services/category_form.html'
    success_url = reverse_lazy('services:category_list')


class NailApplicationTypeListView(LoginRequiredMixin, ListView):
    model = NailApplicationType
    template_name = 'services/nail_type_list.html'
    context_object_name = 'nail_types'


class NailApplicationTypeCreateView(LoginRequiredMixin, CreateView):
    model = NailApplicationType
    form_class = NailApplicationTypeForm
    template_name = 'services/nail_type_form.html'
    success_url = reverse_lazy('services:nail_types_list')
