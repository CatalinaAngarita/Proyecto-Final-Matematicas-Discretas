"""
Visualizador de Estadísticas
==============================
Genera gráficos de distribuciones binomiales y tendencias.

REQUIERE: matplotlib

Uso:
    plotter = StatsPlotter()
    plotter.plot_binomial_pmf(100, 0.15)
    plotter.plot_binomial_cdf(100, 0.15)
    plotter.plot_cancellation_trend(weeks, cancellations)
    plotter.save('output/')
"""
import os
from typing import List, Tuple


class StatsPlotter:
    """
    Genera visualizaciones de análisis estadístico.
    """

    def __init__(self, output_dir: str = None):
        self._matplotlib = None
        self._figures = []
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'output'
        )

    def _check_deps(self):
        try:
            import matplotlib.pyplot as plt
            self._matplotlib = plt
            return True
        except ImportError:
            return False

    def _ensure_output_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _ensure_latex_clean(self):
        """Evita errores con LaTeX si no está instalado."""
        plt = self._matplotlib
        if plt:
            try:
                plt.rcParams['text.usetex'] = False
            except Exception:
                pass

    def plot_binomial_pmf(self, n: int, p: float,
                           title: str = None,
                           highlight_k: int = None):
        """
        Gráfico de la función de masa de probabilidad binomial.

        Muestra P(X=k) para k = 0..n.
        """
        has_deps = self._check_deps()
        if not has_deps:
            print('[StatsPlotter] matplotlib no instalado. '
                  'Saltando PMF.')
            return

        plt = self._matplotlib
        self._ensure_latex_clean()

        from mathematics.binomial.cancellation_analysis import BinomialAnalysis
        ba = BinomialAnalysis(n, p)

        k_values = list(range(n + 1))
        probs = [ba.pmf(k) for k in k_values]

        fig, ax = plt.subplots(figsize=(12, 5))
        colors = ['#8B5E83' if highlight_k is None or k != highlight_k
                  else '#E8C35E' for k in k_values]
        ax.bar(k_values, probs, color=colors, alpha=0.8,
               edgecolor='white', linewidth=0.5)
        ax.set_xlabel('k (número de cancelaciones)', fontsize=11)
        ax.set_ylabel('P(X = k)', fontsize=11)
        ax.set_title(
            title or f'Distribución Binomial B({n}, {p})\n'
                     f'E[X]={ba.expected():.1f}, '
                     f'σ={ba.std_dev():.2f}',
            fontsize=13, fontweight='bold'
        )
        ax.grid(axis='y', alpha=0.3)

        if highlight_k is not None and 0 <= highlight_k <= n:
            ax.annotate(f'k={highlight_k}\np={probs[highlight_k]:.4f}',
                        xy=(highlight_k, probs[highlight_k]),
                        xytext=(highlight_k + 5, probs[highlight_k] + 0.02),
                        arrowprops=dict(arrowstyle='->', color='#E8C35E'),
                        fontsize=10, color='#E8C35E', fontweight='bold')

        self._figures.append(('binomial_pmf', fig))

    def plot_binomial_cdf(self, n: int, p: float,
                           title: str = None):
        """
        Gráfico de la función de distribución acumulada binomial.

        Muestra P(X ≤ k) para k = 0..n.
        """
        has_deps = self._check_deps()
        if not has_deps:
            print('[StatsPlotter] matplotlib no instalado. '
                  'Saltando CDF.')
            return

        plt = self._matplotlib
        self._ensure_latex_clean()

        from mathematics.binomial.cancellation_analysis import BinomialAnalysis
        ba = BinomialAnalysis(n, p)

        k_values = list(range(n + 1))
        cdf_values = [ba.cdf(k) for k in k_values]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.step(k_values, cdf_values, where='post',
                color='#5E8B6E', linewidth=2)
        ax.fill_between(k_values, cdf_values, step='post',
                        alpha=0.3, color='#5E8B6E')
        ax.axhline(y=0.95, color='#E8C35E', linestyle='--',
                   label='95%', alpha=0.7)
        ax.axhline(y=0.50, color='#8B5E83', linestyle='--',
                   label='50%', alpha=0.7)
        ax.set_xlabel('k (número de cancelaciones)', fontsize=11)
        ax.set_ylabel('P(X ≤ k)', fontsize=11)
        ax.set_title(
            title or f'Función de Distribución Acumulada - Binomial({n}, {p})',
            fontsize=13, fontweight='bold'
        )
        ax.legend()
        ax.grid(alpha=0.3)

        self._figures.append(('binomial_cdf', fig))

    def plot_cancellation_trend(self, weeks: List[str],
                                  cancellations: List[int],
                                  total_appointments: List[int],
                                  title: str = 'Tendencia de Cancelaciones'):
        """
        Gráfico de tendencia de cancelaciones por semana.

        Muestra:
        - Barras: cancelaciones por semana
        - Línea: tasa de cancelación (%)
        """
        has_deps = self._check_deps()
        if not has_deps:
            print('[StatsPlotter] matplotlib no instalado. '
                  'Saltando tendencia.')
            return

        plt = self._matplotlib
        self._ensure_latex_clean()

        rates = [
            (c / t * 100) if t > 0 else 0
            for c, t in zip(cancellations, total_appointments)
        ]

        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Barras de cancelaciones
        bars = ax1.bar(weeks, cancellations, color='#E74C3C',
                       alpha=0.7, label='Cancelaciones')
        for bar, val in zip(bars, cancellations):
            ax1.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.5, str(val),
                     ha='center', fontsize=9, fontweight='bold')

        ax1.set_xlabel('Semana', fontsize=11)
        ax1.set_ylabel('Cancelaciones', fontsize=11, color='#E74C3C')
        ax1.tick_params(axis='y', labelcolor='#E74C3C')

        ax2 = ax1.twinx()
        ax2.plot(weeks, rates, 'o-', color='#5E8B6E',
                 linewidth=2, label='Tasa (%)')
        ax2.set_ylabel('Tasa de cancelación (%)', fontsize=11,
                       color='#5E8B6E')
        ax2.tick_params(axis='y', labelcolor='#5E8B6E')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        plt.title(title, fontsize=13, fontweight='bold')
        fig.tight_layout()

        self._figures.append(('cancellation_trend', fig))

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
