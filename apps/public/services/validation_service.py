from datetime import date, time
from uuid import UUID
from django.core.exceptions import ValidationError
from apps.appointments.models import Appointment
from apps.core.models import AppointmentStatus
from apps.schedules.models import WorkSchedule, DayOff, BreakSchedule


def validate_booking(
    specialist_id: UUID,
    appointment_date: date,
    start_time: time,
    end_time: time,
    exclude_appointment_id: UUID = None,
):
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
        raise ValidationError('No hay horario disponible para esta fecha.')

    morning_ok = (
        schedule.morning_start <= start_time and end_time <= schedule.morning_end
    )
    afternoon_ok = (
        schedule.afternoon_start <= start_time and end_time <= schedule.afternoon_end
    )

    if not (morning_ok or afternoon_ok):
        raise ValidationError(
            'El horario debe estar dentro del horario laboral (8:00-12:00 o 13:00-20:00).'
        )

    breaks = BreakSchedule.objects.filter(
        specialist_id=specialist_id, date=appointment_date
    )
    for b in breaks:
        if start_time < b.end_time and end_time > b.start_time:
            raise ValidationError(
                f'La especialista tiene un descanso de {b.start_time.strftime("%H:%M")} a {b.end_time.strftime("%H:%M")}.'
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
                f'Ocupado de {apt.start_time.strftime("%H:%M")} a {apt.end_time.strftime("%H:%M")}.'
            )


def get_available_slots_for_service(specialist_id: UUID, appointment_date: date, service_duration: int):
    from datetime import datetime, timedelta
    from apps.schedules.models import WorkSchedule, BreakSchedule, DayOff

    if DayOff.objects.filter(
        specialist_id=specialist_id, date=appointment_date
    ).exists():
        return []

    day_of_week = appointment_date.weekday()

    try:
        schedule = WorkSchedule.objects.get(
            specialist_id=specialist_id, day_of_week=day_of_week, is_active=True
        )
    except WorkSchedule.DoesNotExist:
        return []

    blocks = [
        (schedule.morning_start, schedule.morning_end),
        (schedule.afternoon_start, schedule.afternoon_end),
    ]

    breaks = list(BreakSchedule.objects.filter(
        specialist_id=specialist_id, date=appointment_date
    ))

    active_statuses = [
        AppointmentStatus.PENDING,
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.IN_PROGRESS,
    ]
    existing = list(Appointment.objects.filter(
        specialist_id=specialist_id,
        date=appointment_date,
        status__in=active_statuses,
    ).order_by('start_time'))

    slots = []
    for block_start, block_end in blocks:
        current = datetime.combine(appointment_date, block_start)
        end = datetime.combine(appointment_date, block_end)
        step = timedelta(minutes=30)

        while current + timedelta(minutes=service_duration) <= end:
            slot_start = current.time()
            slot_end = (current + timedelta(minutes=service_duration)).time()

            if _is_in_break(slot_start, slot_end, breaks):
                current += step
                continue

            if _has_overlap(slot_start, slot_end, existing):
                current += step
                continue

            slots.append({
                'start': slot_start,
                'end': slot_end,
                'start_str': slot_start.strftime('%H:%M'),
                'end_str': slot_end.strftime('%H:%M'),
            })

            current += step

    return slots


def _is_in_break(start: time, end: time, breaks) -> bool:
    for b in breaks:
        if start < b.end_time and end > b.start_time:
            return True
    return False


def _has_overlap(start: time, end: time, appointments) -> bool:
    for apt in appointments:
        if start < apt.end_time and end > apt.start_time:
            return True
    return False
