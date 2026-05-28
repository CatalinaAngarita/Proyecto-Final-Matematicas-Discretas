from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Appointment
from .forms import AppointmentForm


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('client', 'specialist', 'service')
        date_filter = self.request.GET.get('date')
        status_filter = self.request.GET.get('status')
        if date_filter:
            qs = qs.filter(date=date_filter)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:list')


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointments:list')


class AppointmentCancelView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['status', 'cancellation_reason', 'is_cancelled_by_client']
    template_name = 'appointments/appointment_cancel.html'
    success_url = reverse_lazy('appointments:list')


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointments:list')
