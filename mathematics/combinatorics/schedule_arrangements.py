"""
Permutaciones y Arreglos de Horarios
======================================
Cálculos sobre las posibles formas de organizar citas en un día.

CONCEPTOS:
1. Permutaciones con restricciones: ¿De cuántas formas ordenar N citas
   en M slots, donde algunas tienen restricciones de horario?

2. Arreglos sin repetición: ¿Cuántos días diferentes de trabajo posibles
   existen si tenemos S servicios y H horas disponibles?

3. Principio del palomar (Pigeonhole):
   Si tengo más citas que slots, al menos un slot tendrá 2+ citas.
"""
from math import perm, comb, factorial
from itertools import permutations
from typing import List, Tuple


class ScheduleArrangements:
    """
    Cálculos de arreglos y permutaciones de horarios.

    Uso:
        sa = ScheduleArrangements(total_slots=16, total_appointments=5)
        sa.arrangements()           # P(16,5) formas de asignar citas a slots
        sa.pigeonhole_principle()   # Mínimo de citas por slot
    """

    def __init__(self, total_slots: int = 0, total_appointments: int = 0):
        """
        Args:
            total_slots: Número de slots disponibles (ej: 16 slots de 30min en 8h)
            total_appointments: Número de citas a agendar
        """
        self.slots = total_slots
        self.appointments = total_appointments

    # ── ARREGLOS BÁSICOS ──────────────────────────────────────────────

    def arrangements(self) -> int:
        """
        P(n,k): Número de formas de asignar k citas a n slots distintos.
        (sin repetición: cada slot tiene máximo 1 cita)

        Aplicación: si tengo 16 slots y 5 citas, ¿de cuántas formas
        puedo organizarlas?
        """
        if self.appointments > self.slots:
            return 0
        return perm(self.slots, self.appointments)

    def arrangements_with_repetition(self) -> int:
        """
        n^k: Número de formas si las citas se pueden repetir en slots.
        (con repetición: un slot puede tener múltiples citas - conflictos!)

        Aplicación: calcular la probabilidad de conflictos si asignamos
        citas aleatoriamente.
        """
        return self.slots ** self.appointments

    def total_blocks(self, block_minutes: int, day_minutes: int) -> int:
        """
        Número de bloques de block_minutes que caben en day_minutes.
        """
        return day_minutes // block_minutes

    # ── PRINCIPIO DEL PALOMAR ─────────────────────────────────────────

    def pigeonhole_principle(self) -> Tuple[int, bool]:
        """
        Principio del palomar (Pigeonhole Principle):
        Si n elementos se colocan en m contenedores y n > m,
        entonces al menos un contenedor tiene ⌈n/m⌉ elementos.

        Aplicación: si tengo más citas que slots, detectar
        que habrá conflictos inevitables.

        Returns:
            (mínimo de citas por slot, hay_conflictos_inevitables)
        """
        if self.appointments <= self.slots:
            return (1, False)

        min_per_slot = (self.appointments + self.slots - 1) // self.slots
        return (min_per_slot, True)

    def minimum_slots_needed(self) -> int:
        """
        ¿Cuántos slots mínimo se necesitan para que no haya
        conflictos inevitables? (1 cita por slot)
        """
        return max(self.slots, self.appointments)

    # ── PROBABILIDAD DE CONFLICTO ─────────────────────────────────────

    def conflict_probability(self) -> float:
        """
        Probabilidad de que haya al menos un conflicto si asignamos
        citas aleatoriamente a slots.

        P(al menos 1 conflicto) = 1 - P(ningún conflicto)
        P(ningún conflicto) = P(slots, citas) / slots^citas
        """
        if self.appointments > self.slots:
            return 1.0

        no_conflict = perm(self.slots, self.appointments)
        total = self.slots ** self.appointments
        return 1.0 - (no_conflict / total)

    # ── FACTORIAL Y CRECIMIENTO ───────────────────────────────────────

    @staticmethod
    def factorial_growth(n: int) -> List[int]:
        """
        Muestra el crecimiento factorial: n! para valores 1..n.
        Útil para visualizar por qué la búsqueda exhaustiva
        de horarios es imposible para n grande (NP-hard).

        Ejemplo: 10! = 3,628,800 combinaciones
                 15! = 1.3 billones
        """
        return [factorial(i) for i in range(1, n + 1)]

    @staticmethod
    def is_feasible_bruteforce(n: int, max_combinations: int = 1_000_000) -> Tuple[bool, int]:
        """
        Determina si es factible buscar por fuerza bruta
        (n! combinaciones) dado un máximo de combinaciones.

        Aplicación: decidir cuándo usar algoritmos exactos vs heurísticos.
        """
        total = factorial(n)
        return (total <= max_combinations, total)
