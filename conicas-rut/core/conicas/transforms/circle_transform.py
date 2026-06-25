# conicas-rut/core/conicas/transforms/circle_transform.py

from core.utils.manual_math import round_value, sqrt_value, shift_text
from core.utils.result_models import build_success, build_error


def transform_circle(A, B, C, D, E) -> dict:
    """
    Transforma una circunferencia desde forma general a forma canónica.
    """
    steps = []

    try:
        A = round_value(A, 6)
        B = round_value(B, 6)
        C = round_value(C, 6)
        D = round_value(D, 6)
        E = round_value(E, 6)

        if A == 0 or B == 0:
            return build_error(
                error="No se puede transformar como circunferencia porque A o B es cero.",
                data={
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "E": E,
                },
            )

        if A != B:
            return build_error(
                error="No se puede transformar como circunferencia porque A y B son distintos.",
                data={
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "E": E,
                },
            )

        steps.append({
            "title": "Ecuación general",
            "explanation": "Se parte desde la forma Ax² + Ay² + Cx + Dy + E = 0.",
            "equation": f"{A}x² + {B}y² + {C}x + {D}y + {E} = 0",
        })

        h = -C / (2 * A)
        k = -D / (2 * A)

        steps.append({
            "title": "Centro de la circunferencia",
            "explanation": (
                "Para completar cuadrados se usan "
                "h = −C/(2A) y k = −D/(2A)."
            ),
            "equation": (
                f"h = −({C})/(2·{A}) = {round_value(h)} ; "
                f"k = −({D})/(2·{A}) = {round_value(k)}"
            ),
            "result": f"Centro = ({round_value(h)}, {round_value(k)})",
        })

        radius_squared = h**2 + k**2 - (E / A)

        steps.append({
            "title": "Radio al cuadrado",
            "explanation": "El radio se obtiene desde r² = h² + k² − E/A.",
            "equation": (
                f"r² = ({round_value(h)})² + ({round_value(k)})² − ({E}/{A}) "
                f"= {round_value(radius_squared)}"
            ),
            "result": f"r² = {round_value(radius_squared)}",
        })

        canonical_form = (
            f"({shift_text('x', h)})² + "
            f"({shift_text('y', k)})² = {round_value(radius_squared)}"
        )

        if radius_squared < 0:
            steps.append({
                "title": "Conclusión",
                "explanation": (
                    "Como r² < 0, no existe radio real. "
                    "La ecuación representa una circunferencia imaginaria."
                ),
            })

            return build_error(
                error=f"Circunferencia imaginaria: r² = {round_value(radius_squared)} < 0.",
                steps=steps,
                data={
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "E": E,
                    "center": (round_value(h), round_value(k)),
                    "h": round_value(h),
                    "k": round_value(k),
                    "radius": None,
                    "radius_squared": round_value(radius_squared),
                    "canonical_form": canonical_form,
                    "imaginary": True,
                    "degenerate": False,
                },
            )

        if radius_squared == 0:
            steps.append({
                "title": "Conclusión",
                "explanation": (
                    "Como r² = 0, la circunferencia se reduce a un único punto: "
                    "su centro."
                ),
            })

            return build_error(
                error="Circunferencia degenerada: r² = 0.",
                steps=steps,
                data={
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "E": E,
                    "center": (round_value(h), round_value(k)),
                    "h": round_value(h),
                    "k": round_value(k),
                    "radius": 0,
                    "radius_squared": 0,
                    "canonical_form": canonical_form,
                    "imaginary": False,
                    "degenerate": True,
                },
            )

        radius = sqrt_value(radius_squared)

        steps.append({
            "title": "Forma canónica",
            "explanation": "Se reemplazan centro y radio en la forma canónica.",
            "equation": canonical_form,
            "result": f"r = {round_value(radius)}",
        })

        return build_success(
            conic_type="circle",
            explanation="La circunferencia fue transformada a forma canónica.",
            steps=steps,
            data={
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
                "center": (round_value(h), round_value(k)),
                "h": round_value(h),
                "k": round_value(k),
                "radius": round_value(radius),
                "radius_squared": round_value(radius_squared),
                "canonical_form": canonical_form,
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as error:
        return build_error(
            error=f"Error al transformar circunferencia: {error}",
            steps=steps,
        )