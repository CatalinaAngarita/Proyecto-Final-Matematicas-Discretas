import uuid
from django.db import models
from django.utils import timezone


# ==============================================================================
# ABSTRACT BASE MODELS
# ==============================================================================

class UUIDModel(models.Model):
    """Modelo abstracto que usa UUID como primary key en lugar de auto-increment."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que añade marcas de tiempo a cualquier modelo.
    - created_at: se fija una sola vez al crear el registro (auto_now_add)
    - updated_at: se actualiza cada vez que se guarda (auto_now)
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Modelo abstracto para soft delete (borrado lógico).
    En lugar de eliminar registros de la BD (DELETE),
    marcamos is_active=False y registramos cuándo se desactivó.
    Beneficios:
    - Nunca se pierde el historial de citas, clientas, etc.
    - Se puede restaurar un registro
    - Las consultas por defecto excluyen registros inactivos
    """
    is_active = models.BooleanField(
        'Activo',
        default=True,
        help_text='Desmarcar para ocultar este registro sin eliminarlo'
    )
    deleted_at = models.DateTimeField(
        'Fecha de desactivación',
        null=True,
        blank=True,
        editable=False
    )

    class Meta:
        abstract = True

    def soft_delete(self):
        """Marca el registro como inactivo sin borrarlo de la BD."""
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_active', 'deleted_at', 'updated_at'])

    def restore(self):
        """Restaura un registro que fue desactivado."""
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=['is_active', 'deleted_at', 'updated_at'])


class BaseModel(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """
    Modelo base COMPLETO que combina:
    - UUID como PK
    - created_at / updated_at
    - is_active / deleted_at (soft delete)

    Casi todas las entidades del sistema heredarán de este.
    """

    class Meta:
        abstract = True

    def clean(self):
        """Hook para validaciones — sobreescribir en cada subclase."""
        pass

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# ==============================================================================
# CUSTOM MANAGERS
# ==============================================================================

class ActiveManager(models.Manager):
    """
    Manager por defecto para SoftDeleteModel.
    Retorna SOLO registros activos (is_active=True).
    Para ver todos (incluyendo inactivos): Model.all_objects.all()
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AllObjectsManager(models.Manager):
    """Manager que retorna TODOS los registros, activos e inactivos."""
    def get_queryset(self):
        return super().get_queryset()


# ==============================================================================
# CHOICES / ENUMS
# ==============================================================================

class BusinessDayChoices(models.IntegerChoices):
    """
    Días laborales del spa.
    Lunes a Sábado (domingo no laboral).
    """
    MONDAY = 0, 'Lunes'
    TUESDAY = 1, 'Martes'
    WEDNESDAY = 2, 'Miércoles'
    THURSDAY = 3, 'Jueves'
    FRIDAY = 4, 'Viernes'
    SATURDAY = 5, 'Sábado'


class AppointmentStatus(models.TextChoices):
    """
    Ciclo de vida de una cita:
    pending → confirmed → in_progress → completed
         ↘ cancelled
         ↘ no_show
    """
    PENDING = 'pending', 'Pendiente'
    CONFIRMED = 'confirmed', 'Confirmada'
    IN_PROGRESS = 'in_progress', 'En curso'
    COMPLETED = 'completed', 'Completada'
    CANCELLED = 'cancelled', 'Cancelada'
    NO_SHOW = 'no_show', 'No asistió'


class NotificationType(models.TextChoices):
    """Tipos de notificaciones que envía el sistema."""
    REMINDER = 'reminder', 'Recordatorio'
    CONFIRMATION = 'confirmation', 'Confirmación'
    CANCELLATION = 'cancellation', 'Cancelación'
    FOLLOW_UP = 'follow_up', 'Seguimiento'


class NotificationStatus(models.TextChoices):
    """Estado del envío de una notificación."""
    PENDING = 'pending', 'Pendiente'
    SENT = 'sent', 'Enviado'
    FAILED = 'failed', 'Fallido'


class ServiceMainCategory(models.TextChoices):
    """Categoría principal de un servicio."""
    NAIL = 'nail', 'Uñas'
    EYEBROW = 'eyebrow', 'Cejas'
    LASH = 'lash', 'Pestañas'
    WAXING = 'waxing', 'Depilación'
    OTHER = 'other', 'Otros'


class Testimonial(UUIDModel, TimeStampedModel):
    """Opinión de una clienta sobre el servicio recibido."""
    client_name = models.CharField('Nombre de la clienta', max_length=200)
    content = models.TextField('Opinión')
    rating = models.PositiveSmallIntegerField(
        'Calificación',
        default=5,
        help_text='De 1 a 5 estrellas'
    )
    is_active = models.BooleanField('Visible', default=True)
    order = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.client_name} — {"★" * self.rating}{"☆" * (5 - self.rating)}'
