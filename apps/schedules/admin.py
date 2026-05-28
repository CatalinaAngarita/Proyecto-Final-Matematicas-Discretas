from django.contrib import admin
from apps.core.admin_forms import AdminBase
from .models import WorkSchedule, BreakSchedule, DayOff


@admin.register(WorkSchedule)
class WorkScheduleAdmin(AdminBase):
    list_display = ['specialist', 'day_of_week', 'morning_start', 'morning_end',
                    'afternoon_start', 'afternoon_end', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'specialist']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Asignación', {
            'fields': (('specialist', 'day_of_week'),),
        }),
        ('Bloque mañana', {
            'fields': (('morning_start', 'morning_end'),),
        }),
        ('Bloque tarde', {
            'fields': (('afternoon_start', 'afternoon_end'),),
        }),
        ('Estado y auditoría', {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                ('created_at', 'updated_at'),
            ),
        }),
    )


@admin.register(BreakSchedule)
class BreakScheduleAdmin(AdminBase):
    list_display = ['specialist', 'date', 'start_time', 'end_time', 'reason']
    list_filter = ['date', 'specialist']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información del descanso', {
            'fields': (
                ('specialist', 'date'),
                ('start_time', 'end_time'),
                'reason',
            ),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
    )


@admin.register(DayOff)
class DayOffAdmin(AdminBase):
    list_display = ['specialist', 'date', 'reason']
    list_filter = ['date', 'specialist']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información del día libre', {
            'fields': (
                ('specialist', 'date'),
                'reason',
            ),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
    )
