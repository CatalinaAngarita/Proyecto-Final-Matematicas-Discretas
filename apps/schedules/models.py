from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel, UUIDModel, TimeStampedModel, BusinessDayChoices
from apps.specialists.models import Specialist


class WorkSchedule(BaseModel):
    """
    ========================================================================
    HORARIO LABORAL
    ========================================================================
    Define qué días y en qué horarios trabaja cada especialista.

    Estructura del día laboral:
    - Mañana: 8:00 AM a 12:00 PM
    - Tarde:   1:00 PM a 8:00 PM

    La pausa de 12:00 a 1:00 es fija (almuerzo) y no se agenda.

    Decisiones de diseño:
    - Dos bloques (mañana/tarde) en lugar de start/end simple porque
      el negocio opera con un descanso fijo al mediodía.
    - unique_together: un especialista solo puede tener un horario por día
    - day_of_week usa IntegerChoices con nombres en español

    Relaciones:
    - Muchos WorkSchedule pertenecen a UN Specialist
    - Un Specialist tiene vario WorkSchedule (uno por día laboral)
    """
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Especialista',
        related_name='work_schedules'
    )
    day_of_week = models.IntegerField(
        'Día de la semana',
        choices=BusinessDayChoices.choices
    )

    # Bloque mañana
    morning_start = models.TimeField('Inicio mañana', default='08:00')
    morning_end = models.TimeField('Fin mañana', default='12:00')

    # Bloque tarde
    afternoon_start = models.TimeField('Inicio tarde', default='13:00')
    afternoon_end = models.TimeField('Fin tarde', default='20:00')

    class Meta:
        verbose_name = 'Horario laboral'
        verbose_name_plural = 'Horarios laborales'
        unique_together = ['specialist', 'day_of_week']
        ordering = ['day_of_week']

    def __str__(self):
        day_name = BusinessDayChoices(self.day_of_week).label
        return f'{self.specialist} - {day_name}'

    def clean(self):
        if self.morning_start >= self.morning_end:
            raise ValidationError({
                'morning_end': 'El fin de la mañana debe ser después del inicio.'
            })
        if self.afternoon_start >= self.afternoon_end:
            raise ValidationError({
                'afternoon_end': 'El fin de la tarde debe ser después del inicio.'
            })
        if self.morning_end > self.afternoon_start:
            raise ValidationError(
                'El bloque de mañana y tarde no deben solaparse.'
            )


class BreakSchedule(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    DESCANSO PROGRAMADO
    ========================================================================
    Representa un periodo de descanso en un día específico.
    Por ejemplo: "Diana toma 30 min de descanso el 25/05 a las 4pm".

    Diferencia con DayOff:
    - BreakSchedule: descanso PARCIAL (ej: 2 horas)
    - DayOff: día COMPLETO sin labor

    NO hereda SoftDelete porque los descansos pasados se mantienen
    como registro histórico.

    Relaciones:
    - Muchos BreakSchedule pertenecen a UN Specialist
    """
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Especialista',
        related_name='breaks'
    )
    date = models.DateField('Fecha', db_index=True)
    start_time = models.TimeField('Hora inicio')
    end_time = models.TimeField('Hora fin')
    reason = models.CharField('Motivo', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Descanso'
        verbose_name_plural = 'Descansos'
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(
                fields=['specialist', 'date'],
                name='idx_break_specialist_date'
            ),
        ]

    def __str__(self):
        return f'{self.specialist} - {self.date} {self.start_time}-{self.end_time}'

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('El descanso debe iniciar antes de terminar.')


class DayOff(UUIDModel, TimeStampedModel):
    """
    ========================================================================
    DÍA LIBRE
    ========================================================================
    Día completo en que un especialista NO labora.
    Ejemplos: vacaciones, citas médicas, días festivos.

    unique_together: un especialista no puede tener dos registros
    de día libre para la misma fecha.

    NO hereda SoftDelete (histórico inmodificable).

    Relaciones:
    - Muchos DayOff pertenecen a UN Specialist
    """
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name='Especialista',
        related_name='days_off'
    )
    date = models.DateField('Fecha', db_index=True)
    reason = models.CharField('Motivo', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Día libre'
        verbose_name_plural = 'Días libres'
        unique_together = ['specialist', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.specialist} - {self.date}'
