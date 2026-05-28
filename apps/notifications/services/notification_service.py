"""
Servicio principal de notificaciones (orquestador).
Coordina la creación, envío y reintento de notificaciones.
"""
import logging
from typing import Optional
from django.utils import timezone
from django.db import transaction
from apps.core.models import NotificationType, NotificationStatus
from apps.appointments.models import Appointment
from apps.notifications.models import NotificationLog
from .provider_factory import ProviderFactory
from .message_templates import (
    reminder_message,
    confirmation_message,
    cancellation_message,
    follow_up_message,
    reschedule_message,
)

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Orquestador del sistema de notificaciones.

    Responsabilidades:
    1. Crear NotificationLog con el mensaje ya renderizado
    2. Enviar usando el provider configurado
    3. Manejar reintentos
    4. Reportar resultados
    """

    def __init__(self):
        self._provider = None

    @property
    def provider(self):
        if self._provider is None:
            self._provider = ProviderFactory.get_provider()
        return self._provider

    # ── CREACIÓN ──────────────────────────────────────────────────────

    def create_notification(
        self,
        appointment: Appointment,
        notification_type: str,
        scheduled_at=None,
        custom_message: str = '',
    ) -> NotificationLog:
        """
        Crea un registro de notificación con el mensaje renderizado.

        El mensaje se genera automáticamente según el tipo de notificación
        y los datos de la cita.

        Args:
            appointment: Cita asociada
            notification_type: Tipo (reminder, confirmation, etc.)
            scheduled_at: Cuándo enviarlo (None = ahora)
            custom_message: Mensaje personalizado (opcional)

        Returns:
            NotificationLog creado
        """
        phone = appointment.client.phone
        client_name = appointment.client.get_full_name()
        service_name = appointment.service.name
        date_str = appointment.date.strftime('%d/%m/%Y')
        time_str = appointment.start_time.strftime('%H:%M')

        if custom_message:
            message = custom_message
        else:
            message = self._render_message(
                notification_type=notification_type,
                client_name=client_name,
                service_name=service_name,
                date=date_str,
                time=time_str,
                specialist_name=appointment.specialist.get_full_name(),
                price=str(int(appointment.service.price)),
            )

        if scheduled_at is None:
            scheduled_at = timezone.now()

        return NotificationLog.objects.create(
            appointment=appointment,
            notification_type=notification_type,
            recipient_phone=phone,
            message=message,
            scheduled_at=scheduled_at,
            status=NotificationStatus.PENDING,
        )

    # ── ENVÍO ─────────────────────────────────────────────────────────

    def send_notification(self, notification: NotificationLog) -> bool:
        """
        Envía UNA notificación usando el proveedor configurado.

        Args:
            notification: NotificationLog a enviar

        Returns:
            True si se envió exitosamente, False si falló
        """
        if notification.status == NotificationStatus.SENT:
            logger.warning(f'Notif {notification.pk} ya fue enviada.')
            return True

        result = self.provider.send_message(
            to=notification.recipient_phone,
            message=notification.message,
        )

        if result.get('success'):
            notification.mark_as_sent(
                whatsapp_id=result.get('provider_message_id', ''),
                provider=self.provider.get_provider_name(),
            )
            logger.info(
                f'✅ Notif {notification.pk} enviada a '
                f'{notification.recipient_phone}'
            )
            return True
        else:
            notification.mark_as_failed(error=result.get('error', ''))
            logger.error(
                f'❌ Notif {notification.pk} falló: '
                f'{result.get("error", "")}'
            )

            if notification.can_retry():
                logger.info(
                    f'↻ Notif {notification.pk} se reintentará '
                    f'(intento {notification.attempt_count}/'
                    f'{notification.max_attempts})'
                )
            return False

    # ── PROCESAMIENTO ─────────────────────────────────────────────────

    def process_pending(self, max_notifications: int = 50) -> dict:
        """
        Procesa todas las notificaciones pendientes cuyo
        scheduled_at ya haya pasado.

        Este método es llamado por el management command
        (cada 5-15 minutos via cron).

        Args:
            max_notifications: Máximo a procesar en este ciclo

        Returns:
            dict con resumen: sent, failed, skipped
        """
        now = timezone.now()

        pending = NotificationLog.objects.filter(
            status=NotificationStatus.PENDING,
            scheduled_at__lte=now,
        )[:max_notifications]

        if not pending:
            return {'sent': 0, 'failed': 0, 'skipped': 0}

        results = {'sent': 0, 'failed': 0, 'skipped': 0}

        for notification in pending:
            success = self.send_notification(notification)
            if success:
                results['sent'] += 1
            else:
                if notification.can_retry():
                    results['skipped'] += 1
                else:
                    results['failed'] += 1

        logger.info(
            f'Ciclo completado: {results["sent"]} enviadas, '
            f'{results["failed"]} fallidas, '
            f'{results["skipped"]} pendientes de reintento'
        )
        return results

    def retry_failed(self, max_retries: int = 20) -> dict:
        """
        Reintenta notificaciones fallidas que aún tengan
        intentos disponibles.

        Args:
            max_retries: Máximo a reintentar en este ciclo

        Returns:
            dict con resumen
        """
        failed = NotificationLog.objects.filter(
            status=NotificationStatus.FAILED,
            attempt_count__lt=models.F('max_attempts'),
        )[:max_retries]

        results = {'sent': 0, 'still_failed': 0}

        for notification in failed:
            success = self.send_notification(notification)
            if success:
                results['sent'] += 1
            else:
                results['still_failed'] += 1

        return results

    # ── MENSAJES ──────────────────────────────────────────────────────

    def _render_message(
        self,
        notification_type: str,
        client_name: str,
        service_name: str,
        date: str,
        time: str,
        specialist_name: str = '',
        price: str = '',
    ) -> str:
        """Selecciona y renderiza la plantilla adecuada."""
        templates = {
            NotificationType.REMINDER: reminder_message,
            NotificationType.CONFIRMATION: confirmation_message,
            NotificationType.CANCELLATION: cancellation_message,
            NotificationType.FOLLOW_UP: follow_up_message,
        }

        template_fn = templates.get(notification_type)
        if not template_fn:
            logger.warning(f'Plantilla no encontrada para: {notification_type}')
            return f'Notificación de {notification_type} para {client_name}.'

        if notification_type == NotificationType.REMINDER:
            return template_fn(client_name, service_name, date, time, specialist_name)
        elif notification_type == NotificationType.CONFIRMATION:
            return template_fn(client_name, service_name, date, time, price)
        elif notification_type == NotificationType.CANCELLATION:
            return template_fn(client_name, service_name, date)
        elif notification_type == NotificationType.FOLLOW_UP:
            return template_fn(client_name, service_name, date)

        return template_fn(client_name, service_name, date, time)
