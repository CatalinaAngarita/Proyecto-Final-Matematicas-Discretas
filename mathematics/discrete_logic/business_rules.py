"""
Reglas de Negocio como Lógica Proposicional
=============================================
Modela las reglas de negocio del spa como proposiciones lógicas.

Cada regla se expresa como: antecedente → consecuente
Si se cumple el antecedente, debe cumplirse el consecuente.

EJEMPLOS DE REGLAS:
1. Si el servicio es de uñas → debe especificarse el tipo de aplicación
2. Si la cita es en la mañana → debe terminar antes de las 12:00
3. Si la clienta es nueva → enviar mensaje de bienvenida
4. Si se cancela con < 2h de anticipación → marcar como última hora
"""
from typing import List, Tuple, Callable, Dict
from dataclasses import dataclass


@dataclass
class Rule:
    """Una regla de negocio como proposición lógica."""
    name: str
    antecedent: str
    consequent: str
    evaluate: Callable[[], bool]
    message: str


class BusinessRules:
    """
    Motor de reglas de negocio basado en lógica proposicional.

    Uso:
        rules = BusinessRules()
        rules.add_rule(
            'nail_type_required',
            'Servicio es de uñas',
            'Tipo de aplicación especificado',
            lambda: service_category == 'nail' and nail_type is not None,
            'Los servicios de uñas requieren especificar el tipo de aplicación'
        )
        results = rules.evaluate_all()
    """

    def __init__(self):
        self.rules: List[Rule] = []

    def add_rule(self, name: str, antecedent: str, consequent: str,
                 evaluate: Callable[[], bool], message: str):
        """
        Agrega una regla: antecedent → consequent

        La regla se cumple si evaluate() retorna True.
        """
        self.rules.append(Rule(name, antecedent, consequent, evaluate, message))

    def evaluate_all(self) -> List[Dict]:
        """Evalúa todas las reglas y retorna los resultados."""
        results = []
        for rule in self.rules:
            passed = rule.evaluate()
            results.append({
                'name': rule.name,
                'antecedent': rule.antecedent,
                'consequent': rule.consequent,
                'passed': passed,
                'message': rule.message if not passed else '',
                'status': '✅ Cumplida' if passed else '❌ Violada',
            })
        return results

    def rules_passed(self) -> int:
        """Número de reglas que se cumplen."""
        return sum(1 for r in self.evaluate_all() if r['passed'])

    def rules_failed(self) -> int:
        """Número de reglas violadas."""
        return sum(1 for r in self.evaluate_all() if not r['passed'])

    @staticmethod
    def truth_table(variables: List[str]) -> List[Dict[str, bool]]:
        """
        Genera una tabla de verdad para n variables booleanas.

        Aplicación: visualizar todas las combinaciones posibles
        de condiciones para verificar reglas.

        Ejemplo:
            truth_table(['mañana', 'ocupado', 'festivo'])
            → 2^3 = 8 filas
        """
        n = len(variables)
        table = []
        for i in range(2 ** n):
            row = {}
            for j, var in enumerate(variables):
                row[var] = bool((i >> (n - 1 - j)) & 1)
            table.append(row)
        return table

    @staticmethod
    def verify_tautology(expression: Callable[[bool, bool], bool],
                         p_label: str = 'P', q_label: str = 'Q') -> Tuple[bool, List]:
        """
        Verifica si una expresión es una TAUTOLOGÍA
        (verdadera para todas las combinaciones de valores de verdad).

        Aplicación: verificar que una regla de negocio
        no tenga contradicciones lógicas.
        """
        table = BusinessRules.truth_table([p_label, q_label])
        all_true = True
        results = []

        for row in table:
            result = expression(row[p_label], row[q_label])
            results.append({**row, 'result': result})
            if not result:
                all_true = False

        return all_true, results
