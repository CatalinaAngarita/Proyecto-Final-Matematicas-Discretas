from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.models import BaseModel, UUIDModel, TimeStampedModel, AppointmentStatus
from apps.clients.models import Client
from apps.specialists.models import Specialist
from apps.services.models import Service, NailApplicationType


class Appointment(BaseModel):
    """
    ========================================================================
    CITA (APPOINTMENT)
    ========================================================================
    Entidad central del sistema. Representa una cita agendada.

    CICLO DE VIDA DEL ESTADO:
    ┌──────────┐
    │ PENDING  │ → Cita creada, esperando confirmación
    └────┬─────┘
         │
    ┌────▼──────┐
    │ CONFIRMED │ → Cliente confirmó asistencia
    └────┬──────┘
         │
    ┌────▼─────────┐
    │ IN_PROGRESS  │ → El servicio está siendo realizado
    └────┬─────────┘
         │
    ┌────▼─────────┐     ┌───────────┐     ┌──────────┐
    │  COMPLETED   │  o  │ CANCELLED │  o  │ NO_SHOW  │
    └──────────────┘     └───────────┘     └──────────┘

    Decisiones de diseño:
    - NailApplicationType FK nullable: solo aplica a servicios de uñas
    - rescheduled_from (self FK nullable): cuando se reagenda,
      la cita original apunta a la nueva. Esto permite trazabilidad.
    - confirmed_at / completed_at: timestamps de hitos clave
    - cancelled_at + cancellation_reason: análisis de cancelaciones
    - is_cancelled_by_client: estadística de cancelaciones por clienta

    ÍNDICES (explicados abajo en Meta.indexes):
    - idx_appointment_date_status: consulta diaria de citas por estado
    - idx_appointment_client_date: historial de una clienta
    - idx_appointment_specialist_date: agenda de un especialista

    RELACIONES:
    ┌──────────┐     ┌─────────────┐
    │  Client  │1──N│ Appointment │
    └──────────┘     └──────┬──────┘
                            │
    ┌──────────────┐        │
    │  Specialist  │1──────N│
    └──────────────┘        │
                            │
    ┌──────────┐            │
    │  Service │1──────────N│
    └──────────┘            │
                            │
    ┌──────────────────┐    │
    │ NailApplication  │1───N│ (nullable)
    └──────────────────┘    │
    """
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Clienta',
        related_name='appointments',
        help_text='Clienta que recibe el servicio'
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Especialista',
        related_name='appointments',
        help_text='Especialista que realiza el servicio'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Servicio',
        related_name='appointments',
        help_text='Servicio contratado'
    )
    nail_application_type = models.ForeignKey(
        NailApplicationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Tipo de aplicación de uñas',
        help_text='Obligatorio si el servicio es de uñas'
    )

    # --- Tiempo de la cita ---
    date = models.DateField('Fecha de la cita', db_index=True)
    start_time = models.TimeField('Hora de inicio')
    end_time = models.TimeField('Hora de fin')

    # --- Estado ---
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
        db_index=True,
        help_text='Estado actual en el ciclo de vida de la cita'
    )

    notes = models.TextField(
        'Notas de la cita',
        blank=True,
        help_text='Instrucciones especiales, preferencias, etc.'
    )

    # --- Cancelación ---
    is_cancelled_by_client = models.BooleanField(
        'Cancelada por la clienta',
        default=False,
        help_text='Indica si la cancelación fue iniciada por la clienta'
    )
    cancellation_reason = models.TextField(
        'Motivo de cancelación',
        blank=True,
        help_text='Razón por la que se canceló la cita'
    )
    cancelled_at = models.DateTimeField(
        'Fecha de cancelación',
        null=True,
        blank=True
    )

    # --- Hitos de tiempo ---
    confirmed_at = models.DateTimeField(
        'Confirmada el',
        null=True,
        blank=True,
        help_text='Momento en que se confirmó la cita'
    )
    completed_at = models.DateTimeField(
        'Completada el',
        null=True,
        blank=True,
        help_text='Momento en que finalizó el servicio'
    )

    # --- Reagendación (auto-referencia) ---
    rescheduled_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Reagendada desde',
        related_name='rescheduled_to',
        help_text='Cita original que fue reagendada a esta nueva cita'
    )

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-date', 'start_time']
        indexes = [
            models.Index(
                fields=['date', 'status'],
                name='idx_appointment_date_status'
            ),
            models.Index(
                fields=['client', 'date'],
                name='idx_appointment_client_date'
            ),
            models.Index(
                fields=['specialist', 'date', 'status'],
                name='idx_appt_spec_date_status'
            ),
        ]

    def __str__(self):
        return f'{self.client} — {self.service} — {self.date} {self.start_time}'

    def clean(self):
        errors = {}

        if self.start_time >= self.end_time:
            errors['end_time'] = 'La hora de fin debe ser posterior a la hora de inicio.'

        if self.status == AppointmentStatus.CANCELLED and not self.cancelled_at:
            errors['cancelled_at'] = 'Debe registrar la fecha de cancelación.'

        if self.status == AppointmentStatus.CANCELLED and not self.cancellation_reason:
            errors['cancellation_reason'] = 'Debe indicar el motivo de cancelación.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Auto-registrar fechas hito según el estado
        if self.status == AppointmentStatus.CONFIRMED and not self.confirmed_at:
            self.confirmed_at = timezone.now()

        if self.status == AppointmentStatus.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()

        if self.status == AppointmentStatus.CANCELLED and not self.cancelled_at:
            self.cancelled_at = timezone.now()

        self.clean()
        super().save(*args, **kwargs)

    def reschedule(self, new_date, new_start, new_end, reason=''):
        """
        Reagenda esta cita a una nueva fecha/hora.
        Crea una nueva cita y marca la actual como cancelada.
        """
        new_appointment = Appointment.objects.create(
            client=self.client,
            specialist=self.specialist,
            service=self.service,
            nail_application_type=self.nail_application_type,
            date=new_date,
            start_time=new_start,
            end_time=new_end,
            status=AppointmentStatus.PENDING,
            rescheduled_from=self,
            notes=f'Reagendada desde cita {self.pk}. {reason}',
        )

        self.status = AppointmentStatus.CANCELLED
        self.cancelled_at = timezone.now()
        self.cancellation_reason = f'Reagendada a cita {new_appointment.pk}. {reason}'
        self.is_cancelled_by_client = False
        self.save()

        return new_appointment


