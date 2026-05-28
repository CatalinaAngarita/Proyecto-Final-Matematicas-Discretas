"""
Grafo Bipartito Clienta ↔ Servicio
====================================
Modela las relaciones entre clientas y los servicios que han tomado.

Estructura:
- Partición A: Clientes (nodos 'c:{id}')
- Partición B: Servicios (nodos 's:{id}')
- Arista (c, s): El cliente c ha tomado el servicio s

Aplicaciones:
- Recomendación: "clientas que tomaron X también tomaron Y"
- Popularidad: servicios más demandados
- Fidelización: clientas con mayor variedad de servicios
"""
from collections import defaultdict
from typing import List, Tuple, Set, Dict


class ClientServiceGraph:
    """
    Grafo bipartito clienta-servicio.

    Uso:
        g = ClientServiceGraph()
        g.add_booking('María G.', 'Manicura')
        g.add_booking('María G.', 'Pedicura')
        g.add_booking('Carolina M.', 'Manicura')
        g.client_degree('María G.')  # → 2
        g.connected_clients('Manicura')  # → ['María G.', 'Carolina M.']
    """

    def __init__(self):
        # listas de adyacencia
        self.client_to_services: Dict[str, Set[str]] = defaultdict(set)
        self.service_to_clients: Dict[str, Set[str]] = defaultdict(set)
        self._built = False

    def add_booking(self, client_name: str, service_name: str):
        """Registra que una clienta tomó un servicio."""
        self.client_to_services[client_name].add(service_name)
        self.service_to_clients[service_name].add(client_name)

    def add_bookings_batch(self, bookings: List[Tuple[str, str]]):
        """Registra múltiples reservas de una sola vez."""
        for client, service in bookings:
            self.add_booking(client, service)

    # ── PROPIEDADES DEL GRAFO ──────────────────────────────────────────

    @property
    def clients(self) -> List[str]:
        """Lista de todas las clientas en el grafo."""
        return list(self.client_to_services.keys())

    @property
    def services(self) -> List[str]:
        """Lista de todos los servicios en el grafo."""
        return list(self.service_to_clients.keys())

    @property
    def total_vertices(self) -> int:
        """Número total de nodos (clientas + servicios)."""
        return len(self.clients) + len(self.services)

    @property
    def total_edges(self) -> int:
        """Número total de aristas (reservas registradas)."""
        return sum(len(s) for s in self.client_to_services.values())

    def client_degree(self, client_name: str) -> int:
        """
        Grado de un nodo clienta = número de servicios distintos que ha tomado.
        Análogo en teoría de grafos: |N(v)| para v en partición clienta.
        """
        return len(self.client_to_services.get(client_name, set()))

    def service_degree(self, service_name: str) -> int:
        """
        Grado de un nodo servicio = número de clientas que lo han tomado.
        """
        return len(self.service_to_clients.get(service_name, set()))

    def connected_clients(self, service_name: str) -> List[str]:
        """Clientas que han tomado un servicio específico."""
        return list(self.service_to_clients.get(service_name, set()))

    def connected_services(self, client_name: str) -> List[str]:
        """Servicios que una clienta ha tomado."""
        return list(self.client_to_services.get(client_name, set()))

    # ── ANÁLISIS ───────────────────────────────────────────────────────

    def shared_services(self, client_a: str, client_b: str) -> List[str]:
        """
        Servicios que dos clientas tienen en común.
        Intersección de conjuntos: S(a) ∩ S(b)
        """
        services_a = self.client_to_services.get(client_a, set())
        services_b = self.client_to_services.get(client_b, set())
        return list(services_a & services_b)

    def most_popular_services(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Top N servicios más populares (mayor grado).
        Ordena por |N(s)| descendente.
        """
        return sorted(
            [(s, self.service_degree(s)) for s in self.services],
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

    def most_loyal_clients(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Top N clientas con mayor variedad de servicios.
        """
        return sorted(
            [(c, self.client_degree(c)) for c in self.clients],
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

    def service_recommendations(self, client_name: str, top_n: int = 3) -> List[str]:
        """
        Recomienda servicios a una clienta basado en:
        "clientas que tomaron los mismos servicios que tú, también tomaron..."

        Algoritmo:
        1. Encuentra servicios que ha tomado la clienta
        2. Encuentra clientas que compartan al menos 1 servicio
        3. De esas clientas, qué servicios adicionales han tomado
        4. Ranking por frecuencia
        """
        my_services = self.client_to_services.get(client_name, set())
        if not my_services:
            return []

        similar_clients = set()
        for service in my_services:
            similar_clients.update(self.service_to_clients.get(service, set()))

        similar_clients.discard(client_name)

        recommendations = defaultdict(int)
        for other in similar_clients:
            other_services = self.client_to_services.get(other, set())
            for s in other_services:
                if s not in my_services:
                    recommendations[s] += 1

        return [
            s for s, _ in sorted(
                recommendations.items(), key=lambda x: x[1], reverse=True
            )
        ][:top_n]

    def to_networkx(self):
        """
        Convierte a grafo NetworkX para visualización.
        Retorna (G, pos, node_colors, labels).
        """
        import networkx as nx

        G = nx.Graph()
        client_nodes = [f'c:{c}' for c in self.clients]
        service_nodes = [f's:{s}' for s in self.services]

        G.add_nodes_from(client_nodes, bipartite=0)
        G.add_nodes_from(service_nodes, bipartite=1)

        for client, services in self.client_to_services.items():
            for service in services:
                G.add_edge(f'c:{client}', f's:{service}')

        pos = nx.bipartite_layout(G, client_nodes)

        node_colors = [
            '#8B5E83' if n.startswith('c:') else '#5E8B6E'
            for n in G.nodes()
        ]

        labels = {
            n: n[2:] for n in G.nodes()
        }

        return G, pos, node_colors, labels
