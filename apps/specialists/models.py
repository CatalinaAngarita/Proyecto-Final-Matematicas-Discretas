from django.db import models
from django.contrib.auth.models import User
from apps.core.models import BaseModel
from apps.services.models import Service


class Specialist(BaseModel):
    """
    ========================================================================
    ESPECIALISTA
    ========================================================================
    Persona que realiza los servicios. Actualmente solo Diana,
    pero el sistema está preparado para múltiples especialistas.

    Decisiones de diseño:
    - user (OneToOneField, nullable): cada especialista PUEDE tener
      credenciales de acceso al sistema. Nullable porque inicialmente
      solo el admin (Diana dueña) gestiona todo.
    - is_primary (BooleanField): marca a Diana como principal.
      Útil para filtros y dashboard (solo una puede ser primary).
    - services (ManyToManyField): qué servicios sabe hacer cada uno.
      No todos los especialistas harán todos los servicios.

    Relaciones:
    - OneToOne con User: un especialista PUEDE tener 0 o 1 usuario del sistema
    - ManyToMany con Service: un especialista hace MUCHOS servicios,
      un servicio puede ser hecho por MUCHOS especialistas
    - OneToMany con WorkSchedule: un especialista tiene MUCHOS horarios
    - OneToMany con Appointment: un especialista tiene MUCHAS citas
    """
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario asociado',
        help_text='Opcional: credenciales de acceso para el especialista'
    )
    first_name = models.CharField('Nombres', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    email = models.EmailField('Correo electrónico', blank=True)

    is_primary = models.BooleanField(
        'Especialista principal',
        default=False,
        help_text='Solo una especialista puede ser la principal (Diana)'
    )

    services = models.ManyToManyField(
        Service,
        blank=True,
        verbose_name='Servicios que realiza',
        help_text='Seleccionar los servicios que este especialista puede realizar'
    )

    photo = models.ImageField(
        'Foto',
        upload_to='specialists/',
        blank=True,
        help_text='Foto profesional del especialista'
    )
    notes = models.TextField('Notas internas', blank=True)

    class Meta:
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'
        ordering = ['-is_primary', 'first_name']
        indexes = [
            models.Index(
                fields=['is_primary', 'is_active'],
                name='idx_specialist_primary_active'
            ),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """Garantiza que solo una especialista sea la principal."""
        if self.is_primary:
            Specialist.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )
        super().save(*args, **kwargs)
