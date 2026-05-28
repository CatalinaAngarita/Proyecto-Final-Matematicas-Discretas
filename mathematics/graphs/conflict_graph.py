"""
Grafo de Conflictos de Citas (Conflict Graph)
===============================================
Modela los conflictos de horario entre citas agendadas.

Estructura:
- Nodos: Citas (appointment_id)
- Aristas no dirigidas: Dos citas se SOLAPAN en tiempo
  (start_i < end_j AND start_j < end_i)

Aplicaciones:
- Detectar visualmente conflictos en la agenda
- Calcular el número cromático (colorear citas que no conflictúan)
- Encontrar el conjunto máximo de citas sin conflictos (MIS)

Conceptos de Matemáticas Discretas:
- Grafo de intervalos (interval graph): las citas son intervalos en ℝ
- Los grafos de intervalos son perfectos (perfect graphs)
- El número cromático = tamaño de la clique máxima
  (= grosor máximo de la agenda = máximo número de citas simultáneas)
"""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class AppointmentNode:
    """Representa una cita como nodo del grafo."""
    id: str
    client: str
    service: str
    start: str
    end: str

    def duration_minutes(self) -> int:
        h1, m1 = map(int, self.start.split(':'))
        h2, m2 = map(int, self.end.split(':'))
        return (h2 * 60 + m2) - (h1 * 60 + m1)


class ConflictGraph:
    """
    Grafo de conflictos entre citas.

    Uso:
        g = ConflictGraph()
        g.add_appointment('1', 'María', 'Manicura', '09:00', '10:00')
        g.add_appointment('2', 'Ana', 'Pedicura', '09:30', '10:30')
        g.add_appointment('3', 'Luisa', 'Cejas', '10:00', '10:30')
        g.conflicts  # → {'1': {'2'}, '2': {'1', '3'}, '3': {'2'}}
        g.is_independent_set(['1', '3'])  # → True (no se solapan)
    """

    def __init__(self):
        self.appointments: Dict[str, AppointmentNode] = {}
        self.conflicts: Dict[str, set] = {}

    def add_appointment(self, id: str, client: str, service: str,
                        start: str, end: str):
        """Agrega una cita al grafo y recalcula conflictos."""
        node = AppointmentNode(id, client, service, start, end)
        self.appointments[id] = node
        self._rebuild_conflicts()

    def add_appointments_batch(self, appointments: List[AppointmentNode]):
        """Agrega múltiples citas."""
        for apt in appointments:
            self.appointments[apt.id] = apt
        self._rebuild_conflicts()

    def _rebuild_conflicts(self):
        """
        Reconstruye todas las aristas de conflicto.
        Dos citas tienen conflicto SII sus intervalos se solapan:
            start_i < end_j AND start_j < end_i
        """
        self.conflicts = {aid: set() for aid in self.appointments}
        ids = list(self.appointments.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a = self.appointments[ids[i]]
                b = self.appointments[ids[j]]
                if self._overlaps(a, b):
                    self.conflicts[a.id].add(b.id)
                    self.conflicts[b.id].add(a.id)

    def _overlaps(self, a: AppointmentNode, b: AppointmentNode) -> bool:
        """Dos intervalos se solapan si y solo si: start_a < end_b AND start_b < end_a."""
        return a.start < b.end and b.start < a.end

    # ── CONSULTAS ──────────────────────────────────────────────────────

    @property
    def total_conflicts(self) -> int:
        """Número total de pares en conflicto = |E|."""
        return sum(len(n) for n in self.conflicts.values()) // 2

    def has_conflict(self, appointment_id: str) -> bool:
        """Una cita específica tiene conflictos?"""
        return len(self.conflicts.get(appointment_id, set())) > 0

    def conflicting_appointments(self, appointment_id: str) -> List[AppointmentNode]:
        """Citas que conflictúan con una dada."""
        return [
            self.appointments[cid]
            for cid in self.conflicts.get(appointment_id, set())
        ]

    def is_independent_set(self, ids: List[str]) -> bool:
        """
        Verifica si un conjunto de citas es independiente
        (ninguna tiene conflicto con otra del conjunto).
        Aplicación: elegir citas que pueden coexistir.
        """
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if ids[j] in self.conflicts.get(ids[i], set()):
                    return False
        return True

    def maximum_independent_set(self) -> List[AppointmentNode]:
        """
        Heurística greedy para encontrar un conjunto grande
        (no necesariamente máximo) de citas sin conflictos.

        Algoritmo: ordenar por hora fin, seleccionar la que termina
        más temprano, eliminar sus conflictos, repetir.
        """
        sorted_apts = sorted(
            self.appointments.values(),
            key=lambda a: a.end
        )

        selected = []
        excluded = set()

        for apt in sorted_apts:
            if apt.id not in excluded:
                selected.append(apt)
                excluded.update(self.conflicts.get(apt.id, set()))
                excluded.add(apt.id)

        return selected

    def chromatic_number_lower_bound(self) -> int:
        """
        Cota inferior del número cromático = tamaño de la clique máxima.
        En un grafo de intervalos, el número cromático = clique máxima.

        Se calcula como el máximo número de citas que se solapan
        en un mismo punto del tiempo.
        """
        events = []
        for apt in self.appointments.values():
            events.append((apt.start, 'start'))
            events.append((apt.end, 'end'))

        events.sort(key=lambda x: (x[0], x[1] == 'end'))

        max_concurrent = 0
        current = 0
        for time, etype in events:
            if etype == 'start':
                current += 1
                max_concurrent = max(max_concurrent, current)
            else:
                current -= 1

        return max_concurrent

    def schedule_feasibility(self) -> Tuple[bool, str]:
        """
        Verifica si el schedule actual es factible.
        En un grafo de intervalos con 1 especialista,
        el schedule es factible si el número cromático ≤ 1
        (máximo 1 cita simultánea por especialista).
        """
        chromatic = self.chromatic_number_lower_bound()
        if chromatic <= 1:
            return True, 'Schedule factible: sin conflictos.'
        else:
            conflict_ids = []
            for aid, deps in self.conflicts.items():
                if deps:
                    conflict_ids.append(aid)
            return False, (
                f'Schedule NO factible: {chromatic} citas simultáneas. '
                f'{self.total_conflicts} conflictos detectados. '
                f'Citas conflictivas: {conflict_ids[:5]}...'
            )

    def to_networkx(self):
        """Convierte a grafo NetworkX."""
        import networkx as nx

        G = nx.Graph()
        for aid, node in self.appointments.items():
            G.add_node(aid, label=f'{node.client}\n{node.service}')

        for aid, deps in self.conflicts.items():
            for dep in deps:
                G.add_edge(aid, dep)

        pos = nx.spring_layout(G, seed=42, k=1.5)

        degrees = dict(G.degree())
        node_sizes = [300 + degrees[n] * 100 for n in G.nodes()]
        node_colors = ['#D4726A' if degrees[n] > 0 else '#5E8B6E' for n in G.nodes()]

        return G, pos, node_colors, node_sizes
