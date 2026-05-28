"""
Detector Lógico de Conflictos
===============================
Implementa la detección de conflictos usando lógica proposicional
y teoría de conjuntos.

FUNDAMENTO MATEMÁTICO:

Dados dos intervalos I_i = [start_i, end_i) y I_j = [start_j, end_j),
hay conflicto SII:
    start_i < end_j AND start_j < end_i

Esto es equivalente a:
    I_i ∩ I_j ≠ ∅

APLICACIONES:
- Detectar conflictos al agendar una nueva cita
- Auditar la agenda existente
- Explicar POR QUÉ hay conflicto
"""
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from datetime import date, time


@dataclass
class TimeInterval:
    """Un intervalo de tiempo [start, end)."""
    start: time
    end: time

    def overlaps_with(self, other: 'TimeInterval') -> bool:
        """
        Dos intervalos se solapan SII:
            start_this < end_other AND start_other < end_this
        """
        return self.start < other.end and other.start < self.end

    def intersection(self, other: 'TimeInterval') -> int:
        """
        Duración de la intersección en minutos.
        |I_i ∩ I_j| = max(0, min(end_i, end_j) - max(start_i, start_j))
        """
        latest_start = max(self.start, other.start)
        earliest_end = min(self.end, other.end)

        if latest_start < earliest_end:
            return (
                (earliest_end.hour * 60 + earliest_end.minute) -
                (latest_start.hour * 60 + latest_start.minute)
            )
        return 0


class ConflictDetector:
    """
    Detector lógico de conflictos de horario.

    Uso:
        cd = ConflictDetector()
        cd.add_appointment('1', time(9, 0), time(10, 0))
        cd.add_appointment('2', time(9, 30), time(10, 30))

        conflicts = cd.find_conflicts()
        # → [{'a': '1', 'b': '2', 'overlap': 30}]

        cd.can_schedule(time(10, 0), time(11, 0))
        # → True
    """

    def __init__(self):
        self.appointments: Dict[str, TimeInterval] = {}

    def add_appointment(self, id: str, start: time, end: time):
        """Registra una cita."""
        self.appointments[id] = TimeInterval(start, end)

    def find_conflicts(self) -> List[Dict]:
        """
        Encuentra todos los pares de citas que se solapan.

        Complejidad: O(n²) donde n = número de citas
        """
        conflicts = []
        ids = list(self.appointments.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a = self.appointments[ids[i]]
                b = self.appointments[ids[j]]
                if a.overlaps_with(b):
                    conflicts.append({
                        'appointment_a': ids[i],
                        'appointment_b': ids[j],
                        'overlap_minutes': a.intersection(b),
                    })

        return conflicts

    def can_schedule(self, start: time, end: time) -> Tuple[bool, List[str]]:
        """
        Verifica si se puede agendar una nueva cita.

        Returns:
            (puede_agendar, [razones_de_conflicto])
        """
        new_interval = TimeInterval(start, end)
        conflicting = []

        for id, interval in self.appointments.items():
            if new_interval.overlaps_with(interval):
                conflicting.append(id)

        return len(conflicting) == 0, conflicting

    def find_available_blocks(self, day_start: time, day_end: time,
                               min_duration: int = 30) -> List[Tuple[time, time]]:
        """
        Encuentra bloques disponibles en el día de duración >= min_duration.

        Algoritmo: ordenar citas por start, encontrar huecos entre ellas.
        """
        sorted_apts = sorted(
            self.appointments.items(),
            key=lambda x: x[1].start
        )

        available = []
        cursor = day_start

        for id, interval in sorted_apts:
            if cursor < interval.start:
                gap = (
                    (interval.start.hour * 60 + interval.start.minute) -
                    (cursor.hour * 60 + cursor.minute)
                )
                if gap >= min_duration:
                    available.append((cursor, interval.start))
            cursor = max(cursor, interval.end)

        if cursor < day_end:
            gap = (
                (day_end.hour * 60 + day_end.minute) -
                (cursor.hour * 60 + cursor.minute)
            )
            if gap >= min_duration:
                available.append((cursor, day_end))

        return available

    def conflict_report(self) -> Dict:
        """Reporte completo de conflictos."""
        conflicts = self.find_conflicts()
        total_overlap = sum(c['overlap_minutes'] for c in conflicts)

        return {
            'total_appointments': len(self.appointments),
            'total_conflicts': len(conflicts),
            'total_overlap_minutes': total_overlap,
            'appointments_in_conflict': len({
                c['appointment_a'] for c in conflicts
            } | {c['appointment_b'] for c in conflicts}),
            'has_conflicts': len(conflicts) > 0,
        }
