from django import forms
from apps.services.models import Service


class ServiceSelectionForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label='Selecciona un servicio',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'serviceSelect'}),
        label='¿Qué servicio deseas?',
    )


class DateTimeSelectionForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': ''}),
        label='Selecciona la fecha',
    )
    time_slot = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect(attrs={'class': 'btn-check', 'id': ''}),
        label='Selecciona el horario',
    )

    def __init__(self, *args, **kwargs):
        slots = kwargs.pop('slots', [])
        super().__init__(*args, **kwargs)
        if slots:
            choices = [(s['start_str'], f"{s['start_str']} — {s['end_str']}") for s in slots]
            self.fields['time_slot'].choices = choices
        else:
            self.fields['time_slot'].choices = []
            self.fields['time_slot'].widget = forms.HiddenInput()


class ClientInfoForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg', 'placeholder': 'Ej: María',
            'autocomplete': 'given-name',
        }),
        label='Tu nombre',
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg', 'placeholder': 'Ej: Pérez',
            'autocomplete': 'family-name',
        }),
        label='Tus apellidos',
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg', 'placeholder': '+57 300 123 4567',
            'type': 'tel', 'autocomplete': 'tel',
        }),
        label='Tu número de WhatsApp',
        help_text='Te enviaremos un recordatorio de tu cita',
    )
