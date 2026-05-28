from django.contrib import admin
from django.db import models
from apps.core.admin_forms import AdminBase, CompactTextarea
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(AdminBase):
    list_display = [
        'id', 'client', 'specialist', 'service', 'date',
        'start_time', 'end_time', 'status', 'created_at'
    ]
    list_filter = ['status', 'date', 'specialist']
    search_fields = ['client__first_name', 'client__last_name', 'client__phone']
    date_hierarchy = 'date'
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'completed_at']
    formfield_overrides = {
        models.TextField: {'widget': CompactTextarea(rows=3)},
    }

    fieldsets = (
        ('Información principal', {
            'fields': (
                ('client', 'specialist'),
                ('service', 'nail_application_type'),
            ),
        }),
        ('Horario', {
            'fields': (
                ('date',),
                ('start_time', 'end_time'),
            ),
        }),
        ('Estado', {
            'fields': (
                ('status',),
            ),
        }),
        ('Cancelación', {
            'fields': (
                ('is_cancelled_by_client', 'cancelled_at'),
                'cancellation_reason',
            ),
        }),
        ('Notas', {
            'fields': ('notes',),
        }),
        ('Hitos de tiempo', {
            'classes': ('collapse',),
            'fields': (
                ('confirmed_at', 'completed_at'),
            ),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (
                ('created_at', 'updated_at'),
                'rescheduled_from',
            ),
        }),
    )
