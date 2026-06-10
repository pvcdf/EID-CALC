# conicas-rut/core/result_models.py 

"""

{
    "valid"      : bool           True si el módulo terminó sin errores
    "error"      : str | None     Mensaje de error si valid = False
    "conic_type" : str | None     'circle' | 'ellipse' | 'hyperbola' | 'parabola'
    "explanation": str            Explicación legible del resultado
    "steps"      : list[str]      Pasos matemáticos para imprimir en consola/UI
    "data"       : dict           Datos específicos del módulo (ver cada módulo)
}
"""

"""
la funcion de este diccionario es mapear los nombres de las conicas a su traduccion en español, para mostrarlo en la interfaz
ya que al trabajar con los nombres en español directamente pueden ocurrir errores por las tildes, codificacion, mayusculas etc.
"""
CONIC_NAMES_ES: dict[str, str] = {
    "circle":    "Circunferencia",
    "ellipse":   "Elipse",
    "hyperbola": "Hipérbola",
    "parabola":  "Parábola",
}


def conic_name_es(conic_type: str) -> str:
    """Retorna el nombre en español del tipo de cónica."""
    return CONIC_NAMES_ES.get(conic_type, conic_type or "Desconocido")


# ── Constructores ───────────────────────────────────────────────────────────

def build_success(
    conic_type:  str  = None,
    explanation: str  = None,
    steps:       list = None,
    data:        dict = None,
) -> dict:
    """
    Construye un resultado exitoso con estructura estándar.
    """
    return {
        "valid":       True,
        "error":       None,
        "conic_type":  conic_type,
        "explanation": explanation or "",
        "steps":       steps or [],
        "data":        data or {},
    }


def build_error(
    error: str,
    steps: list = None,
    data:  dict = None,
) -> dict:
    """
    Construye un resultado de error con estructura estándar.

    """
    return {
        "valid":       False,
        "error":       error,
        "conic_type":  None,
        "explanation": None,
        "steps":       steps or [],
        "data":        data or {},
    }