from django.contrib import admin
from .models import CancellationStat, ServiceStat


@admin.register(CancellationStat)
class CancellationStatAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_appointments', 'cancelled_count',
                    'no_show_count', 'completed_count', 'cancellation_rate']
    list_filter = ['date']
    date_hierarchy = 'date'


@admin.register(ServiceStat)
class ServiceStatAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'total_bookings', 'total_revenue', 'month']
    list_filter = ['month']