class AppointmentRescheduleLog(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    LOG DE REAGENDACIÓN
    ========================================================================
    Registro histórico de CADA VEZ que una cita es reagendada.

    ¿Por qué existe este modelo separado?
    - Para auditoría: permite ver el historial completo de cambios
    - Para estadísticas: cuántas reagendaciones ocurren, en qué periodos
    - Para análisis de cancelaciones: las reagendaciones no cuentan como
      cancelaciones reales

    NO hereda SoftDelete: el log es inmutable, nunca se borra.

    Relaciones:
    - Muchos logs pertenecen a UNA Appointment
    """
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        verbose_name='Cita',
        related_name='reschedule_logs'
    )

    # Datos ANTES de la reagendación
    old_date = models.DateField('Fecha anterior')
    old_start_time = models.TimeField('Hora inicio anterior')
    old_end_time = models.TimeField('Hora fin anterior')

    # Datos DESPUÉS de la reagendación
    new_date = models.DateField('Nueva fecha')
    new_start_time = models.TimeField('Nueva hora inicio')
    new_end_time = models.TimeField('Nueva hora fin')

    reason = models.TextField('Motivo', blank=True)

    rescheduled_by = models.CharField(
        'Reagendada por',
        max_length=50,
        choices=[
            ('admin', 'Administrador'),
            ('client', 'Clienta'),
            ('system', 'Sistema'),
        ],
        default='admin'
    )

    class Meta:
        verbose_name = 'Registro de reagendación'
        verbose_name_plural = 'Registros de reagendación'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reagendación #{self.pk} - Cita {self.appointment.pk}'
