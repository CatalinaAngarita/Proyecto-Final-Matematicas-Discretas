"""
Predictor de Cancelaciones
===========================
Usa la distribución binomial para predecir cancelaciones
y tomar decisiones de negocio.

APLICACIONES:
1. Predecir cancelaciones por día/semana/mes
2. Calcular overbooking seguro
3. Evaluar impacto de cambios en política de cancelación
4. Estimar ingresos esperados
"""
from typing import List, Dict, Tuple
from mathematics.binomial.cancellation_analysis import BinomialAnalysis


class CancellationPredictor:
    """
    Predictor de cancelaciones usando el modelo binomial.

    Uso:
        # Historial: 20 cancelaciones en 150 citas
        predictor = CancellationPredictor(historical_cancellations=20,
                                          historical_total=150)

        predictor.daily_prediction(avg_daily_citas=12)
        predictor.optimal_overbooking(slots=20, max_risk=0.10)
    """

    def __init__(self, historical_cancellations: int = 0,
                 historical_total: int = 0):
        """
        Args:
            historical_cancellations: Cancelaciones en el período histórico
            historical_total: Total de citas en el período histórico
        """
        self.cancellations = historical_cancellations
        self.total = historical_total
        self.p = historical_cancellations / historical_total if historical_total > 0 else 0.15

    @property
    def rate(self) -> float:
        """Tasa de cancelación estimada."""
        return self.p

    def daily_prediction(self, avg_daily_citas: int) -> BinomialAnalysis:
        """
        Predicción para un día típico.

        Aplicación: ¿cuántas cancelaciones esperar mañana?
        """
        return BinomialAnalysis(avg_daily_citas, self.p)

    def weekly_prediction(self, avg_weekly_citas: int) -> BinomialAnalysis:
        """Predicción semanal."""
        return BinomialAnalysis(avg_weekly_citas, self.p)

    def monthly_prediction(self, avg_monthly_citas: int) -> BinomialAnalysis:
        """Predicción mensual."""
        return BinomialAnalysis(avg_monthly_citas, self.p)

    def optimal_overbooking(self, slots: int, max_risk: float = 0.10) -> int:
        """
        Calcula el máximo número de slots extras (overbooking)
        que se pueden aceptar sin superar max_risk de que
        todas las citas se cumplan.

        Aplicación: si tengo 20 slots y acepto 3 extras,
        ¿qué tan probable es que vengan más de 20 clientes?

        Returns:
            Número máximo de slots adicionales
        """
        max_extras = 0
        for extra in range(1, slots + 1):
            ba = BinomialAnalysis(slots + extra, self.p)
            risk = ba.risk_of_overbooking(slots + extra, slots)
            if risk <= max_risk:
                max_extras = extra
            else:
                break
        return max_extras

    def revenue_with_overbooking(self, slots: int, price_per_service: float,
                                  max_risk: float = 0.10) -> Dict:
        """
        Calcula ingresos esperados con y sin overbooking.

        Returns:
            Dict con ingresos esperados, riesgo, y slots óptimos
        """
        extras = self.optimal_overbooking(slots, max_risk)
        total_booked = slots + extras
        ba = BinomialAnalysis(total_booked, self.p)

        expected_attend = total_booked - ba.expected()
        expected_revenue = expected_attend * price_per_service

        return {
            'slots_disponibles': slots,
            'slots_extras_recomendados': extras,
            'total_reservas': total_booked,
            'esperanza_asistentes': round(expected_attend, 1),
            'ingreso_esperado': round(expected_revenue, 2),
            'riesgo_overbooking': round(ba.risk_of_overbooking(total_booked, slots), 4),
        }

    def scenario_analysis(self, scenarios: List[Tuple[str, int, int]]) -> List[Dict]:
        """
        Analiza múltiples escenarios.
        Cada escenario: (nombre, slots, precio_servicio)

        Aplicación: comparar diferentes días de la semana
        (lunes menos slots, sábado más slots, etc.)
        """
        results = []
        for name, slots, price in scenarios:
            rev = self.revenue_with_overbooking(slots, price)
            rev['escenario'] = name
            results.append(rev)
        return results

    def improvement_impact(self, new_rate: float, avg_daily_citas: int) -> Dict:
        """
        Impacto de reducir la tasa de cancelación.

        Aplicación: si una campaña de recordatorio reduce
        cancelaciones de 15% a 10%, ¿cuánto mejora el ingreso?

        Args:
            new_rate: Nueva tasa de cancelación estimada
            avg_daily_citas: Promedio de citas por día
        """
        old = BinomialAnalysis(avg_daily_citas, self.p)
        new = BinomialAnalysis(avg_daily_citas, new_rate)

        return {
            'old_rate': self.p,
            'new_rate': new_rate,
            'change': round((self.p - new_rate) * 100, 1),
            'old_expected_cancellations': round(old.expected(), 2),
            'new_expected_cancellations': round(new.expected(), 2),
            'cancellations_saved': round(old.expected() - new.expected(), 2),
            'old_p_zero': round(old.pmf(0), 4),
            'new_p_zero': round(new.pmf(0), 4),
        }
