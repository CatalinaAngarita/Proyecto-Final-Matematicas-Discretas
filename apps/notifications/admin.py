from django.contrib import admin
from django.db import models
from apps.core.admin_forms import AdminBase, CompactTextarea
from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(AdminBase):
    list_display = [
        'appointment_short', 'notification_type', 'recipient_phone',
        'status', 'scheduled_at', 'sent_at', 'attempt_count',
    ]
    list_filter = ['notification_type', 'status', 'channel', 'provider', 'created_at']
    search_fields = ['recipient_phone', 'appointment__client__first_name']
    readonly_fields = ['created_at', 'updated_at', 'sent_at', 'attempt_count']
    date_hierarchy = 'scheduled_at'
    list_editable = ['status']
    formfield_overrides = {
        models.TextField: {'widget': CompactTextarea(rows=3)},
    }

    fieldsets = (
        ('Cita y tipo', {
            'fields': (
                ('appointment', 'notification_type'),
                ('recipient_phone', 'channel'),
            ),
        }),
        ('Mensaje', {
            'fields': ('message',),
        }),
        ('Estado y programación', {
            'fields': (
                ('status', 'scheduled_at'),
                ('sent_at', 'provider'),
            ),
        }),
        ('Errores y tracking', {
            'fields': (
                ('attempt_count', 'whatsapp_message_id'),
                'error_message',
            ),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
    )

    def appointment_short(self, obj):
        return f'#{str(obj.appointment.pk)[:8]}'
    appointment_short.short_description = 'Cita'
