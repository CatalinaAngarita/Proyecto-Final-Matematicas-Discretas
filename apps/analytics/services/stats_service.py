from datetime import date, timedelta
from django.db.models import Count, Sum, Q
from apps.appointments.models import Appointment
from apps.core.utils.constants import (
    APPOINTMENT_COMPLETED, APPOINTMENT_CANCELLED, APPOINTMENT_NO_SHOW
)


def get_daily_stats(target_date: date = None) -> dict:
    """Estadísticas del día."""
    if target_date is None:
        target_date = date.today()

    qs = Appointment.objects.filter(date=target_date)
    total = qs.count()
    completed = qs.filter(status=APPOINTMENT_COMPLETED).count()
    cancelled = qs.filter(status=APPOINTMENT_CANCELLED).count()
    no_show = qs.filter(status=APPOINTMENT_NO_SHOW).count()

    return {
        'date': target_date,
        'total': total,
        'completed': completed,
        'cancelled': cancelled,
        'no_show': no_show,
        'completion_rate': round((completed / total * 100), 1) if total else 0,
        'cancellation_rate': round((cancelled / total * 100), 1) if total else 0,
    }


def get_weekly_stats() -> list:
    """Estadísticas de los últimos 7 días."""
    today = date.today()
    week_ago = today - timedelta(days=7)
    return [
        get_daily_stats(today - timedelta(days=i))
        for i in range(7)
    ]


def get_most_requested_services(limit: int = 10) -> list:
    """Servicios más solicitados."""
    return (
        Appointment.objects
        .values('service__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:limit]
    )


def get_client_retention_rate() -> dict:
    """Tasa de retención de clientas."""
    total_clients = (
        Appointment.objects
        .values('client')
        .distinct()
        .count()
    )
    returning_clients = (
        Appointment.objects
        .values('client')
        .annotate(visit_count=Count('id'))
        .filter(visit_count__gte=2)
        .count()
    )

    return {
        'total_clients': total_clients,
        'returning_clients': returning_clients,
        'retention_rate': round(
            (returning_clients / total_clients * 100), 1
        ) if total_clients else 0,
    }
