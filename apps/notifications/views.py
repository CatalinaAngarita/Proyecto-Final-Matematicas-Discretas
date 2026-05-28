from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NotificationLog


class NotificationLogListView(LoginRequiredMixin, ListView):
    model = NotificationLog
    template_name = 'notifications/notification_log_list.html'
    context_object_name = 'logs'
    paginate_by = 50
    ordering = ['-created_at']
