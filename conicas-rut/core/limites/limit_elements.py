# conicas-rut/core/limites/limit_elements.py

"""
Construye campos, respuestas, pasos y filas para la vista de límites.
Separa la lógica de presentación desde TramoView.
"""


# ── Campos de respuesta de la interfaz ─────────────────────────────────────

def get_limit_answer_fields() -> list[tuple[str, str, bool]]:
    """Retorna los campos que debe mostrar la UI."""
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
    """Genera los valores que se revelan en los campos de la UI."""
    if not isinstance(analysis, dict):
        return {}

    return {
        "lim_izq": format_value(analysis.get("lim_izquierdo")),                  # límite lateral izquierdo
        "lim_der": format_value(analysis.get("lim_derecho")),                    # límite lateral derecho
        "concl_limite": analysis.get("conclusion_limite", "—"),                 # conclusión del límite
        "f_a": format_value(analysis.get("valor_en_punto"), undefined="No definido"),
        "concl_cont": analysis.get("conclusion_continuidad", "—"),              # conclusión de continuidad
        "tipo_disc": analysis.get("clasificacion_discontinuidad", "—"),         # tipo de discontinuidad
        "justif": analysis.get("justificacion", "—"),                          # justificación matemática
    }


# ── Tabla de valores ───────────────────────────────────────────────────────

def build_value_table_rows(analysis: dict) -> list[dict]:
    """Une las filas izquierda y derecha en una sola estructura para la tabla."""
    if not isinstance(analysis, dict):
        return []

    rows = []

    for row in analysis.get("tabla_izquierda", []):
        rows.append({
            "x": row.get("x"),                  # valor cercano a por izquierda
            "y": row.get("y"),                  # resultado de f(x)
            "lado": "◀ izq",                   # etiqueta visual del lado
            "separator_before": False,          # no separa antes de filas izquierdas
        })

    for index, row in enumerate(analysis.get("tabla_derecha", [])):
        rows.append({
            "x": row.get("x"),                  # valor cercano a por derecha
            "y": row.get("y"),                  # resultado de f(x)
            "lado": "der ▶",                   # etiqueta visual del lado
            "separator_before": index == 0,     # separa al comenzar el lado derecho
        })

    return rows


def build_table_rows(analysis: dict) -> list[dict]:
    """Alias de compatibilidad para código anterior."""
    return build_value_table_rows(analysis)


# ── Pasos y textos para la interfaz ────────────────────────────────────────

def build_limit_generation_steps(datos: dict, analysis: dict) -> list[dict]:
    """Combina pasos de generación de la función y desarrollo algebraico."""
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
    """Convierte una explicación larga en viñetas simples para la UI."""
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


# ── Formato de valores ────────────────────────────────────────────────────

def format_value(value, undefined="No definido") -> str:
    """Formatea números, infinitos simbólicos y valores indefinidos."""
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
    """Alias interno de compatibilidad."""
    return format_value(value, undefined)