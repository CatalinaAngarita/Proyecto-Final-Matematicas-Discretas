from django.db import models
from django.utils import timezone
from apps.core.models import UUIDModel, TimeStampedModel, NotificationType, NotificationStatus
from apps.appointments.models import Appointment


class NotificationLog(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    REGISTRO DE NOTIFICACIÓN
    ========================================================================
    Cada fila representa UN intento de envío de notificación.

    CAMPOS CLAVE:
    - scheduled_at: momento EN QUE debe enviarse (útil para programar)
    - attempt_count: cuántos intentos de envío se han hecho (máx 3)
    - provider: qué proveedor se usó (meta, twilio)
    - channel: qué canal (whatsapp, sms)

    CICLO DE VIDA:
    ┌──────────┐
    │ PENDING  │──→ SENT (mark_as_sent)
    │          │──→ FAILED (mark_as_failed)
    └──────────┘
         │ reintento si attempt_count < 3
         └──→ PENDING again (reset)
    """
    PROVIDER_META = 'meta'
    PROVIDER_TWILIO = 'twilio'
    PROVIDER_CHOICES = [
        (PROVIDER_META, 'Meta Cloud API'),
        (PROVIDER_TWILIO, 'Twilio'),
    ]

    CHANNEL_WHATSAPP = 'whatsapp'
    CHANNEL_SMS = 'sms'
    CHANNEL_CHOICES = [
        (CHANNEL_WHATSAPP, 'WhatsApp'),
        (CHANNEL_SMS, 'SMS'),
    ]

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        verbose_name='Cita',
        related_name='notifications',
        help_text='Cita asociada a esta notificación'
    )
    notification_type = models.CharField(
        'Tipo de notificación',
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.REMINDER,
        db_index=True,
        help_text='Recordatorio, confirmación, cancelación o seguimiento'
    )
    recipient_phone = models.CharField(
        'Teléfono destino',
        max_length=20,
        help_text='Número al que se envió el mensaje (formato internacional)'
    )
    message = models.TextField(
        'Mensaje enviado',
        help_text='Contenido exacto del mensaje en el momento del envío'
    )

    # --- Estado ---
    status = models.CharField(
        'Estado del envío',
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        db_index=True
    )

    # --- Programación ---
    scheduled_at = models.DateTimeField(
        'Programado para',
        null=True,
        blank=True,
        db_index=True,
        help_text='Momento en que debe enviarse la notificación'
    )
    sent_at = models.DateTimeField('Enviado el', null=True, blank=True)

    # --- Proveedor y canal ---
    provider = models.CharField(
        'Proveedor',
        max_length=20,
        choices=PROVIDER_CHOICES,
        default=PROVIDER_META,
        blank=True,
        help_text='Qué proveedor se usó para el envío'
    )
    channel = models.CharField(
        'Canal',
        max_length=20,
        choices=CHANNEL_CHOICES,
        default=CHANNEL_WHATSAPP,
        help_text='Canal usado: WhatsApp o SMS'
    )

    # --- Control de reintentos ---
    attempt_count = models.PositiveSmallIntegerField(
        'Intentos realizados',
        default=0,
        help_text='Número de veces que se ha intentado enviar (máx 3)'
    )
    max_attempts = models.PositiveSmallIntegerField(
        'Máximo de intentos',
        default=3,
        editable=False
    )
    error_message = models.TextField(
        'Mensaje de error',
        blank=True,
        help_text='Descripción del error si el envío falló'
    )
    whatsapp_message_id = models.CharField(
        'ID del mensaje en WhatsApp',
        max_length=100,
        blank=True,
        help_text='ID devuelto por la API de WhatsApp para tracking'
    )

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=['appointment', 'notification_type'],
                name='idx_notif_appointment_type'
            ),
            models.Index(
                fields=['status', 'scheduled_at'],
                name='idx_notif_status_scheduled'
            ),
        ]

    def __str__(self):
        return f'{self.get_notification_type_display()} — Cita #{str(self.appointment.pk)[:8]}'

    def can_retry(self) -> bool:
        """Verifica si aún se puede reintentar el envío."""
        return (
            self.status == NotificationStatus.FAILED
            and self.attempt_count < self.max_attempts
        )

    def mark_as_sent(self, whatsapp_id='', provider=''):
        """Marca la notificación como enviada exitosamente."""
        self.status = NotificationStatus.SENT
        self.sent_at = timezone.now()
        self.attempt_count = models.F('attempt_count') + 1
        if whatsapp_id:
            self.whatsapp_message_id = whatsapp_id
        if provider:
            self.provider = provider
        self.save(update_fields=[
            'status', 'sent_at', 'attempt_count',
            'whatsapp_message_id', 'provider', 'updated_at'
        ])
        self.refresh_from_db()

    def mark_as_failed(self, error=''):
        """Marca la notificación como fallida y registra el error."""
        self.status = NotificationStatus.FAILED
        self.error_message = error
        self.attempt_count = models.F('attempt_count') + 1
        self.save(update_fields=[
            'status', 'error_message', 'attempt_count', 'updated_at'
        ])
        self.refresh_from_db()

    def reset_to_pending(self):
        """Reintenta: vuelve a estado pendiente para reprocesar."""
        self.status = NotificationStatus.PENDING
        self.error_message = ''
        self.save(update_fields=['status', 'error_message', 'updated_at'])
