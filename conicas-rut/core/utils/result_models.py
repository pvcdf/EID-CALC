# conicas-rut/core/utils/result_models.py

"""
Estructura estándar para respuestas internas del sistema.

Formato base:
{
    "valid"      : bool,
    "error"      : str | None,
    "conic_type" : str | None,
    "explanation": str,
    "steps"      : list,
    "data"       : dict,
}
"""

CONIC_NAMES_ES: dict[str, str] = {
    "circle": "Circunferencia",
    "ellipse": "Elipse",
    "hyperbola": "Hipérbola",
    "parabola": "Parábola",
}


# ── Nombres de cónicas ────────────────────────────────────────────────────

def conic_name_es(conic_type: str | None) -> str:
    """Retorna el nombre en español del tipo de cónica."""
    if not conic_type:
        return "Desconocido"

    return CONIC_NAMES_ES.get(conic_type, conic_type)


# ── Constructores de respuesta ────────────────────────────────────────────

def build_success(
    conic_type: str | None = None,
    explanation: str | None = None,
    steps: list | None = None,
    data: dict | None = None,
) -> dict:
    """Construye una respuesta exitosa con estructura estándar."""
    return {
        "valid": True,
        "error": None,
        "conic_type": conic_type,
        "explanation": explanation or "",
        "steps": steps if steps is not None else [],
        "data": data if data is not None else {},
    }


def build_error(
    error: str,
    steps: list | None = None,
    data: dict | None = None,
) -> dict:
    """Construye una respuesta de error con estructura estándar."""
    return {
        "valid": False,
        "error": error,
        "conic_type": None,
        "explanation": None,
        "steps": steps if steps is not None else [],
        "data": data if data is not None else {},
    }