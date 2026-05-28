from django import forms
from .models import WorkSchedule, BreakSchedule, DayOff


class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ['specialist', 'day_of_week', 'morning_start', 'morning_end',
                  'afternoon_start', 'afternoon_end']
        widgets = {
            'specialist': forms.Select(attrs={'class': 'form-select'}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'morning_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'morning_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'afternoon_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'afternoon_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class BreakScheduleForm(forms.ModelForm):
    class Meta:
        model = BreakSchedule
        fields = ['specialist', 'date', 'start_time', 'end_time', 'reason']
        widgets = {
            'specialist': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DayOffForm(forms.ModelForm):
    class Meta:
        model = DayOff
        fields = ['specialist', 'date', 'reason']
        widgets = {
            'specialist': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }
