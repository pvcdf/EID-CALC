# conicas-rut/core/conicas/transforms/hyperbola_transform.py

from core.utils.manual_math import round_value, sqrt_value, shift_text
from core.utils.result_models import build_success, build_error


def transform_hyperbola(A, B, C, D, E) -> dict:
    """
    Transforma una hipérbola desde forma general a forma canónica.
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
                error="No se puede transformar como hipérbola porque A o B es cero.",
                data={
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "E": E,
                },
            )

        if A * B > 0:
            return build_error(
                error="No se puede transformar como hipérbola porque A y B no tienen signos opuestos.",
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
            "explanation": "Se parte desde Ax² + By² + Cx + Dy + E = 0.",
            "equation": f"{A}x² + {B}y² + {C}x + {D}y + {E} = 0",
        })

        h = -C / (2 * A)
        k = -D / (2 * B)

        steps.append({
            "title": "Centro de la hipérbola",
            "explanation": (
                "El centro se obtiene completando cuadrados: "
                "h = −C/(2A) y k = −D/(2B)."
            ),
            "equation": (
                f"h = −({C})/(2·{A}) = {round_value(h)} ; "
                f"k = −({D})/(2·{B}) = {round_value(k)}"
            ),
            "result": f"Centro = ({round_value(h)}, {round_value(k)})",
        })

        constant = A * h**2 + B * k**2 - E

        steps.append({
            "title": "Constante del lado derecho",
            "explanation": (
                "Luego de completar cuadrados se obtiene "
                "A(x−h)² + B(y−k)² = K."
            ),
            "equation": (
                f"K = {A}({round_value(h)})² + {B}({round_value(k)})² − ({E}) "
                f"= {round_value(constant)}"
            ),
            "result": f"K = {round_value(constant)}",
        })

        if constant == 0:
            return build_error(
                error="Hipérbola degenerada: K = 0.",
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
                    "constant": 0,
                    "imaginary": False,
                    "degenerate": True,
                },
            )

        x_denominator = constant / A
        y_denominator = constant / B

        if x_denominator > 0 and y_denominator < 0:
            orientation = "horizontal"
            a2 = x_denominator
            b2 = -y_denominator

            canonical_form = (
                f"({shift_text('x', h)})²/{round_value(a2)} − "
                f"({shift_text('y', k)})²/{round_value(b2)} = 1"
            )

        elif y_denominator > 0 and x_denominator < 0:
            orientation = "vertical"
            a2 = y_denominator
            b2 = -x_denominator

            canonical_form = (
                f"({shift_text('y', k)})²/{round_value(a2)} − "
                f"({shift_text('x', h)})²/{round_value(b2)} = 1"
            )

        else:
            return build_error(
                error="No se pudo normalizar la hipérbola: denominadores inválidos.",
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
                    "constant": round_value(constant),
                    "x_denominator": round_value(x_denominator),
                    "y_denominator": round_value(y_denominator),
                },
            )

        a = sqrt_value(a2)
        b = sqrt_value(b2)
        c = sqrt_value(a2 + b2)

        steps.append({
            "title": "Normalización",
            "explanation": (
                "Se divide por K y se identifica cuál término queda positivo. "
                "Ese término define la orientación de la hipérbola."
            ),
            "equation": (
                f"Denominador en x = {round_value(x_denominator)} ; "
                f"Denominador en y = {round_value(y_denominator)}"
            ),
            "result": f"Orientación: {orientation}",
        })

        steps.append({
            "title": "Parámetros de la hipérbola",
            "explanation": "En una hipérbola se cumple c² = a² + b².",
            "equation": (
                f"a² = {round_value(a2)} ; "
                f"b² = {round_value(b2)} ; "
                f"c² = {round_value(a2 + b2)}"
            ),
            "result": (
                f"a = {round_value(a)}, b = {round_value(b)}, "
                f"c = {round_value(c)}"
            ),
        })

        steps.append({
            "title": "Forma canónica",
            "explanation": "Se obtiene la ecuación canónica de la hipérbola.",
            "equation": canonical_form,
        })

        return build_success(
            conic_type="hyperbola",
            explanation="La hipérbola fue transformada a forma canónica.",
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
                "constant": round_value(constant),
                "x_denominator": round_value(x_denominator),
                "y_denominator": round_value(y_denominator),
                "a2": round_value(a2),
                "b2": round_value(b2),
                "a": round_value(a),
                "b": round_value(b),
                "c": round_value(c),
                "orientation": orientation,
                "canonical_form": canonical_form,
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as error:
        return build_error(
            error=f"Error al transformar hipérbola: {error}",
            steps=steps,
        )