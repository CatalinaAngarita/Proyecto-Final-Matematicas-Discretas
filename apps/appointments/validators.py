from datetime import date, time
from uuid import UUID
from django.core.exceptions import ValidationError
from .models import Appointment
from apps.core.models import AppointmentStatus
from apps.schedules.models import WorkSchedule, DayOff, BreakSchedule


def validate_appointment_time(
    specialist_id: UUID,
    appointment_date: date,
    start_time: time,
    end_time: time,
    exclude_appointment_id: UUID = None
):
    """
    Validación completa de disponibilidad de horario para una cita.

    1. La fecha no puede ser pasada
    2. La hora de inicio debe ser anterior a la de fin
    3. El especialista no debe tener día libre
    4. Debe existir un horario laboral definido para ese día
    5. El horario debe estar dentro de los bloques laborales
    6. No debe coincidir con un descanso programado
    7. No debe solaparse con otra cita existente
    """
    if appointment_date < date.today():
        raise ValidationError('No se pueden agendar citas en fechas pasadas.')

    if start_time >= end_time:
        raise ValidationError('La hora de inicio debe ser anterior a la hora de fin.')

    day_of_week = appointment_date.weekday()

    if DayOff.objects.filter(
        specialist_id=specialist_id, date=appointment_date
    ).exists():
        raise ValidationError('La especialista no labora esta fecha.')

    try:
        schedule = WorkSchedule.objects.get(
            specialist_id=specialist_id, day_of_week=day_of_week, is_active=True
        )
    except WorkSchedule.DoesNotExist:
        raise ValidationError('No hay horario definido para este día.')

    morning_ok = (
        schedule.morning_start <= start_time and end_time <= schedule.morning_end
    )
    afternoon_ok = (
        schedule.afternoon_start <= start_time and end_time <= schedule.afternoon_end
    )

    if not (morning_ok or afternoon_ok):
        raise ValidationError(
            'El horario debe estar dentro del horario laboral '
            '(8:00-12:00 o 13:00-20:00).'
        )

    breaks = BreakSchedule.objects.filter(
        specialist_id=specialist_id, date=appointment_date
    )
    for b in breaks:
        if start_time < b.end_time and end_time > b.start_time:
            raise ValidationError(
                f'La especialista tiene un descanso de {b.start_time} a {b.end_time}.'
            )

    active_statuses = [
        AppointmentStatus.PENDING,
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.IN_PROGRESS,
    ]
    appointments = Appointment.objects.filter(
        specialist_id=specialist_id,
        date=appointment_date,
        status__in=active_statuses,
    )
    if exclude_appointment_id:
        appointments = appointments.exclude(id=exclude_appointment_id)

    for apt in appointments:
        if start_time < apt.end_time and end_time > apt.start_time:
            raise ValidationError(
                'Ya existe una cita en este horario. '
                f'Ocupado de {apt.start_time} a {apt.end_time}.'
            )


def get_available_slots_for_date(
    specialist_id: UUID,
    appointment_date: date,
    service_duration: int
):
    """Retorna slots disponibles como lista de tuplas (start, end)."""
    from apps.schedules.services.availability import get_available_slots
    return get_available_slots(specialist_id, appointment_date, service_duration)
