# conicas-rut/core/conicas/transforms/general_transform.py

from core.conicas.coef_builder import ecuacion_a_texto
from core.utils.result_models import build_success, build_error


# ── Reconstrucción de forma general ────────────────────────────────────────
# Documenta el camino inverso:
# forma canónica → forma general original.

def transform_to_general(conic_type: str, transform_data: dict, coef_data: dict) -> dict:
    """Reconstruye o conserva la forma general desde los coeficientes originales."""
    if not isinstance(transform_data, dict):
        return build_error(
            error="Datos canónicos inválidos para reconstruir forma general."
        )

    if not isinstance(coef_data, dict):
        return build_error(
            error="Coeficientes inválidos para reconstruir forma general."
        )

    if transform_data.get("imaginary"):
        return build_success(
            conic_type=conic_type,
            explanation="La cónica es imaginaria; no se reconstruye una curva real.",
            steps=[
                {
                    "title": "Cónica imaginaria",
                    "explanation": (
                        "La forma canónica no representa puntos reales, "
                        "pero la ecuación general original se conserva."
                    ),
                    "equation": coef_data.get("equation_str", "—"),
                }
            ],
            data={
                "equation_str": coef_data.get("equation_str", "—"),
                "imaginary": True,
            },
        )

    if transform_data.get("degenerate"):
        return build_success(
            conic_type=conic_type,
            explanation="La cónica es degenerada; se conserva la ecuación general original.",
            steps=[
                {
                    "title": "Cónica degenerada",
                    "explanation": (
                        "La transformación canónica detectó un caso degenerado. "
                        "Se conserva la ecuación general original."
                    ),
                    "equation": coef_data.get("equation_str", "—"),
                }
            ],
            data={
                "equation_str": coef_data.get("equation_str", "—"),
                "degenerate": True,
            },
        )

    A = coef_data.get("A")
    B = coef_data.get("B")
    C = coef_data.get("C")
    D = coef_data.get("D")
    E = coef_data.get("E")

    A_frac = coef_data.get("A_frac")  # fracción exacta de A
    B_frac = coef_data.get("B_frac")  # fracción exacta de B

    if A_frac and B_frac:
        equation = ecuacion_a_texto(A_frac, B_frac, C, D, E)
    else:
        equation = coef_data.get(
            "equation_str",
            f"{A}x² + {B}y² + {C}x + {D}y + {E} = 0",
        )

    steps = [
        {
            "title": "Forma canónica",
            "explanation": "Se toma la forma canónica calculada previamente.",
            "equation": transform_data.get("canonical_form", "—"),
        },
        {
            "title": "Expansión conceptual",
            "explanation": (
                "Para volver a la forma general se expanden los cuadrados, "
                "se multiplican los denominadores y se agrupan términos semejantes."
            ),
        },
        {
            "title": "Forma general obtenida",
            "explanation": "La ecuación resultante coincide con los coeficientes generados desde el RUT.",
            "equation": equation,
        },
    ]

    return build_success(
        conic_type=conic_type,
        explanation="Se documentó la equivalencia entre forma canónica y forma general.",
        steps=steps,
        data={
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
            "equation_str": equation,  # forma general final
        },
    )