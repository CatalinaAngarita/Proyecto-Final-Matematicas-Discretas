from django.db import models
from apps.core.models import UUIDModel, TimeStampedModel
from apps.services.models import Service


class DailySummary(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    RESUMEN DIARIO
    ========================================================================
    Snapshot diario del estado del negocio. Se calcula una vez al día
    (mediante un cron job o señal) y se almacena para consultas rápidas.

    ¿Por qué desnormalizar estos datos?
    - Las consultas de "¿cómo fue el día de hoy?" serían instantáneas
    - Las gráficas del dashboard no necesitan JOINs pesados
    - Los históricos mensuales se calculan agregando estos registros

    Decisiones de diseño:
    - unique_together: solo un resumen por día
    - total_revenue como entero (en centavos) para evitar floats
    """
    date = models.DateField('Fecha', unique=True, db_index=True)

    # Volumen de citas
    total_appointments = models.PositiveIntegerField('Total citas', default=0)
    completed_appointments = models.PositiveIntegerField('Completadas', default=0)
    cancelled_appointments = models.PositiveIntegerField('Canceladas', default=0)
    no_show_appointments = models.PositiveIntegerField('No asistieron', default=0)

    # Métricas financieras
    total_revenue = models.DecimalField(
        'Ingresos del día',
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Métricas de clientas
    new_clients = models.PositiveIntegerField('Clientas nuevas', default=0)
    returning_clients = models.PositiveIntegerField('Clientas recurrentes', default=0)

    class Meta:
        verbose_name = 'Resumen diario'
        verbose_name_plural = 'Resúmenes diarios'
        ordering = ['-date']

    def __str__(self):
        return f'Resumen {self.date}'

    @property
    def cancellation_rate(self):
        """Tasa de cancelación del día (porcentaje)."""
        if self.total_appointments == 0:
            return 0.0
        return round(
            (self.cancelled_appointments / self.total_appointments) * 100, 1
        )

    @property
    def completion_rate(self):
        """Tasa de completación del día."""
        if self.total_appointments == 0:
            return 0.0
        return round(
            (self.completed_appointments / self.total_appointments) * 100, 1
        )


class CancellationStat(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    ESTADÍSTICA DE CANCELACIÓN
    ========================================================================
    Métricas detalladas de cancelación agrupadas por fecha.
    Separada de DailySummary para permitir análisis más granular.

    Future use: alimentará los cálculos binomiales y de probabilidad
    para predecir cancelaciones usando SciPy.
    """
    date = models.DateField('Fecha', unique=True, db_index=True)

    total_appointments = models.PositiveIntegerField('Total citas', default=0)
    cancelled_count = models.PositiveIntegerField('Cancelaciones', default=0)
    no_show_count = models.PositiveIntegerField('No asistencias', default=0)
    completed_count = models.PositiveIntegerField('Completadas', default=0)

    cancellation_rate = models.DecimalField(
        'Tasa de cancelación (%)',
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    # Análisis de cancelaciones
    cancelled_by_client = models.PositiveIntegerField(
        'Canceladas por clienta',
        default=0,
        help_text='Cuántas cancelaciones fueron iniciadas por la clienta'
    )
    last_minute_cancellations = models.PositiveIntegerField(
        'Cancelaciones de último minuto',
        default=0,
        help_text='Cancelaciones con menos de 2 horas de anticipación'
    )

    class Meta:
        verbose_name = 'Estadística de cancelación'
        verbose_name_plural = 'Estadísticas de cancelación'
        ordering = ['-date']

    def __str__(self):
        return f'Cancelaciones {self.date}'


class ServiceStat(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    ESTADÍSTICA DE SERVICIO
    ========================================================================
    Rendimiento mensual de cada servicio.
    Útil para identificar los servicios más populares y rentables.

    Decisiones de diseño:
    - service (FK nullable por si se elimina el servicio, no perder stats)
    - month como DateField (primer día del mes) para agrupación
    - unique_together: una estadística por servicio por mes
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Servicio',
        related_name='stats'
    )
    service_name = models.CharField(
        'Nombre del servicio',
        max_length=200,
        help_text='Nombre en el momento de la estadística (congelado)'
    )
    total_bookings = models.PositiveIntegerField('Total reservas', default=0)
    total_revenue = models.DecimalField(
        'Ingresos totales',
        max_digits=14,
        decimal_places=2,
        default=0
    )
    month = models.DateField('Mes', db_index=True)

    class Meta:
        verbose_name = 'Estadística de servicio'
        verbose_name_plural = 'Estadísticas de servicios'
        ordering = ['-month', '-total_bookings']
        unique_together = ['service', 'month']
        indexes = [
            models.Index(
                fields=['month', 'total_bookings'],
                name='idx_servicestat_month_bookings'
            ),
        ]

    def __str__(self):
        return f'{self.service_name} — {self.month}'
