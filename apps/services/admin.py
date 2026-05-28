from django.contrib import admin
from django.db import models
from apps.core.admin_forms import AdminBase, CompactTextarea
from .models import Service, ServiceCategory, NailApplicationType

formfield_overrides = {
    models.TextField: {'widget': CompactTextarea(rows=3)},
}


class BaseServiceAdmin(AdminBase):
    list_editable = ['is_active']
    search_fields = ['name']
    formfield_overrides = formfield_overrides


@admin.register(Service)
class ServiceAdmin(AdminBase):
    list_display = ['name', 'category', 'service_category', 'duration_minutes', 'price', 'is_active']
    list_filter = ['category', 'service_category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'price']
    readonly_fields = ['created_at', 'updated_at']
    formfield_overrides = formfield_overrides

    fieldsets = (
        ('Información del servicio', {
            'fields': (
                ('name', 'category'),
                ('service_category',),
            ),
        }),
        ('Precio y duración', {
            'fields': (
                ('price', 'duration_minutes'),
            ),
        }),
        ('Descripción', {
            'fields': ('description',),
        }),
        ('Estado y auditoría', {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                ('created_at', 'updated_at'),
            ),
        }),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(BaseServiceAdmin):
    list_display = ['name', 'description', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información', {
            'fields': (
                ('name', 'is_active'),
                'description',
            ),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
    )


@admin.register(NailApplicationType)
class NailApplicationTypeAdmin(BaseServiceAdmin):
    list_display = ['name', 'description', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información', {
            'fields': (
                ('name', 'is_active'),
                'description',
            ),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
    )
