"""
Combinatoria de Servicios
==========================
Cálculos de combinaciones y permutaciones aplicados a los servicios del spa.

CONCEPTOS DE MATEMÁTICAS DISCRETAS:

1. Combinaciones: C(n,k) = n! / (k!(n-k)!)
   ¿Cuántos paquetes de k servicios puedo ofrecer si tengo n servicios?
   Ej: Con 15 servicios, ¿cuántos paquetes de 3 servicios diferentes existen?

2. Permutaciones: P(n,k) = n! / (n-k)!
   ¿De cuántas formas puedo ordenar k servicios en un día?

3. Potencias: n^k
   ¿Cuántas secuencias de k servicios puedo formar (con repetición)?

APLICACIONES EN EL NEGOCIO:
- Crear paquetes promocionales (combinaciones de servicios)
- Calcular horarios posibles (permutaciones de citas)
- Estimar capacidad del día
"""
from math import comb, perm, factorial
from typing import List, Tuple, Iterator
from itertools import combinations, permutations


class ServiceCombinations:
    """
    Cálculos combinatorios sobre servicios del spa.

    Uso:
        sc = ServiceCombinations()
        sc.add_service('Manicura', 45)
        sc.add_service('Pedicura', 45)
        sc.add_service('Uñas Acrílicas', 120)
        sc.add_service('Cejas', 30)

        sc.combinations(2)      # Pares de servicios
        sc.total_packages(3)    # Todos los paquetes de 3 servicios
        sc.package_duration(['Manicura', 'Pedicura'])  # 90 min
    """

    def __init__(self):
        self.services: List[Tuple[str, int]] = []
        self._names: List[str] = []

    def add_service(self, name: str, duration_minutes: int):
        """Registra un servicio con su duración."""
        self.services.append((name, duration_minutes))
        self._names.append(name)

    def add_services_batch(self, service_list: List[Tuple[str, int]]):
        """Registra múltiples servicios."""
        for name, duration in service_list:
            self.add_service(name, duration)

    @property
    def n(self) -> int:
        """Número total de servicios registrados."""
        return len(self.services)

    # ── COMBINACIONES ──────────────────────────────────────────────────

    def combinations(self, k: int) -> int:
        """
        C(n,k): Número de formas de elegir k servicios SIN orden.
        ¿Cuántos paquetes de k servicios puedo ofrecer?
        """
        if k > self.n:
            return 0
        return comb(self.n, k)

    def combinations_with_repetition(self, k: int) -> int:
        """
        C(n+k-1, k): Combinaciones CON repetición.
        ¿Cuántas formas de elegir k servicios si se pueden repetir?
        """
        return comb(self.n + k - 1, k)

    def list_combinations(self, k: int) -> Iterator[Tuple[str, ...]]:
        """Genera todas las combinaciones de k servicios."""
        return combinations(self._names, k)

    def total_packages(self, max_services: int = None) -> int:
        """
        Suma de todas las combinaciones posibles desde 1 hasta n o max.

        ∑ C(n,k) para k = 1 hasta min(n, max_services)

        Esto es: de 1 servicio hasta N servicios, ¿cuántos paquetes únicos?
        """
        if max_services is None or max_services > self.n:
            max_services = self.n
        return sum(comb(self.n, k) for k in range(1, max_services + 1))

    # ── PERMUTACIONES ──────────────────────────────────────────────────

    def permutations(self, k: int) -> int:
        """
        P(n,k): Número de formas de ordenar k servicios.
        ¿De cuántas formas puedo agendar k servicios en un día?
        """
        if k > self.n:
            return 0
        return perm(self.n, k)

    def list_permutations(self, k: int) -> Iterator[Tuple[str, ...]]:
        """Genera todas las permutaciones de k servicios."""
        return permutations(self._names, k)

    # ── DURACIONES ─────────────────────────────────────────────────────

    def package_duration(self, selected: List[str]) -> int:
        """
        Duración total de un paquete de servicios (suma de minutos).
        """
        duration_map = dict(self.services)
        return sum(duration_map.get(s, 0) for s in selected)

    def package_durations(self, k: int) -> List[Tuple[Tuple[str, ...], int]]:
        """
        Calcula la duración de todas las combinaciones de k servicios.
        Útil para encontrar paquetes que quepan en un bloque de tiempo.
        """
        return [
            (combo, self.package_duration(list(combo)))
            for combo in self.list_combinations(k)
        ]

    def packages_fitting_in(self, max_minutes: int, k: int) -> List[Tuple[str, ...]]:
        """
        Encuentra combinaciones de k servicios cuya duración total
        no exceda max_minutes.
        """
        return [
            combo for combo, duration in self.package_durations(k)
            if duration <= max_minutes
        ]

    # ── CAPACIDAD DEL DÍA ──────────────────────────────────────────────

    def max_services_in_day(self, day_minutes: int, min_buffer: int = 0) -> int:
        """
        Máximo número de servicios que caben en un día.
        Usa los servicios más cortos primero (greedy).
        """
        sorted_durations = sorted(d for _, d in self.services)
        total = 0
        count = 0
        for d in sorted_durations:
            if total + d + (min_buffer if count > 0 else 0) <= day_minutes:
                total += d + (min_buffer if count > 0 else 0)
                count += 1
            else:
                break
        return count

    def schedule_permutations_count(self, available_minutes: int) -> int:
        """
        ¿Cuántas secuencias diferentes de servicios puedo agendar en
        un bloque de tiempo dado?

        Esto es: suma de permutaciones para todo k que quepa
        """
        max_k = self.max_services_in_day(available_minutes)
        return sum(perm(self.n, k) for k in range(1, max_k + 1))

    # ── ESTADÍSTICAS ──────────────────────────────────────────────────

    def summary(self) -> dict:
        """Resumen de cálculos combinatorios."""
        return {
            'total_services': self.n,
            'total_pairs': self.combinations(2),
            'total_triplets': self.combinations(3),
            'total_all_packages': self.total_packages(),
            'total_permutations_3': self.permutations(3),
            'max_in_6h_block': self.max_services_in_day(360),
            'max_in_8h_day': self.max_services_in_day(480),
        }
