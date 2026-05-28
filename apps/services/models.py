from django.db import models
from apps.core.models import BaseModel, ServiceMainCategory


class ServiceCategory(BaseModel):
    """
    ========================================================================
    CATEGORÍA PERSONALIZADA DE SERVICIO
    ========================================================================
    Categorías que el administrador puede crear libremente.
    Es independiente de ServiceMainCategory (que es fija: uñas/cejas/depilación).

    Ejemplos: 'Uñas Acrílicas', 'Cejas con Henna', 'Depilación Facial'

    Relaciones:
    - Una categoría tiene MUCHOS servicios (ForeignKey en Service)
    """
    name = models.CharField('Nombre', max_length=100, unique=True)
    description = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Categoría de servicio'
        verbose_name_plural = 'Categorías de servicios'
        ordering = ['name']

    def __str__(self):
        return self.name


class NailApplicationType(BaseModel):
    """
    ========================================================================
    TIPO DE APLICACIÓN DE UÑAS
    ========================================================================
    Catálogo de técnicas de aplicación de uñas que ofrece el spa.
    (~7 tipos: Acrílicas, Gel, Semipermanente, Polygel, Press-on, etc.)

    Independiente de Service para poder asociarlo a múltiples servicios.
    No todos los servicios de uñas aplican todos los tipos.

    Relaciones:
    - Un tipo se asocia a MUCHAS citas (ForeignKey nullable en Appointment)
    """
    name = models.CharField('Nombre del tipo', max_length=100, unique=True)
    description = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Tipo de aplicación de uñas'
        verbose_name_plural = 'Tipos de aplicación de uñas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(BaseModel):
    """
    ========================================================================
    SERVICIO
    ========================================================================
    Cada servicio que el spa ofrece. Ejemplos:
    - 'Manicura básica' (45 min, $35,000)
    - 'Uñas acrílicas completo' (120 min, $120,000)
    - 'Diseño de cejas' (30 min, $25,000)

    Decisiones de diseño:
    - category (ServiceMainCategory): clasificación fija (uñas, cejas, depilación)
    - service_category (ServiceCategory FK): clasificación flexible que crea el admin
    - Tener ambas permite filtros rápidos y agrupaciones personalizadas
    - price como DecimalField (no FloatField) para precisión monetaria

    Relaciones:
    - Un servicio pertenece a UNA categoría principal (TextChoices)
    - Un servicio puede tener UNA categoría personalizada (FK nullable)
    - Un servicio es realizado por MUCHOS especialistas (M2M en Specialist)
    - Un servicio aparece en MUCHAS citas (FK en Appointment)
    """
    name = models.CharField('Nombre del servicio', max_length=200)
    description = models.TextField('Descripción', blank=True)

    category = models.CharField(
        'Categoría principal',
        max_length=20,
        choices=ServiceMainCategory.choices,
        default=ServiceMainCategory.NAIL,
        db_index=True,
        help_text='Clasificación fija: uñas, cejas, depilación u otros'
    )
    service_category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Categoría personalizada',
        help_text='Categoría creada por el administrador (opcional)'
    )

    duration_minutes = models.PositiveIntegerField(
        'Duración (minutos)',
        help_text='Tiempo estimado del servicio'
    )
    price = models.DecimalField(
        'Precio',
        max_digits=10,
        decimal_places=2,
        help_text='Precio en pesos colombianos (COP)'
    )

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['category', 'name']
        indexes = [
            models.Index(
                fields=['category', 'is_active'],
                name='idx_service_category_active'
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.duration_minutes is not None and self.duration_minutes < 5:
            raise ValidationError('La duración mínima es de 5 minutos.')
        if self.price is not None and self.price < 0:
            raise ValidationError('El precio no puede ser negativo.')
