# conicas-rut/core/limites/limit_elements.py

"""
Construcción de campos y respuestas para la vista de límites.

Este módulo separa la lógica de respuestas desde TramoView.
La vista solo debería crear campos vacíos y luego revelar estos valores.
"""


def get_limit_answer_fields() -> list[tuple[str, str, bool]]:
    """
    Retorna los campos que debe mostrar la UI.

    """
    return [
        ("Límite izquierdo   lím(x→a⁻)", "lim_izq", False),
        ("Límite derecho     lím(x→a⁺)", "lim_der", False),
        ("Conclusión — existencia del límite", "concl_limite", False),
        ("Valor f(a)", "f_a", False),
        ("Conclusión — continuidad en x = a", "concl_cont", False),
        ("Tipo de discontinuidad", "tipo_disc", False),
        ("Justificación escrita", "justif", True),
    ]


def build_limit_answer_values(analysis: dict) -> dict:
    """
    Recibe el resultado de AnalizarLimites() y genera los valores
    que se revelan en los campos de la UI.
    """
    if not isinstance(analysis, dict):
        return {}

    return {
        "lim_izq": _fmt_value(analysis.get("lim_izquierdo")),
        "lim_der": _fmt_value(analysis.get("lim_derecho")),
        "concl_limite": analysis.get("conclusion_limite", "—"),
        "f_a": _fmt_value(
            analysis.get("valor_en_punto"),
            undefined="No definido",
        ),
        "concl_cont": analysis.get("conclusion_continuidad", "—"),
        "tipo_disc": analysis.get("clasificacion_discontinuidad", "—"),
        "justif": analysis.get("justificacion", "—"),
    }


def build_table_rows(analysis: dict) -> list[dict]:
    """
    Construye filas unificadas para tabla de valores.

    Retorna una lista:
    [
        {"x": ..., "y": ..., "lado": "◀ izq"},
        {"x": ..., "y": ..., "lado": "der ▶"},
    ]
    """
    if not isinstance(analysis, dict):
        return []

    izquierda = analysis.get("tabla_izquierda", [])
    derecha = analysis.get("tabla_derecha", [])

    rows = []

    for row in izquierda:
        rows.append({
            "x": row.get("x"),
            "y": row.get("y"),
            "lado": "◀ izq",
        })

    for row in derecha:
        rows.append({
            "x": row.get("x"),
            "y": row.get("y"),
            "lado": "der ▶",
        })

    return rows


def _fmt_value(value, undefined="No definido") -> str:
    if value is None:
        return undefined

    if isinstance(value, float):
        if value == int(value):
            return str(int(value))

        return f"{value:.3f}"

    return str(value)