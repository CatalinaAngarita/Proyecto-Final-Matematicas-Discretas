from datetime import date, time, datetime, timedelta
from typing import List, Dict, Tuple, Optional
from uuid import UUID
from .models import Appointment
from apps.core.models import AppointmentStatus


def find_optimal_slot(
    specialist_id: UUID,
    target_date: date,
    duration_minutes: int,
    available_slots: List[Tuple[time, time]]
) -> Optional[Tuple[time, time]]:
    """
    Algoritmo para encontrar el slot óptimo disponible.

    Estrategia:
    1. Toma los slots disponibles del día
    2. Filtra los que tienen duración suficiente
    3. Elimina los que se solapan con citas existentes
    4. Entre los restantes, elige el que DEJA MENOR HUECO
       antes de la cita (para minimizar tiempos muertos)

    Retorna (start_time, end_time) o None si no hay slot disponible.
    """
    if not available_slots:
        return None

    active_statuses = [
        AppointmentStatus.PENDING,
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.IN_PROGRESS,
    ]

    existing = Appointment.objects.filter(
        specialist_id=specialist_id,
        date=target_date,
        status__in=active_statuses,
    ).order_by('start_time')

    if not existing.exists():
        return available_slots[0]

    appointments_today = list(existing)
    best_slot = None
    best_gap = float('inf')

    for slot_start, slot_end in available_slots:
        slot_duration = (
            (slot_end.hour * 60 + slot_end.minute) -
            (slot_start.hour * 60 + slot_start.minute)
        )
        if slot_duration < duration_minutes:
            continue

        has_conflict = False
        for apt in appointments_today:
            if apt.start_time < slot_end and apt.end_time > slot_start:
                has_conflict = True
                break

        if has_conflict:
            continue

        gap_before = _gap_before(slot_start, appointments_today)
        if gap_before < best_gap:
            best_gap = gap_before
            best_slot = (slot_start, slot_end)

    return best_slot


def _gap_before(slot_start: time, appointments: List) -> int:
    """
    Calcula el hueco en minutos entre la última cita que termina
    antes del slot propuesto y el inicio del slot.

    Útil para optimizar la agenda: preferimos slots que dejen
    menos tiempo muerto entre citas.
    """
    last_end = time(8, 0)
    for apt in appointments:
        if apt.end_time <= slot_start:
            last_end = apt.end_time
    gap = (
        (slot_start.hour * 60 + slot_start.minute) -
        (last_end.hour * 60 + last_end.minute)
    )
    return gap


def organize_appointments_by_date(
    specialist_id: UUID,
    target_date: date
) -> List[Dict]:
    """
    Organiza las citas de un día en orden cronológico
    y retorna una estructura lista para visualización en timeline.
    """
    appointments = Appointment.objects.filter(
        specialist_id=specialist_id,
        date=target_date,
    ).select_related('client', 'service').order_by('start_time')

    timeline = []
    for apt in appointments:
        timeline.append({
            'id': str(apt.id),
            'client': str(apt.client),
            'service': str(apt.service),
            'start': apt.start_time.strftime('%H:%M'),
            'end': apt.end_time.strftime('%H:%M'),
            'status': apt.status,
            'status_display': apt.get_status_display(),
        })

    return timeline


def get_appointment_conflicts(
    specialist_id: UUID,
    target_date: date
) -> List[Dict]:
    """
    Detecta conflictos de horario (citas que se solapan).
    Útil para auditoría y corrección manual de la agenda.
    """
    active_statuses = [
        AppointmentStatus.PENDING,
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.IN_PROGRESS,
    ]

    appointments = Appointment.objects.filter(
        specialist_id=specialist_id,
        date=target_date,
        status__in=active_statuses,
    ).order_by('start_time')

    conflicts = []
    for i, current in enumerate(appointments):
        for next_apt in appointments[i + 1:]:
            if current.end_time > next_apt.start_time:
                conflicts.append({
                    'first': current,
                    'second': next_apt,
                    'overlap_minutes': (
                        (current.end_time.hour * 60 + current.end_time.minute) -
                        (next_apt.start_time.hour * 60 + next_apt.start_time.minute)
                    ),
                })

    return conflicts
