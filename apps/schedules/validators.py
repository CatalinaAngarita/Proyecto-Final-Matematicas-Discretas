from django.core.exceptions import ValidationError
from datetime import time


def validate_business_hours(start: time, end: time):
    if start >= end:
        raise ValidationError('La hora de inicio debe ser anterior a la hora de fin.')


def validate_time_slot(start: time, end: time, slot_minutes: int = 30):
    total = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
    if total < slot_minutes:
        raise ValidationError(
            f'El bloque debe tener al menos {slot_minutes} minutos.'
        )
