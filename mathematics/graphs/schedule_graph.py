"""
Grafo de Horarios (Schedule Graph)
====================================
Representa los slots de tiempo disponibles como un grafo dirigido.

Estructura:
- Nodos: Slots de 30 minutos (time slot: '08:00', '08:30', ..., '19:30')
- Aristas dirigidas: Conectan slot_i → slot_{i+1} (el flujo del tiempo)
- Nodos ocupados: Tienen una propiedad 'occupied=True' si hay cita

Aplicaciones:
- Visualizar ocupación del día de un especialista
- Encontrar slots libres contiguos (walk en el grafo)
- Optimizar asignación: encontrar el camino más corto entre slots libres
"""
from datetime import time, timedelta
from typing import List, Dict, Optional


class ScheduleGraph:
    """
    Grafo dirigido de slots de tiempo.

    Uso:
        g = ScheduleGraph()
        g.build_slots('08:00', '12:00', slot_minutes=30)
        g.occupy('09:00', '10:00')
        g.occupy('10:30', '11:30')
        g.available_slots()  # → [('08:00','09:00'), ('10:00','10:30'), ...]
        g.longest_available_block()  # → ('08:00', '09:00')
    """

    def __init__(self):
        self.slots: Dict[str, dict] = {}
        self.edges: List[tuple] = []
        self.slot_minutes = 30
        self._ordered_slots: List[str] = []

    def build_slots(self, start: str, end: str, slot_minutes: int = 30):
        """
        Construye el grafo de slots para un bloque horario.

        Args:
            start: Hora inicio (HH:MM)
            end: Hora fin (HH:MM)
            slot_minutes: Duración de cada slot (default: 30)
        """
        self.slot_minutes = slot_minutes
        current = self._str_to_time(start)
        end_time = self._str_to_time(end)
        self.slots = {}
        self.edges = []
        self._ordered_slots = []

        while current < end_time:
            slot_key = self._time_to_str(current)
            self.slots[slot_key] = {
                'time': current,
                'occupied': False,
                'appointment_id': None,
                'index': len(self._ordered_slots),
            }
            self._ordered_slots.append(slot_key)
            current += timedelta(minutes=slot_minutes)

        for i in range(len(self._ordered_slots) - 1):
            self.edges.append((self._ordered_slots[i], self._ordered_slots[i + 1]))

    def _str_to_time(self, s: str) -> time:
        h, m = map(int, s.split(':'))
        return time(h, m)

    def _time_to_str(self, t: time) -> str:
        return f'{t.hour:02d}:{t.minute:02d}'

    # ── OCUPACIÓN ──────────────────────────────────────────────────────

    def occupy(self, start: str, end: str, appointment_id=None):
        """
        Marca slots como ocupados en el intervalo [start, end).

        Args:
            start: Hora inicio (HH:MM)
            end: Hora fin (HH:MM)
            appointment_id: ID opcional de la cita
        """
        current = self._str_to_time(start)
        end_time = self._str_to_time(end)

        while current < end_time:
            slot_key = self._time_to_str(current)
            if slot_key in self.slots:
                self.slots[slot_key]['occupied'] = True
                self.slots[slot_key]['appointment_id'] = appointment_id
            current += timedelta(minutes=self.slot_minutes)

    def free(self, start: str, end: str):
        """Libera slots en el intervalo [start, end)."""
        current = self._str_to_time(start)
        end_time = self._str_to_time(end)
        while current < end_time:
            slot_key = self._time_to_str(current)
            if slot_key in self.slots:
                self.slots[slot_key]['occupied'] = False
                self.slots[slot_key]['appointment_id'] = None
            current += timedelta(minutes=self.slot_minutes)

    def clear(self):
        """Limpia todas las ocupaciones."""
        for key in self.slots:
            self.slots[key]['occupied'] = False
            self.slots[key]['appointment_id'] = None

    # ── CONSULTAS ──────────────────────────────────────────────────────

    def is_available(self, start: str, duration_minutes: int) -> bool:
        """
        Verifica si un bloque de duración dada está disponible.

        Args:
            start: Hora inicio
            duration_minutes: Duración en minutos

        Returns:
            True si todo el bloque está libre
        """
        current = self._str_to_time(start)
        end = current + timedelta(minutes=duration_minutes)

        while current < end:
            key = self._time_to_str(current)
            if key not in self.slots or self.slots[key]['occupied']:
                return False
            current += timedelta(minutes=self.slot_minutes)

        return True

    def available_slots(self) -> List[tuple]:
        """
        Encuentra bloques contiguos disponibles.
        Recorre el grafo siguiendo aristas mientras los nodos estén libres.

        Returns:
            Lista de (start, end) disponibles
        """
        available = []
        i = 0
        while i < len(self._ordered_slots):
            if not self.slots[self._ordered_slots[i]]['occupied']:
                block_start = self._ordered_slots[i]
                while (
                    i < len(self._ordered_slots)
                    and not self.slots[self._ordered_slots[i]]['occupied']
                ):
                    i += 1
                block_end = self._ordered_slots[i - 1]
                available.append((block_start, block_end))
            else:
                i += 1

        return available

    def longest_available_block(self) -> Optional[tuple]:
        """
        Encuentra el bloque libre más largo.

        Aplicación: encontrar el mejor momento para agendar
        un servicio largo (ej: uñas acrílicas 120 min).
        """
        blocks = self.available_slots()
        if not blocks:
            return None

        def block_duration(block):
            start = self._str_to_time(block[0])
            end = self._str_to_time(block[1])
            return (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)

        return max(blocks, key=block_duration)

    def occupancy_rate(self) -> float:
        """
        Tasa de ocupación del día.
        """
        if not self.slots:
            return 0.0
        occupied = sum(1 for s in self.slots.values() if s['occupied'])
        return occupied / len(self.slots)

    # ── NetworkX ───────────────────────────────────────────────────────

    def to_networkx(self):
        """
        Convierte a grafo dirigido NetworkX.
        """
        import networkx as nx

        G = nx.DiGraph()
        for slot_key, data in self.slots.items():
            G.add_node(slot_key, occupied=data['occupied'],
                       appointment_id=data['appointment_id'])
        G.add_edges_from(self.edges)

        pos = nx.kamada_kawai_layout(G)

        node_colors = [
            '#E8C35E' if not G.nodes[n]['occupied'] else '#D4726A'
            for n in G.nodes()
        ]

        return G, pos, node_colors
