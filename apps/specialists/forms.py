from django import forms
from .models import Specialist


class SpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        fields = ['first_name', 'last_name', 'phone', 'email', 'is_primary', 'services', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
