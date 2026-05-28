from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WorkSchedule, BreakSchedule, DayOff
from .forms import WorkScheduleForm, BreakScheduleForm, DayOffForm


class WorkScheduleListView(LoginRequiredMixin, ListView):
    model = WorkSchedule
    template_name = 'schedules/work_schedule_list.html'
    context_object_name = 'schedules'


class WorkScheduleCreateView(LoginRequiredMixin, CreateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    template_name = 'schedules/work_schedule_form.html'
    success_url = reverse_lazy('schedules:work_list')


class WorkScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    template_name = 'schedules/work_schedule_form.html'
    success_url = reverse_lazy('schedules:work_list')


class WorkScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkSchedule
    template_name = 'schedules/work_schedule_confirm_delete.html'
    success_url = reverse_lazy('schedules:work_list')


class BreakScheduleListView(LoginRequiredMixin, ListView):
    model = BreakSchedule
    template_name = 'schedules/break_list.html'
    context_object_name = 'breaks'


class BreakScheduleCreateView(LoginRequiredMixin, CreateView):
    model = BreakSchedule
    form_class = BreakScheduleForm
    template_name = 'schedules/break_form.html'
    success_url = reverse_lazy('schedules:break_list')


class DayOffListView(LoginRequiredMixin, ListView):
    model = DayOff
    template_name = 'schedules/day_off_list.html'
    context_object_name = 'days_off'


class DayOffCreateView(LoginRequiredMixin, CreateView):
    model = DayOff
    form_class = DayOffForm
    template_name = 'schedules/day_off_form.html'
    success_url = reverse_lazy('schedules:day_off_list')
