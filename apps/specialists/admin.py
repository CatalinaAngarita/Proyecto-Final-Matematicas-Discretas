from django.contrib import admin
from django.db import models
from apps.core.admin_forms import AdminBase, CompactTextarea
from .models import Specialist


@admin.register(Specialist)
class SpecialistAdmin(AdminBase):
    list_display = ['first_name', 'last_name', 'phone', 'is_primary', 'is_active']
    list_filter = ['is_primary', 'is_active']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    list_editable = ['is_active']
    filter_horizontal = ['services']
    readonly_fields = ['created_at', 'updated_at']
    formfield_overrides = {
        models.TextField: {'widget': CompactTextarea(rows=3)},
    }

    fieldsets = (
        ('Información personal', {
            'fields': (
                ('first_name', 'last_name'),
                ('user',),
            ),
        }),
        ('Contacto', {
            'fields': (
                ('phone', 'email'),
            ),
        }),
        ('Servicios y foto', {
            'fields': (
                'services',
                'photo',
            ),
        }),
        ('Notas', {
            'fields': ('notes',),
        }),
        ('Estado y auditoría', {
            'classes': ('collapse',),
            'fields': (
                ('is_primary', 'is_active'),
                ('created_at', 'updated_at'),
            ),
        }),
    )
