"""
Sistema de Validación de Restricciones (Constraint Satisfaction)
=================================================================
Implementa lógica proposicional para validar que una cita cumple
con todas las reglas de negocio antes de ser agendada.

CONCEPTOS DE LÓGICA DISCRETA:

1. Proposiciones lógicas: Cada restricción es una proposición P_i
   que debe ser VERDADERA para que la cita sea válida.

2. Conjunción: Una cita es válida SII todas las restricciones se cumplen.
   Válida = P_1 ∧ P_2 ∧ ... ∧ P_n

3. Implicación: Si la clienta tiene cita a las 9am, entonces
   el slot de 9am debe estar disponible.
   Cita(9am) → Disponible(9am)

4. Negación: No se puede agendar si hay conflicto.
   ¬Conflicto(cita_nueva, cita_existente)

APLICACIONES:
- Validar una cita antes de crearla
- Explicar POR QUÉ una cita no es posible
- Verificar integridad de la agenda
"""
from typing import List, Dict, Callable, Tuple
from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Constraint:
    """Una restricción lógica con nombre, función de validación y mensaje."""
    name: str
    description: str
    check: Callable[[], bool]
    error_message: str


@dataclass
class ValidationResult:
    """Resultado de la validación de restricciones."""
    is_valid: bool
    passed: List[str] = field(default_factory=list)
    failed: List[Tuple[str, str]] = field(default_factory=list)

    @property
    def summary(self) -> str:
        if self.is_valid:
            return '✅ Todas las restricciones cumplidas.'
        failed_msgs = [f'❌ {name}: {msg}' for name, msg in self.failed]
        return 'Restricciones fallidas:\n' + '\n'.join(failed_msgs)


class ConstraintValidator:
    """
    Validador de restricciones lógicas para agendar citas.

    Uso:
        v = ConstraintValidator()

        # Registrar restricciones
        v.add_constraint('horario_valido', 'Cita dentro del horario laboral',
                         lambda: 8 <= hora < 12 or 13 <= hora < 20,
                         'La cita debe estar en horario laboral (8-12 o 13-20)')

        v.add_constraint('sin_conflicto', 'No hay conflicto con otras citas',
                         lambda: not hay_conflicto,
                         'Ya existe una cita en este horario')

        result = v.validate()
        if not result.is_valid:
            print(result.summary)
    """

    def __init__(self):
        self.constraints: List[Constraint] = []

    def add_constraint(
        self,
        name: str,
        description: str,
        check: Callable[[], bool],
        error_message: str,
    ):
        """Agrega una restricción al validador."""
        self.constraints.append(
            Constraint(name, description, check, error_message)
        )

    def add_required_time_range(self, start: time, end: time, morning_end: time,
                                 afternoon_start: time, afternoon_end: time):
        """
        Restricción: la cita debe estar en horario laboral.
        (start >= morning_start AND end <= morning_end) OR
        (start >= afternoon_start AND end <= afternoon_end)
        """
        def check():
            return (
                (start >= time(8, 0) and end <= morning_end) or
                (start >= afternoon_start and end <= afternoon_end)
            )

        self.add_constraint(
            'horario_laboral',
            'Cita dentro del horario laboral',
            check,
            f'La cita de {start} a {end} no está dentro del horario laboral '
            f'(8:00-{morning_end} o {afternoon_start}-{afternoon_end})'
        )

    def add_conflict_check(self, has_conflict: bool):
        """
        Restricción: no debe haber conflicto con citas existentes.
        Proposición: ¬Conflicto(cita_nueva, citas_existentes)
        """
        self.add_constraint(
            'sin_conflicto',
            'No hay conflicto con otras citas',
            lambda: not has_conflict,
            'Ya existe otra cita en este horario'
        )

    def add_day_off_check(self, is_day_off: bool):
        """Restricción: el especialista no debe tener día libre."""
        self.add_constraint(
            'dia_libre',
            'El especialista no tiene día libre',
            lambda: not is_day_off,
            'La especialista no labora esta fecha'
        )

    def add_max_duration_check(self, duration: int, max_duration: int):
        """Restricción: la duración no debe exceder el máximo."""
        self.add_constraint(
            'duracion_maxima',
            'Duración dentro del límite',
            lambda: duration <= max_duration,
            f'La duración de {duration} min excede el máximo de {max_duration} min'
        )

    def add_future_date_check(self, cita_date: date, today: date):
        """Restricción: la fecha no puede ser pasada."""
        self.add_constraint(
            'fecha_futura',
            'Fecha no es pasada',
            lambda: cita_date >= today,
            'No se pueden agendar citas en fechas pasadas'
        )

    def add_minimum_notice_check(self, cita_datetime, now, min_hours: int = 2):
        """Restricción: debe agendarse con al menos min_hours de anticipación."""
        from datetime import timedelta

        self.add_constraint(
            'anticipacion_minima',
            f'Cita con al menos {min_hours}h de anticipación',
            lambda: cita_datetime >= now + timedelta(hours=min_hours),
            f'La cita debe agendarse con al menos {min_hours} horas de anticipación'
        )

    def validate(self) -> ValidationResult:
        """
        Evalúa TODAS las restricciones.
        La cita es válida SII todas las restricciones son VERDADERAS.

        Válida = C_1 ∧ C_2 ∧ ... ∧ C_n
        """
        result = ValidationResult(is_valid=True)

        for c in self.constraints:
            try:
                if c.check():
                    result.passed.append(c.name)
                else:
                    result.is_valid = False
                    result.failed.append((c.name, c.error_message))
            except Exception as e:
                result.is_valid = False
                result.failed.append((c.name, f'Error: {e}'))

        return result
