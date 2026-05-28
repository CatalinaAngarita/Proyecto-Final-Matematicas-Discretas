"""
Programador de notificaciones.
Calcula cuándo deben enviarse los recordatorios y crea
los NotificationLog correspondientes con scheduled_at.
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import logging
from apps.appointments.models import Appointment
from apps.core.models import AppointmentStatus, NotificationType
from .notification_service import NotificationService

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """
    Lógica para programar recordatorios automáticos.

    FLUJO:
    1. Una cita se confirma (status → confirmed)
    2. scheduler.schedule_reminders(appointment) se ejecuta
    3. Crea NotificationLog con scheduled_at = fecha_cita - 24h
    4. Crea NotificationLog con scheduled_at = fecha_cita - 2h
    5. El comando process_notifications los envía cuando scheduled_at ≤ now
    """

    def __init__(self):
        self.service = NotificationService()

    def schedule_reminders(self, appointment: Appointment):
        """
        Programa los recordatorios automáticos para una cita.

        Crea dos notificaciones:
        - Recordatorio 1: 24 horas antes
        - Recordatorio 2: 2 horas antes

        Args:
            appointment: Instancia de Appointment confirmada
        """
        if appointment.status != AppointmentStatus.CONFIRMED:
            logger.warning(
                f'Cita {appointment.pk} no está confirmada. '
                f'Estado actual: {appointment.status}'
            )
            return

        self._schedule_single_reminder(
            appointment=appointment,
            hours_before=24,
            label='recordatorio-24h',
        )
        self._schedule_single_reminder(
            appointment=appointment,
            hours_before=2,
            label='recordatorio-2h',
        )

        logger.info(
            f'Recordatorios programados para cita {appointment.pk}: '
            f'-24h y -2h'
        )

    def schedule_follow_up(self, appointment: Appointment):
        """
        Programa un mensaje de seguimiento para el día siguiente
        a una cita completada.
        """
        follow_up_date = appointment.date + timedelta(days=1)
        scheduled = timezone.make_aware(
            datetime.combine(follow_up_date, datetime.min.time())
        )

        self.service.create_notification(
            appointment=appointment,
            notification_type=NotificationType.FOLLOW_UP,
            scheduled_at=scheduled,
        )
        logger.info(f'Seguimiento programado para cita {appointment.pk}')

    def schedule_confirmation(self, appointment: Appointment):
        """
        Envía confirmación inmediatamente después de agendar.
        scheduled_at = now (se envía en el próximo ciclo).
        """
        self.service.create_notification(
            appointment=appointment,
            notification_type=NotificationType.CONFIRMATION,
            scheduled_at=timezone.now(),
        )
        logger.info(f'Confirmación programada para cita {appointment.pk}')

    def schedule_cancellation(self, appointment: Appointment):
        """
        Envía notificación de cancelación inmediatamente.
        """
        self.service.create_notification(
            appointment=appointment,
            notification_type=NotificationType.CANCELLATION,
            scheduled_at=timezone.now(),
        )
        logger.info(f'Notificación de cancelación para cita {appointment.pk}')

    def _schedule_single_reminder(
        self,
        appointment: Appointment,
        hours_before: int,
        label: str,
    ):
        """
        Crea un NotificationLog programado para X horas antes de la cita.

        Args:
            appointment: La cita
            hours_before: Cuántas horas antes enviar el recordatorio
            label: Identificador interno para logging
        """
        appointment_dt = timezone.make_aware(
            datetime.combine(appointment.date, appointment.start_time)
        )
        scheduled_at = appointment_dt - timedelta(hours=hours_before)

        now = timezone.now()

        if scheduled_at <= now:
            scheduled_at = now

        self.service.create_notification(
            appointment=appointment,
            notification_type=NotificationType.REMINDER,
            scheduled_at=scheduled_at,
        )
