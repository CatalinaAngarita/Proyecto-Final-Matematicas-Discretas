"""
diana-nails-smart-booking — Módulo de Matemáticas Discretas
============================================================

Este módulo implementa conceptos de matemáticas discretas aplicados
al sistema de agendamiento del spa Diana Nails.

CONTENIDO:
- graphs/       → Teoría de grafos (NetworkX): relaciones clienta-servicio,
                  horarios, conflictos, BFS/DFS
- combinatorics/→ Combinatoria y permutaciones: paquetes de servicios,
                  ordenación de citas
- discrete_logic/→ Lógica proposicional: validación de restricciones,
                   detección de conflictos, reglas de negocio
- binomial/     → Distribución binomial: análisis de cancelaciones,
                  predicción de no-asistencias
- visualizations/→ Visualización con matplotlib de grafos y estadísticas
- run_examples.py → Script que ejecuta todos los ejemplos con datos reales

USO:
    from mathematics.graphs import ClientServiceGraph
    g = ClientServiceGraph()
    g.build()
    g.visualize()
"""
