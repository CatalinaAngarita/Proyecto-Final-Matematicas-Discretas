#!/usr/bin/env python
"""
Ejemplos completos de Matemáticas Discretas aplicadas al booking system.
========================================================================
Ejecuta: python run_examples.py

Genera figuras en mathematics/output/ (si matplotlib está instalado)
y muestra resultados por consola.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def separator(title: str):
    print()
    print('=' * 70)
    print(f'  {title}')
    print('=' * 70)


# ── COMBINATORIA ───────────────────────────────────────────────────────

def run_combinatorics():
    separator('COMBINATORIA: Combinaciones de Servicios')

    from mathematics.combinatorics.service_combinations import ServiceCombinations

    sc = ServiceCombinations()
    sc.add_services_batch([
        ('Manicura Básica', 30),
        ('Manicura Gel', 45),
        ('Pedicura Básica', 30),
        ('Pedicura Gel', 45),
        ('Uñas Acrílicas', 120),
        ('Uñas Press-on', 60),
        ('Nail Art', 90),
        ('Cejas (Depilación)', 15),
        ('Cejas (Diseño)', 30),
        ('Lifting de Pestañas', 45),
        ('Pestañas POSTIZAS', 60),
        ('Depilación Facial', 20),
        ('Depilación Corporal', 45),
        ('Mascarilla Facial', 30),
        ('Masaje Relajante', 60),
        ('Masaje Descontracturante', 60),
        ('Exfoliación Corporal', 40),
        ('Envoltura de Algas', 50),
        ('Aromaterapia', 45),
        ('Hidratación Profunda', 40),
    ])

    print(f'\n  Total de servicios disponibles: {sc.n}')
    print(f'  Pares de servicios C({sc.n}, 2) = {sc.combinations(2)}')
    print(f'  Tripletas C({sc.n}, 3) = {sc.combinations(3)}')
    print(f'  Paquetes de 4 C({sc.n}, 4) = {sc.combinations(4)}')
    print(f'  Total paquetes posibles: {sc.total_packages()}')
    print(f'  Formas de ordenar 5 servicios: {sc.permutations(5)}')

    # Paquetes que caben en 3h (180 min)
    print(f'\n  Paquetes de 2 servicios en ≤ 180 min:')
    for combo, dur in sc.package_durations(2):
        if dur <= 180:
            print(f'    {combo}: {dur} min')
    print(f'\n  Máximo de servicios en bloque de 4h: {sc.max_services_in_day(240)}')
    print(f'\n  Resumen:')
    for k, v in sc.summary().items():
        print(f'    {k}: {v}')

    separator('COMBINATORIA: Arreglos de Horarios')

    from mathematics.combinatorics.schedule_arrangements import ScheduleArrangements

    sa = ScheduleArrangements(total_slots=16, total_appointments=5)
    print(f'\n  Slots en el día: {sa.slots}')
    print(f'  Citas a agendar: {sa.appointments}')
    print(f'  Arreglos posibles P({sa.slots},{sa.appointments}) = {sa.arrangements()}')
    print(f'  Arreglos con repetición {sa.slots}^{sa.appointments} = {sa.arrangements_with_repetition()}')
    print(f'  Probabilidad de conflicto (asignación aleatoria): {sa.conflict_probability():.4f}')

    min_p, conflict = sa.pigeonhole_principle()
    print(f'  Principio del palomar: mínimo {min_p} cita(s) por slot, '
          f'conflictos inevitables: {conflict}')

    # Más citas que slots - conflicto inevitable
    sa2 = ScheduleArrangements(total_slots=8, total_appointments=12)
    print(f'\n  --- Con 12 citas y 8 slots ---')
    min_p2, conflict2 = sa2.pigeonhole_principle()
    print(f'  Principio del palomar: mínimo {min_p2} cita(s) por slot, '
          f'conflictos inevitables: {conflict2}')

    print(f'\n  Crecimiento factorial (10! = {__import__("math").factorial(10):,})')
    print(f'  Búsqueda por fuerza bruta para n=12: '
          f'{"factible" if __import__("math").factorial(12) <= 1_000_000 else "inviable"}')
    print(f'  15! = {__import__("math").factorial(15):,} combinaciones → inviable')


# ── LÓGICA DISCRETA ───────────────────────────────────────────────────

def run_discrete_logic():
    separator('LÓGICA DISCRETA: Validación de Restricciones')

    from mathematics.discrete_logic.constraints import ConstraintValidator
    from datetime import date, time, datetime, timedelta

    v = ConstraintValidator()

    # Simular datos de una cita
    tomorrow = date.today() + timedelta(days=1)
    now = datetime.now()

    v.add_required_time_range(
        start=time(9, 0),
        end=time(10, 0),
        morning_end=time(12, 0),
        afternoon_start=time(13, 0),
        afternoon_end=time(20, 0),
    )
    v.add_conflict_check(has_conflict=False)
    v.add_day_off_check(is_day_off=False)
    v.add_max_duration_check(duration=60, max_duration=180)
    v.add_future_date_check(cita_date=tomorrow, today=date.today())
    v.add_minimum_notice_check(
        cita_datetime=datetime.combine(tomorrow, time(9, 0)),
        now=now,
        min_hours=2,
    )

    result = v.validate()
    print(f'\n  Cita: mañana a las 9:00 (duración: 60 min)')
    print(f'  Válida: {result.is_valid}')
    print(f'  Restricciones cumplidas: {len(result.passed)}')
    print(f'  Restricciones fallidas: {len(result.failed)}')
    if result.failed:
        for name, msg in result.failed:
            print(f'    ❌ {name}: {msg}')

    # Ahora probar una cita inválida - conflicto
    print(f'\n  --- Cita con CONFLICTO ---')
    v2 = ConstraintValidator()
    v2.add_required_time_range(
        start=time(9, 0), end=time(10, 0),
        morning_end=time(12, 0),
        afternoon_start=time(13, 0), afternoon_end=time(20, 0),
    )
    v2.add_conflict_check(has_conflict=True)
    v2.add_day_off_check(is_day_off=False)
    v2.add_max_duration_check(duration=60, max_duration=180)
    v2.add_future_date_check(cita_date=tomorrow, today=date.today())
    v2.add_minimum_notice_check(
        cita_datetime=datetime.combine(tomorrow, time(9, 0)),
        now=now, min_hours=2,
    )

    result2 = v2.validate()
    print(f'  Válida: {result2.is_valid}')
    for name, msg in result2.failed:
        print(f'    ❌ {name}: {msg}')

    separator('LÓGICA DISCRETA: Reglas de Negocio')

    from mathematics.discrete_logic.business_rules import BusinessRules

    rules = BusinessRules()

    rules.add_rule(
        'nail_type_required',
        'Servicio es de uñas',
        'Tipo de aplicación especificado',
        lambda: True,  # Simulación: sí se especificó
        'Servicios de uñas requieren tipo de aplicación'
    )
    rules.add_rule(
        'within_hours',
        'Cita en horario laboral',
        'Horario válido',
        lambda: True,  # Simulación: está en horario laboral
        'La cita debe estar entre 8-12 o 13-20'
    )
    rules.add_rule(
        'min_notice',
        'Cita con 2h+ anticipación',
        'Anticipación suficiente',
        lambda: True,
        'Las citas requieren 2+ horas de anticipación'
    )
    rules.add_rule(
        'no_double_booking',
        'Especialista disponible',
        'Sin conflicto de horario',
        lambda: False,  # Simulación: CONFLICTO
        'La especialista ya tiene una cita en este horario'
    )
    rules.add_rule(
        'max_per_day',
        'Límite de citas por día',
        'Menos de 20 citas en el día',
        lambda: True,
        'La especialista no puede tomar más de 20 citas al día'
    )

    results = rules.evaluate_all()
    print(f'\n  Reglas cumplidas: {rules.rules_passed()}/{len(results)}')
    for r in results:
        print(f'  {r["status"]} → {r["name"]}: {r["antecedent"]} ⇒ {r["consequent"]}')
        if not r['passed']:
            print(f'           {r["message"]}')

    separator('LÓGICA DISCRETA: Tabla de Verdad')

    print(f'\n  Tabla de verdad: 2 variables (P, Q)')

    table = BusinessRules.truth_table(['P', 'Q'])
    print(f'  {"P":<8} {"Q":<8} {"P∧Q":<8} {"P∨Q":<8} {"P→Q":<8} {"P↔Q":<8}')
    print(f'  {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*8}')
    for row in table:
        p, q = row['P'], row['Q']
        conj = p and q
        disj = p or q
        imp = not p or q
        bic = (p and q) or (not p and not q)
        print(f'  {str(p):<8} {str(q):<8} {str(conj):<8} {str(disj):<8} {str(imp):<8} {str(bic):<8}')

    separator('LÓGICA DISCRETA: Detector de Conflictos')

    from mathematics.discrete_logic.conflict_detector import ConflictDetector
    from datetime import time

    cd = ConflictDetector()
    cd.add_appointment('A001', time(9, 0), time(10, 0))
    cd.add_appointment('A002', time(9, 30), time(10, 30))
    cd.add_appointment('A003', time(10, 30), time(11, 30))
    cd.add_appointment('A004', time(11, 0), time(12, 0))
    cd.add_appointment('A005', time(14, 0), time(15, 0))

    print(f'\n  Agenda del día:')
    for id_, interval in cd.appointments.items():
        print(f'    {id_}: {interval.start} - {interval.end}')

    conflicts = cd.find_conflicts()
    print(f'\n  Conflictos detectados: {len(conflicts)}')
    for c in conflicts:
        print(f'    ⚠ {c["appointment_a"]} ∩ {c["appointment_b"]} '
              f'→ {c["overlap_minutes"]} min de solapamiento')

    report = cd.conflict_report()
    print(f'\n  Reporte de conflictos:')
    for k, v in report.items():
        print(f'    {k}: {v}')

    print(f'\n  ¿Se puede agendar 10:00-11:00?')
    can, reasons = cd.can_schedule(time(10, 0), time(11, 0))
    print(f'    {"SÍ" if can else "NO"}')
    if reasons:
        print(f'    Conflictos con: {", ".join(reasons)}')

    print(f'\n  Bloques disponibles (≥ 30 min):')
    available = cd.find_available_blocks(time(8, 0), time(20, 0), 30)
    for start, end in available:
        dur = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
        print(f'    {start} - {end} ({dur} min)')


# ── DISTRIBUCIÓN BINOMIAL ─────────────────────────────────────────────

def run_binomial():
    separator('DISTRIBUCIÓN BINOMIAL: Análisis de Cancelaciones')

    from mathematics.binomial.cancellation_analysis import BinomialAnalysis

    # Escenario típico: tasa de cancelación 15%
    ba = BinomialAnalysis(n=100, p=0.15)
    summary = ba.summary()

    print(f'\n  Análisis binomial B(n=100, p=0.15):')
    for k, v in summary.items():
        print(f'    {k}: {v}')

    print(f'\n  --- Probabilidades específicas ---')
    for k in [0, 5, 10, 15, 20, 25, 30]:
        print(f'    P(X = {k:>2}) = {ba.pmf(k):.4f}  |  P(X ≤ {k:>2}) = {ba.cdf(k):.4f}')

    print(f'\n  --- Intervalos de confianza ---')
    for conf in [0.90, 0.95, 0.99]:
        lo, hi = ba.confidence_interval(conf)
        print(f'    IC al {conf*100:.0f}%: [{lo:.4f}, {hi:.4f}]')

    print(f'\n  --- Riesgo de overbooking ---')
    ba_ob = BinomialAnalysis(n=20, p=0.15)
    for extra in range(1, 6):
        risk = ba_ob.risk_of_overbooking(20 + extra, 20)
        print(f'    20 slots + {extra} extra: riesgo = {risk:.4f} ({risk*100:.1f}%)')

    separator('DISTRIBUCIÓN BINOMIAL: Predicción de Cancelaciones')

    from mathematics.binomial.cancellation_predictor import CancellationPredictor

    # Historial: 45 cancelaciones en 300 citas
    predictor = CancellationPredictor(historical_cancellations=45,
                                       historical_total=300)

    print(f'\n  Tasa de cancelación histórica: {predictor.rate:.2%}')

    # Predicción diaria
    daily = predictor.daily_prediction(avg_daily_citas=12)
    print(f'\n  Predicción diaria (12 citas):')
    print(f'    Cancelaciones esperadas: {daily.expected():.1f}')
    print(f'    P(0 cancelaciones): {daily.pmf(0):.4f}')
    print(f'    P(≤ 3 cancelaciones): {daily.cdf(3):.4f}')

    # Overbooking óptimo
    ob = predictor.optimal_overbooking(slots=20, max_risk=0.10)
    print(f'\n  Overbooking óptimo:')
    print(f'    Slots disponibles: 20')
    print(f'    Extras recomendados: {ob}')
    print(f'    Total a vender: {20 + ob}')

    rev = predictor.revenue_with_overbooking(slots=20, price_per_service=45000,
                                              max_risk=0.10)
    print(f'\n  Ingreso con overbooking:')
    for k, v in rev.items():
        print(f'    {k}: {v}')

    # Escenarios por día de la semana
    scenarios = [
        ('Lunes (baja)', 10, 45000),
        ('Martes (media)', 14, 45000),
        ('Miércoles (media)', 16, 45000),
        ('Jueves (alta)', 18, 45000),
        ('Viernes (alta)', 20, 45000),
        ('Sábado (máxima)', 24, 50000),
    ]

    print(f'\n  --- Análisis de escenarios por día ---')
    for s in predictor.scenario_analysis(scenarios):
        print(f'    {s["escenario"]}:')
        print(f'      Slots: {s["slots_disponibles"]}, '
              f'Extras: {s["slots_extras_recomendados"]}')
        print(f'      Ingreso esperado: ${s["ingreso_esperado"]:,.0f}')

    # Impacto de mejora
    impact = predictor.improvement_impact(new_rate=0.10,
                                           avg_daily_citas=12)
    print(f'\n  --- Impacto de reducir tasa de 15% → 10% ---')
    for k, v in impact.items():
        if isinstance(v, float):
            print(f'    {k}: {v:.4f}')
        else:
            print(f'    {k}: {v}')


# ── VISUALIZACIONES ───────────────────────────────────────────────────

def run_visualizations():
    separator('VISUALIZACIONES')

    from mathematics.visualizations.graph_plotter import GraphPlotter
    from mathematics.visualizations.stats_plotter import StatsPlotter

    print('\n  Generando gráficos...')
    gp = GraphPlotter()

    # Bipartite graph
    clients = ['Ana', 'Betty', 'Carol', 'Diana', 'Emily', 'Fernanda']
    services = ['Manicura', 'Pedicura', 'Acrílicas', 'Cejas',
                'Pestañas', 'Masaje', 'Facial']
    edges = [
        (0, 0), (0, 1), (0, 3), (1, 1), (1, 2), (1, 5),
        (2, 0), (2, 4), (2, 6), (3, 2), (3, 3), (3, 5),
        (4, 4), (4, 6), (5, 0), (5, 1), (5, 5),
    ]
    gp.plot_bipartite(clients, services, edges)

    # Conflict graph
    from datetime import time
    intervals = [
        ('A001', time(9, 0), time(10, 0)),
        ('A002', time(9, 30), time(10, 30)),
        ('A003', time(10, 0), time(11, 0)),
        ('A004', time(11, 0), time(12, 0)),
        ('A005', time(11, 30), time(12, 30)),
        ('A006', time(14, 0), time(15, 0)),
        ('A007', time(14, 30), time(15, 30)),
    ]
    gp.plot_conflict_graph(intervals)

    sp = StatsPlotter()

    # Binomial PMF
    sp.plot_binomial_pmf(n=100, p=0.15, highlight_k=15)

    # Binomial CDF
    sp.plot_binomial_cdf(n=100, p=0.15)

    # Cancellation trend
    weeks = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4',
             'Sem 5', 'Sem 6', 'Sem 7', 'Sem 8']
    cancellations = [3, 5, 2, 7, 4, 6, 3, 5]
    totals = [20, 25, 22, 30, 28, 26, 24, 27]
    sp.plot_cancellation_trend(weeks, cancellations, totals)

    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'output'
    )
    gp.save(output_dir)
    sp.save(output_dir)
    print(f'\n  Figuras guardadas en: {output_dir}/')


# ── MAIN ──────────────────────────────────────────────────────────────

def main():
    print()
    print('╔══════════════════════════════════════════════════════════╗')
    print('║   MATEMÁTICAS DISCRETAS - Intelligent Booking System    ║')
    print('║              Diana Nails Spa - 3er Corte                ║')
    print('╚══════════════════════════════════════════════════════════╝')

    run_combinatorics()
    run_discrete_logic()
    run_binomial()
    run_visualizations()

    separator('FIN')
    print('\n  Todos los ejemplos ejecutados correctamente.')
    print('  Revisa mathematics/output/ para las figuras.\n')


if __name__ == '__main__':
    main()
