"""
Análisis de Cancelaciones (Distribución Binomial)
==================================================
Modela cancelaciones como experimentos binomiales.

FUNDAMENTO MATEMÁTICO:

Cada cita es un ensayo de Bernoulli:
- Éxito (X=1): la cita se cancela
- Fracaso (X=0): la cita se cumple

X ~ Binomial(n, p) donde:
- n = número total de citas
- p = probabilidad de cancelación

FUNCIONES:
1. PMF: P(X = k) = C(n,k) * p^k * (1-p)^(n-k)
   Probabilidad de exactamente k cancelaciones

2. CDF: P(X ≤ k)
   Probabilidad de k o menos cancelaciones

3. Esperanza: E[X] = n * p
   Número esperado de cancelaciones

4. Varianza: Var(X) = n * p * (1-p)
   Dispersión de las cancelaciones

5. Desviación estándar: σ = √(n * p * (1-p))

APLICACIONES EN EL NEGOCIO:
- Predecir cuántas cancelaciones esperar por día/semana
- Calcular sobrecupos necesarios (overbooking)
- Evaluar si un cambio de política reduce cancelaciones
"""
from math import comb
from typing import Tuple, List
import statistics


def factorial(n: int) -> int:
    """n! = n * (n-1) * ... * 1"""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


class BinomialAnalysis:
    """
    Análisis binomial para cancelaciones de citas.

    Uso:
        ba = BinomialAnalysis(n=100, p=0.15)
        ba.pmf(10)       # P(exactamente 10 cancelaciones)
        ba.cdf(20)       # P(a lo sumo 20 cancelaciones)
        ba.expected()    # E[X] = 15
        ba.variance()    # Var(X) = 12.75
    """

    def __init__(self, n: int, p: float):
        """
        Args:
            n: Número de citas (ensayos)
            p: Probabilidad de cancelación (0 ≤ p ≤ 1)
        """
        self.n = n
        self.p = p
        self.q = 1.0 - p

    def pmf(self, k: int) -> float:
        """
        P(X = k) = C(n,k) * p^k * q^(n-k)

        Probabilidad de exactamente k cancelaciones en n citas.
        """
        if k < 0 or k > self.n:
            return 0.0
        return comb(self.n, k) * (self.p ** k) * (self.q ** (self.n - k))

    def cdf(self, k: int) -> float:
        """
        P(X ≤ k) = Σ_{i=0}^{k} PMF(i)

        Probabilidad de k o menos cancelaciones.
        """
        if k < 0:
            return 0.0
        if k >= self.n:
            return 1.0
        return sum(self.pmf(i) for i in range(0, k + 1))

    def sf(self, k: int) -> float:
        """
        P(X > k) = 1 - CDF(k)

        Probabilidad de más de k cancelaciones.
        """
        return 1.0 - self.cdf(k)

    def expected(self) -> float:
        """
        E[X] = n * p

        Número esperado de cancelaciones.
        Aplicación: estimar pérdida de ingresos por cancelaciones.
        """
        return self.n * self.p

    def variance(self) -> float:
        """
        Var(X) = n * p * q = n * p * (1-p)

        Mide la dispersión de las cancelaciones.
        """
        return self.n * self.p * self.q

    def std_dev(self) -> float:
        """σ = √Var(X)"""
        return self.variance() ** 0.5

    def skewness(self) -> float:
        """
        Coeficiente de asimetría (sesgo):
        (q - p) / √(n * p * q)

        - p < 0.5: sesgo positivo (cola a la derecha)
        - p = 0.5: simétrico
        - p > 0.5: sesgo negativo (cola a la izquierda)

        Aplicación: entender la forma de la distribución
        para calcular percentiles.
        """
        return (self.q - self.p) / (self.variance() ** 0.5)

    def most_probable_outcome(self) -> Tuple[int, float]:
        """
        Moda: el valor de k con mayor probabilidad.
        ⌊(n+1) * p⌋ o ⌈(n+1) * p - 1⌉

        Aplicación: el número de cancelaciones MÁS PROBABLE.
        """
        k = int((self.n + 1) * self.p)
        if self.p == 0:
            return (0, 1.0)
        if self.p == 1:
            return (self.n, 1.0)
        return (k, self.pmf(k))

    def confidence_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """
        Intervalo de confianza aproximado (Wald):
        p̂ ± z * √(p̂ * q̂ / n)

        Aplicación: rango dentro del cual caen las cancelaciones
        con nivel de confianza dado.
        """
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)

        margin = z * ((self.p * self.q) / self.n) ** 0.5
        return (self.p - margin, self.p + margin)

    def risk_of_overbooking(self, booked_slots: int, available_slots: int) -> float:
        """
        Riesgo de overbooking:
        P(no-shows > available_slots) = P(X > available_slots)

        Aplicación: si tengo 20 slots pero acepto 22 reservas,
        ¿qué probabilidad hay de que vengan más de 20?
        """
        if booked_slots <= available_slots:
            return 0.0

        # Necesitamos n = available_slots, calcular probabilidad
        # de que los no-shows superen los slots extra
        no_shows_needed = booked_slots - available_slots
        return self.sf(no_shows_needed)

    def summary(self) -> dict:
        """Resumen completo del análisis binomial."""
        mode_k, mode_p = self.most_probable_outcome()
        return {
            'n': self.n,
            'p': self.p,
            'expected_cancellations': round(self.expected(), 2),
            'variance': round(self.variance(), 2),
            'std_dev': round(self.std_dev(), 2),
            'skewness': round(self.skewness(), 3),
            'most_probable_cancellations': mode_k,
            'probability_of_most_probable': round(mode_p, 4),
            'p_at_least_half': round(self.cdf(self.n // 2), 4),
            'p_zero_cancellations': round(self.pmf(0), 4),
            'ci_95': [round(x, 4) for x in self.confidence_interval(0.95)],
        }
