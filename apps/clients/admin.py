from django.contrib import admin
from django.db import models
from apps.core.admin_forms import AdminBase, CompactTextarea
from .models import Client


@admin.register(Client)
class ClientAdmin(AdminBase):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'total_visits', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    list_editable = ['is_active']
    ordering = ['-created_at']
    readonly_fields = ['total_visits', 'last_visit_date', 'created_at', 'updated_at']
    formfield_overrides = {
        models.TextField: {'widget': CompactTextarea(rows=3)},
    }

    fieldsets = (
        ('Información personal', {
            'fields': (
                ('first_name', 'last_name'),
                ('birth_date',),
            ),
        }),
        ('Contacto', {
            'fields': (
                ('phone', 'email'),
            ),
        }),
        ('Seguimiento', {
            'fields': (
                ('total_visits', 'last_visit_date'),
            ),
        }),
        ('Notas internas', {
            'fields': ('notes',),
        }),
        ('Estado y auditoría', {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                ('created_at', 'updated_at'),
            ),
        }),
    )
