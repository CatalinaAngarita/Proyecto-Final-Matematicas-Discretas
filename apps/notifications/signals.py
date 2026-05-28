"""
Señales para crear notificaciones automáticas cuando cambia
el estado de una cita.

CADENA DE EVENTOS:
┌──────────────────────┐     ┌──────────────────────┐
│ Cita CREADA         │────→│ notification:        │
│ (status=pending)    │     │ confirmation (manual) │
└──────────────────────┘     └──────────────────────┘

┌──────────────────────┐     ┌──────────────────────┐
│ Cita CONFIRMADA      │────→│ scheduler:           │
│ (status=confirmed)   │     │ recordatorio -24h    │
│                      │     │ recordatorio -2h     │
└──────────────────────┘     └──────────────────────┘

┌──────────────────────┐     ┌──────────────────────┐
│ Cita CANCELADA       │────→│ notification:        │
│ (status=cancelled)   │     │ cancelación          │
└──────────────────────┘     └──────────────────────┘

┌──────────────────────┐     ┌──────────────────────┐
│ Cita COMPLETADA      │────→│ notification:        │
│ (status=completed)   │     │ seguimiento (+1 día) │
└──────────────────────┘     └──────────────────────┘
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from apps.appointments.models import Appointment
from apps.core.models import AppointmentStatus
from .services.scheduler import NotificationScheduler

logger = logging.getLogger(__name__)
scheduler = NotificationScheduler()


@receiver(post_save, sender=Appointment)
def handle_appointment_status_change(sender, instance, created, **kwargs):
    """
    Se ejecuta después de cada guardado de Appointment.
    Detecta cambios de estado y acciona las notificaciones correspondientes.
    """
    if created and instance.status == AppointmentStatus.PENDING:
        logger.info(f'Cita {instance.pk} creada (pendiente). Sin acción automática.')
        return

    if instance.status == AppointmentStatus.CONFIRMED:
        logger.info(f'Cita {instance.pk} confirmada. Programando recordatorios...')
        scheduler.schedule_reminders(instance)
        scheduler.schedule_confirmation(instance)
        return

    if instance.status == AppointmentStatus.CANCELLED:
        logger.info(f'Cita {instance.pk} cancelada. Enviando notificación...')
        scheduler.schedule_cancellation(instance)
        return

    if instance.status == AppointmentStatus.COMPLETED:
        logger.info(f'Cita {instance.pk} completada. Programando seguimiento...')
        scheduler.schedule_follow_up(instance)
        return
