from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Specialist
from .forms import SpecialistForm


class SpecialistListView(LoginRequiredMixin, ListView):
    model = Specialist
    template_name = 'specialists/specialist_list.html'
    context_object_name = 'specialists'


class SpecialistCreateView(LoginRequiredMixin, CreateView):
    model = Specialist
    form_class = SpecialistForm
    template_name = 'specialists/specialist_form.html'
    success_url = reverse_lazy('specialists:list')


class SpecialistUpdateView(LoginRequiredMixin, UpdateView):
    model = Specialist
    form_class = SpecialistForm
    template_name = 'specialists/specialist_form.html'
    success_url = reverse_lazy('specialists:list')


class SpecialistDeleteView(LoginRequiredMixin, DeleteView):
    model = Specialist
    template_name = 'specialists/specialist_confirm_delete.html'
    success_url = reverse_lazy('specialists:list')
