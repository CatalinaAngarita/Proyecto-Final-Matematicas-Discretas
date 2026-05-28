from django.contrib import admin
from django.db import models
from apps.core.admin_forms import CompactTextarea
from .models import Testimonial


admin.site.site_header = 'Diana Nails — Panel Administrativo'
admin.site.site_title = 'Diana Nails Admin'
admin.site.index_title = 'Bienvenido al panel de administración'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating_stars', 'is_active', 'order', 'created_at']
    list_filter = ['rating', 'is_active']
    search_fields = ['client_name', 'content']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    formfield_overrides = {
        models.TextField: {'widget': CompactTextarea(rows=3)},
    }

    fieldsets = (
        ('Información', {
            'fields': (
                ('client_name', 'rating'),
                ('is_active', 'order'),
            ),
        }),
        ('Opinión', {
            'fields': ('content',),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
    )

    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = 'Calificación'
