from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel


class Client(BaseModel):
    """
    ========================================================================
    CLIENTA
    ========================================================================
    Entidad principal del negocio. Representa a una clienta del spa.

    Decisiones de diseño:
    - UUID como PK: las URLs de detalle no exponen IDs secuenciales
    - phone unique + indexed: la búsqueda por teléfono es la más frecuente
    - total_visits como campo desnormalizado: evita COUNT(*) en cada consulta
    - last_visit_date: útil para campañas de reactivación
    - Hereda soft delete: si una clienta ya no viene, no se pierde su historial

    Relaciones:
    - Una clienta tiene MUCHAS citas (ForeignKey en Appointment)
    - Una clienta tiene MUCHAS notificaciones (a través de Appointment)

    Índices:
    - phone: búsqueda exacta por teléfono (único)
    - email: búsqueda por correo
    - is_active + created_at: listado de clientas activas ordenadas
    - last_visit_date: clientas que no visitan hace tiempo
    """
    first_name = models.CharField('Nombres', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100)

    phone = models.CharField(
        'Teléfono',
        max_length=20,
        unique=True,
        db_index=True,
        help_text='Formato: +57 300 123 4567'
    )
    email = models.EmailField('Correo electrónico', blank=True, db_index=True)

    birth_date = models.DateField(
        'Fecha de nacimiento',
        null=True,
        blank=True,
        help_text='Para enviar saludos de cumpleaños'
    )

    # --- Campos de seguimiento ---
    total_visits = models.PositiveIntegerField(
        'Visitas totales',
        default=0,
        help_text='Se incrementa automáticamente al completar una cita'
    )
    last_visit_date = models.DateField(
        'Última visita',
        null=True,
        blank=True,
        help_text='Fecha de la última cita completada'
    )

    notes = models.TextField(
        'Notas internas',
        blank=True,
        help_text='Preferencias, alergias, observaciones importantes'
    )

    class Meta:
        verbose_name = 'Clienta'
        verbose_name_plural = 'Clientas'
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=['is_active', 'created_at'],
                name='idx_client_active_created'
            ),
            models.Index(
                fields=['last_visit_date'],
                name='idx_client_last_visit'
            ),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def increment_visits(self):
        """Incrementa el contador y actualiza la última visita."""
        self.total_visits = models.F('total_visits') + 1
        self.last_visit_date = models.F('last_visit_date')
        self.save(update_fields=['total_visits', 'last_visit_date', 'updated_at'])
        self.refresh_from_db()
