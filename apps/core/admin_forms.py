from django import forms
from django.db import models
from unfold.admin import ModelAdmin as UnfoldModelAdmin


class CompactTextarea(forms.Textarea):
    """Textarea widget with controlled height."""

    def __init__(self, attrs=None, rows=3):
        default_attrs = {
            'rows': str(rows),
            'style': 'min-height: 80px; max-height: 160px; resize: vertical;',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class CompactAdminForm(forms.ModelForm):
    """Base ModelForm that applies compact widgets to all textareas."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('rows', '3')
                field.widget.attrs.setdefault(
                    'style',
                    'min-height: 80px; max-height: 160px; resize: vertical;'
                )


class AdminBase(UnfoldModelAdmin):
    """Base admin class for the entire project.
    - Enables Unfold's "+" add button in navigation
    - Always shows "Save and add another" option
    - Shows "Save and continue editing"
    """
    show_add_link = True

    class Media:
        css = {
            'all': ('css/admin.css',),
        }


def compact_form_fields(model_admin):
    """Apply compact textarea widgets to any ModelAdmin via formfield_overrides."""
    if not hasattr(model_admin, 'formfield_overrides') or model_admin.formfield_overrides is None:
        model_admin.formfield_overrides = {}
    model_admin.formfield_overrides[models.TextField] = {
        'widget': CompactTextarea(rows=3),
    }
    return model_admin
