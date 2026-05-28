from datetime import date, time, datetime, timedelta
from typing import List, Tuple
from uuid import UUID
from apps.schedules.models import WorkSchedule, BreakSchedule, DayOff


def get_available_slots(
    specialist_id: UUID,
    target_date: date,
    service_duration: int = 60
) -> List[Tuple[time, time]]:
    """
    Retorna los slots disponibles para un especialista en una fecha dada,
    considerando horario laboral, descansos y días libres.
    """
    if DayOff.objects.filter(
        specialist_id=specialist_id, date=target_date
    ).exists():
        return []

    day_of_week = target_date.weekday()

    try:
        schedule = WorkSchedule.objects.get(
            specialist_id=specialist_id,
            day_of_week=day_of_week,
            is_active=True
        )
    except WorkSchedule.DoesNotExist:
        return []

    blocks = [
        (schedule.morning_start, schedule.morning_end),
        (schedule.afternoon_start, schedule.afternoon_end),
    ]

    breaks = BreakSchedule.objects.filter(
        specialist_id=specialist_id,
        date=target_date,
    )

    slots = []
    for block_start, block_end in blocks:
        current = datetime.combine(target_date, block_start)
        end = datetime.combine(target_date, block_end)

        while current + timedelta(minutes=service_duration) <= end:
            slot_start = current.time()
            slot_end = (current + timedelta(minutes=service_duration)).time()

            if not _is_in_break(slot_start, slot_end, breaks):
                slots.append((slot_start, slot_end))

            current += timedelta(minutes=30)

    return slots


def _is_in_break(start: time, end: time, breaks) -> bool:
    for b in breaks:
        if start < b.end_time and end > b.start_time:
            return True
    return False
