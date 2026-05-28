from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CancellationStat, ServiceStat


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/analytics_dashboard.html'


class CancellationStatsListView(LoginRequiredMixin, ListView):
    model = CancellationStat
    template_name = 'analytics/cancellation_stats_list.html'
    context_object_name = 'stats'
    paginate_by = 30
    ordering = ['-date']


class ServiceStatsListView(LoginRequiredMixin, ListView):
    model = ServiceStat
    template_name = 'analytics/service_stats_list.html'
    context_object_name = 'stats'
    paginate_by = 30
    ordering = ['-month']
