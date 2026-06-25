# conicas-rut/core/limites/limit_elements.py

"""
Construcción de campos, respuestas, pasos y filas para la vista de límites.
Este módulo separa lógica de presentación desde TramoView.
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
    Genera los valores que se revelan en los campos de la UI.
    """
    if not isinstance(analysis, dict):
        return {}

    return {
        "lim_izq": format_value(analysis.get("lim_izquierdo")),
        "lim_der": format_value(analysis.get("lim_derecho")),
        "concl_limite": analysis.get("conclusion_limite", "—"),
        "f_a": format_value(analysis.get("valor_en_punto"), undefined="No definido"),
        "concl_cont": analysis.get("conclusion_continuidad", "—"),
        "tipo_disc": analysis.get("clasificacion_discontinuidad", "—"),
        "justif": analysis.get("justificacion", "—"),
    }


def build_value_table_rows(analysis: dict) -> list[dict]:
    """
    Construye filas unificadas para la tabla de valores.

    """
    if not isinstance(analysis, dict):
        return []

    rows = []

    for row in analysis.get("tabla_izquierda", []):
        rows.append({
            "x": row.get("x"),
            "y": row.get("y"),
            "lado": "◀ izq",
            "separator_before": False,
        })

    for index, row in enumerate(analysis.get("tabla_derecha", [])):
        rows.append({
            "x": row.get("x"),
            "y": row.get("y"),
            "lado": "der ▶",
            "separator_before": index == 0,
        })

    return rows


def build_table_rows(analysis: dict) -> list[dict]:
    """
    Alias de compatibilidad para código anterior.
    """
    return build_value_table_rows(analysis)


def build_limit_generation_steps(datos: dict, analysis: dict) -> list[dict]:
    """
    Combina pasos preliminares de generación y desarrollo algebraico.
    """
    if not isinstance(datos, dict) or not isinstance(analysis, dict):
        return []

    steps = []

    for index, text in enumerate(datos.get("pasos_preliminares", []), start=1):
        steps.append({
            "title": f"Paso {index}",
            "explanation": text,
        })

    steps.extend(analysis.get("desarrollo_algebraico", []))

    return steps


def build_rule_bullets(text: str) -> str:
    """
    Convierte una explicación larga en viñetas simples para la UI.
    """
    if not text:
        return "—"

    parts = []
    current = ""

    for char in text:
        current += char

        if char in [".", ";"]:
            cleaned = current.strip(" .;")
            if cleaned:
                parts.append(cleaned)
            current = ""

    cleaned = current.strip(" .;")
    if cleaned:
        parts.append(cleaned)

    if not parts:
        return text

    return "• " + "\n• ".join(parts)


def format_value(value, undefined="No definido") -> str:
    """
    Formatea valores numéricos, infinitos simbólicos y valores indefinidos.
    """
    if value is None:
        return undefined

    if isinstance(value, str):
        return value

    if isinstance(value, float):
        rounded = round(value, 3)

        if rounded == int(rounded):
            return str(int(rounded))

        return f"{rounded:.3f}"

    return str(value)


def _fmt_value(value, undefined="No definido") -> str:
    """
    Alias interno de compatibilidad.
    """
    return format_value(value, undefined)