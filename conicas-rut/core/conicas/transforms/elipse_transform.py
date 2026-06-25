# conicas-rut/core/conicas/transforms/elipse_transform.py

from core.utils.manual_math import round_value, sqrt_value, shift_text
from core.utils.result_models import build_success, build_error


def transform_ellipse(A, B, C, D, E) -> dict:
    """
    Transforma una elipse desde forma general a forma canónica.
    """
    steps = []

    try:
        A = round_value(A, 6)
        B = round_value(B, 6)
        C = round_value(C, 6)
        D = round_value(D, 6)
        E = round_value(E, 6)

        if A <= 0 or B <= 0:
            return build_error(
                error="No se puede transformar como elipse del proyecto porque A y B deben ser positivos.",
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
            "title": "Centro de la elipse",
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

        x_radius_squared = constant / A
        y_radius_squared = constant / B

        canonical_form = (
            f"({shift_text('x', h)})²/{round_value(x_radius_squared)} + "
            f"({shift_text('y', k)})²/{round_value(y_radius_squared)} = 1"
        )

        if constant < 0:
            steps.append({
                "title": "Conclusión",
                "explanation": (
                    "En este proyecto A y B son positivos para la elipse. "
                    "Si K < 0, los denominadores quedan negativos y no existen puntos reales."
                ),
            })

            return build_error(
                error=f"Elipse imaginaria: K = {round_value(constant)} < 0.",
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
                    "x_radius_squared": round_value(x_radius_squared),
                    "y_radius_squared": round_value(y_radius_squared),
                    "a": None,
                    "b": None,
                    "c": None,
                    "a2": round_value(x_radius_squared),
                    "b2": round_value(y_radius_squared),
                    "canonical_form": canonical_form,
                    "major_axis": None,
                    "imaginary": True,
                    "degenerate": False,
                },
            )

        if constant == 0:
            steps.append({
                "title": "Conclusión",
                "explanation": (
                    "Como K = 0, la elipse se reduce a un único punto. "
                    "Es una cónica degenerada."
                ),
            })

            return build_error(
                error="Elipse degenerada: K = 0.",
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
                    "x_radius_squared": 0,
                    "y_radius_squared": 0,
                    "a": 0,
                    "b": 0,
                    "c": 0,
                    "a2": 0,
                    "b2": 0,
                    "canonical_form": (
                        f"{A}({shift_text('x', h)})² + "
                        f"{B}({shift_text('y', k)})² = 0"
                    ),
                    "major_axis": None,
                    "imaginary": False,
                    "degenerate": True,
                },
            )

        if x_radius_squared >= y_radius_squared:
            major_axis = "horizontal"
            semi_major_squared = x_radius_squared
            semi_minor_squared = y_radius_squared
        else:
            major_axis = "vertical"
            semi_major_squared = y_radius_squared
            semi_minor_squared = x_radius_squared

        a = sqrt_value(semi_major_squared)
        b = sqrt_value(semi_minor_squared)
        c = sqrt_value(semi_major_squared - semi_minor_squared)

        steps.append({
            "title": "Denominadores de la forma canónica",
            "explanation": (
                "Se divide la ecuación por K para obtener denominadores "
                "en x e y."
            ),
            "equation": (
                f"rx² = K/A = {round_value(x_radius_squared)} ; "
                f"ry² = K/B = {round_value(y_radius_squared)}"
            ),
        })

        steps.append({
            "title": "Semiejes y focos",
            "explanation": (
                "En una elipse, a² es el mayor denominador, b² el menor, "
                "y c² = a² − b²."
            ),
            "equation": (
                f"a² = {round_value(semi_major_squared)} ; "
                f"b² = {round_value(semi_minor_squared)} ; "
                f"c² = {round_value(semi_major_squared - semi_minor_squared)}"
            ),
            "result": (
                f"a = {round_value(a)}, b = {round_value(b)}, "
                f"c = {round_value(c)}"
            ),
        })

        steps.append({
            "title": "Forma canónica",
            "explanation": "Se obtiene la ecuación canónica de la elipse.",
            "equation": canonical_form,
            "result": f"Eje mayor: {major_axis}",
        })

        return build_success(
            conic_type="ellipse",
            explanation="La elipse fue transformada a forma canónica.",
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
                "x_radius_squared": round_value(x_radius_squared),
                "y_radius_squared": round_value(y_radius_squared),
                "semi_major_squared": round_value(semi_major_squared),
                "semi_minor_squared": round_value(semi_minor_squared),
                "a2": round_value(semi_major_squared),
                "b2": round_value(semi_minor_squared),
                "a": round_value(a),
                "b": round_value(b),
                "c": round_value(c),
                "canonical_form": canonical_form,
                "major_axis": major_axis,
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as error:
        return build_error(
            error=f"Error al transformar elipse: {error}",
            steps=steps,
        )