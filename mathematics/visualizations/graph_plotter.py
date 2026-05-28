"""
Visualizador de Grafos
========================
Genera gráficos de los diferentes tipos de grafos usados
en el sistema de booking.

REQUIERE: matplotlib, networkx

Uso:
    plotter = GraphPlotter()
    plotter.plot_bipartite(clients, services, edges)
    plotter.plot_schedule(timeslots, appointments)
    plotter.plot_conflict_graph(intervals)
    plotter.show()  # o plotter.save('output/')
"""
import os
from typing import List, Tuple, Dict, Any
from datetime import time


class GraphPlotter:
    """
    Genera visualizaciones de grafos.

    Dependencia opcional: si matplotlib no está instalado,
    los métodos escriben datos en vez de graficar.
    """

    def __init__(self, output_dir: str = None):
        self._matplotlib = None
        self._networkx = None
        self._figures = []
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'output'
        )

    def _check_deps(self):
        """Intenta cargar matplotlib y networkx."""
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
            self._matplotlib = plt
            self._networkx = nx
            return True
        except ImportError:
            return False

    def _ensure_output_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_bipartite(self, clients: List[str], services: List[str],
                        edges: List[Tuple[int, int]],
                        title: str = 'Grafo Bipartito: Clientes ↔ Servicios'):
        """
        Grafo bipartito clientes-servicios.

        Los clientes están a la izquierda, servicios a la derecha.
        Una arista significa que el cliente ha tomado ese servicio.
        """
        has_deps = self._check_deps()
        if not has_deps:
            print('[GraphPlotter] matplotlib/networkx no instalados. '
                  'Saltando gráfico bipartito.')
            return

        plt = self._matplotlib
        nx = self._networkx

        G = nx.Graph()
        left_nodes = [f'C_{i}' for i in range(len(clients))]
        right_nodes = [f'S_{j}' for j in range(len(services))]

        G.add_nodes_from(left_nodes, bipartite=0)
        G.add_nodes_from(right_nodes, bipartite=1)
        G.add_edges_from([(f'C_{i}', f'S_{j}') for i, j in edges])

        pos = {}
        pos.update(
            (node, (1, index))
            for index, node in enumerate(left_nodes)
        )
        pos.update(
            (node, (2, index))
            for index, node in enumerate(right_nodes)
        )

        fig, ax = plt.subplots(figsize=(10, max(6, len(clients) * 0.5)))
        nx.draw(G, pos, with_labels=True,
                node_color=['#8B5E83' if n.startswith('C') else '#5E8B6E'
                            for n in G.nodes()],
                node_size=800, font_size=9, font_color='white',
                edge_color='#E8C35E', width=1.5, ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        self._figures.append(('bipartite', fig))

    def plot_schedule_graph(self, timeslots: List[str],
                             appointments: List[Tuple[str, str, str]],
                             title: str = 'Grafo de Horarios: Slots → Citas'):
        """
        Grafo dirigido de asignación de slots a citas.

        Cada slot apunta a la cita asignada (si existe).
        """
        has_deps = self._check_deps()
        if not has_deps:
            print('[GraphPlotter] matplotlib/networkx no instalados. '
                  'Saltando gráfico de horarios.')
            return

        plt = self._matplotlib
        nx = self._networkx

        G = nx.DiGraph()
        slot_nodes = [f'Slot {s}' for s in timeslots]
        apt_nodes = [f'{c} @ {t}' for c, t, _ in appointments]

        G.add_nodes_from(slot_nodes, layer='slot')
        G.add_nodes_from(apt_nodes, layer='appointment')

        for slot_label in slot_nodes:
            matching = [
                n for n in apt_nodes
                if slot_label.replace('Slot ', '') in n
            ]
            if matching:
                G.add_edge(slot_label, matching[0])
            else:
                G.add_edge(slot_label, '(libre)')
                G.add_node('(libre)', layer='free')

        fig, ax = plt.subplots(figsize=(12, len(timeslots) * 0.6))
        pos = nx.spring_layout(G, k=2, iterations=50)
        nx.draw(G, pos, with_labels=True,
                node_color=['#8B5E83' if G.nodes[n].get('layer') == 'slot'
                            else '#5E8B6E' if G.nodes[n].get('layer') == 'appointment'
                            else '#E8C35E'
                            for n in G.nodes()],
                node_size=600, font_size=8,
                edge_color='gray', arrows=True, ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        self._figures.append(('schedule', fig))

    def plot_conflict_graph(self, intervals: List[Tuple[str, time, time]],
                              title: str = 'Grafo de Conflictos (Intervalos)'):
        """
        Grafo de conflictos: arista entre citas que se solapan.

        Se muestra como grafo de intervalos.
        """
        has_deps = self._check_deps()
        if not has_deps:
            print('[GraphPlotter] matplotlib/networkx no instalados. '
                  'Saltando gráfico de conflictos.')
            return

        plt = self._matplotlib
        nx = self._networkx

        G = nx.Graph()
        ids = [i for i, _, _ in intervals]

        for i in range(len(intervals)):
            for j in range(i + 1, len(intervals)):
                id_a, s_a, e_a = intervals[i]
                id_b, s_b, e_b = intervals[j]
                if s_a < e_b and s_b < e_a:
                    G.add_edge(id_a, id_b)

        G.add_nodes_from(ids)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Izquierda: grafo de conflictos
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True,
                node_color='#8B5E83', node_size=800,
                font_color='white', font_size=10,
                edge_color='#E74C3C', width=2, ax=ax1)
        ax1.set_title('Grafo de Conflictos', fontsize=12, fontweight='bold')

        # Derecha: representación de intervalos
        for idx, (id_, start, end) in enumerate(intervals):
            s_min = start.hour * 60 + start.minute
            e_min = end.hour * 60 + end.minute
            ax2.barh(idx, e_min - s_min, left=s_min,
                     height=0.6, color='#5E8B6E', alpha=0.7)
            ax2.text(s_min + 1, idx, id_, va='center', fontsize=9)

        ax2.set_yticks(range(len(intervals)))
        ax2.set_yticklabels([i for i, _, _ in intervals])
        ax2.set_xlabel('Minutos del día')
        ax2.set_title('Representación de Intervalos', fontsize=12,
                      fontweight='bold')

        fig.suptitle(title, fontsize=14, fontweight='bold')
        self._figures.append(('conflict', fig))

    def save(self, output_dir: str = None):
        """Guarda todas las figuras como PNG."""
        d = output_dir or self.output_dir
        self._ensure_output_dir()
        for name, fig in self._figures:
            path = os.path.join(d, f'{name}.png')
            fig.savefig(path, dpi=150, bbox_inches='tight')
            print(f'  Gráfico guardado: {path}')
        plt = self._matplotlib
        if plt:
            plt.close('all')

    def show(self):
        """Muestra todas las figuras."""
        plt = self._matplotlib
        if plt:
            plt.show()
