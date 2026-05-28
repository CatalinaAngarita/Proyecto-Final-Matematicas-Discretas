"""
Recorridos de Grafos: BFS y DFS
=================================
Implementaciones de BFS (Breadth-First Search) y DFS (Depth-First Search)
aplicados al grafo de relaciones clienta-servicio.

APLICACIONES EN EL NEGOCIO:

BFS (Búsqueda en Anchura):
- Encontrar la distancia más corta entre dos clientas
  a través de servicios compartidos
- "Clientas que tomaron los mismos servicios"
- Recomendaciones en cadena: "a los clientes que les gustó X también les gustó Y"

DFS (Búsqueda en Profundidad):
- Explorar todas las conexiones de un servicio
- Encontrar componentes conexas (grupos de clientas afines)
- Detectar comunidades de clientas con preferencias similares
"""
from collections import deque
from typing import List, Set, Dict, Optional
from .client_service_graph import ClientServiceGraph


class GraphTraversal:
    """
    BFS y DFS sobre el grafo clienta-servicio.

    Uso:
        g = ClientServiceGraph()
        g.add_booking(...)
        t = GraphTraversal(g)

        # BFS: clientas similares
        t.bfs_similar_clients('María G.')

        # DFS: explorar conexiones de un servicio
        t.dfs_explore_service('Manicura')

        # Distancia más corta entre dos clientas
        t.shortest_path('María G.', 'Ana L.')
    """

    def __init__(self, graph: ClientServiceGraph):
        self.graph = graph
        self._adjacency = self._build_adjacency()

    def _build_adjacency(self) -> Dict[str, Set[str]]:
        """
        Construye lista de adyacencia del grafo bipartito.
        Conecta clientas a través de servicios compartidos.

        Estructura: {nodo: set(nodos_vecinos)}
        donde nodo puede ser 'c:nombre' o 's:servicio'
        """
        adj = {}

        for client, services in self.graph.client_to_services.items():
            c_node = f'c:{client}'
            adj[c_node] = {f's:{s}' for s in services}

        for service, clients in self.graph.service_to_clients.items():
            s_node = f's:{service}'
            adj[s_node] = {f'c:{c}' for c in clients}

        return adj

    # ── BFS: Breadth-First Search ─────────────────────────────────────

    def bfs(self, start: str) -> Dict[str, int]:
        """
        BFS desde un nodo inicial.
        Retorna {nodo: distancia} para todos los nodos alcanzables.

        Complejidad: O(V + E)
        """
        visited = {start: 0}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            for neighbor in self._adjacency.get(current, set()):
                if neighbor not in visited:
                    visited[neighbor] = visited[current] + 1
                    queue.append(neighbor)

        return visited

    def bfs_similar_clients(self, client_name: str) -> List[str]:
        """
        BFS: Encuentra clientas similares.
        Clientas a distancia 2 = comparten al menos un servicio.
        Clientas a distancia 4 = comparten clientas que comparten servicios (2 saltos).

        Ejemplo:
            María → Manicura → Ana → Pedicura → Luisa
            (dist 0)  (dist 1)  (dist 2)  (dist 3)  (dist 4)

            María y Ana están a distancia 2 (comparten Manicura).
            María y Luisa están a distancia 4 (conexión indirecta).
        """
        start = f'c:{client_name}'
        distances = self.bfs(start)

        similar = []
        for node, dist in distances.items():
            if node.startswith('c:') and dist == 2:
                similar.append(node[2:])

        return similar

    def shortest_path(self, client_a: str, client_b: str) -> Optional[List[str]]:
        """
        BFS: Distancia más corta entre dos clientas.
        Incluye el camino completo de nodos.

        Retorna: ['c:María', 's:Manicura', 'c:Ana'] o None si no hay conexión.

        Aplicación: ¿qué servicio conecta a dos clientas?
        """
        start = f'c:{client_a}'
        target = f'c:{client_b}'

        if start not in self._adjacency or target not in self._adjacency:
            return None

        parent = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            if current == target:
                return self._reconstruct_path(parent, start, target)

            for neighbor in self._adjacency.get(current, set()):
                if neighbor not in parent:
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None

    def _reconstruct_path(self, parent, start, target):
        """Reconstruye el camino desde parent pointers."""
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    # ── DFS: Depth-First Search ───────────────────────────────────────

    def dfs(self, start: str) -> List[str]:
        """
        DFS desde un nodo inicial.
        Retorna el orden de visita de todos los nodos alcanzables.

        Complejidad: O(V + E)
        """
        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(node)
            for neighbor in self._adjacency.get(node, set()):
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return order

    def dfs_explore_service(self, service_name: str) -> Dict:
        """
        DFS: Explora todas las conexiones de un servicio.

        Retorna estructura jerárquica:
        {
            'service': 'Manicura',
            'clients': ['María', 'Ana'],
            'connected_services': ['Pedicura', 'Cejas'],
            'depth': 3
        }
        """
        start = f's:{service_name}'
        order = self.dfs(start)

        clients = []
        services = []
        for node in order:
            if node.startswith('c:'):
                clients.append(node[2:])
            elif node.startswith('s:'):
                services.append(node[2:])

        return {
            'service': service_name,
            'clients': clients,
            'connected_services': [s for s in services if s != service_name],
            'depth': len(order),
        }

    def connected_components(self) -> List[Set[str]]:
        """
        Encuentra todas las componentes conexas del grafo.

        Una componente conexa es un conjunto de nodos donde cada par
        está conectado por al menos un camino.

        Aplicación: comunidades de clientas con intereses similares.
        """
        all_nodes = set(self._adjacency.keys())
        visited = set()
        components = []

        for node in all_nodes:
            if node not in visited:
                component = set(self.dfs(node))
                components.append(component)
                visited.update(component)

        return components

    def component_clients(self, component: Set[str]) -> List[str]:
        """Extrae solo los nombres de clientas de una componente."""
        return sorted(
            [n[2:] for n in component if n.startswith('c:')]
        )
