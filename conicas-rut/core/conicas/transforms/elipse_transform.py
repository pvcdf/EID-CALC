# conicas-rut/core/conicas/transforms/elipse_transform.py

from core.utils.result_models import build_success, build_error

#helpers internos para no repetir lógica en cada transform.
def _r(value: float, digits: int = 4) -> float:
    return round(value, digits)

#Redondea valores para mostrar en pasos, canónicas y data
def _sqrt(value: float) -> float:
    return value ** 0.5

#Calcula raíz cuadrada sin math.sqrt
def _shift(variable: str, value: float) -> str:
    value = _r(value)

    if value == 0:
        return variable

    if value > 0:
        return f"{variable} − {value}"

    return f"{variable} + {_r(-value)}"


def transform_ellipse(A, B, C, D, E):
    steps: list[dict] = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        if A == 0 or B == 0:
            return build_error(
                error="No se puede transformar como elipse porque A o B es cero.",
                steps=steps,
            )

        steps.append({
            "title": "Agrupar términos cuadráticos",
            "explanation": "Se separan los grupos en x e y para completar cuadrados.",
            "equation": f"({A})x² + ({C})x + ({B})y² + ({D})y + {E} = 0",
        })

        h = -C / (2 * A)
        k = -D / (2 * B)

        steps.append({
            "title": "Completar cuadrado en x",
            "equation": f"h = −C / (2A) = −({C}) / (2·{A})",
            "result": str(_r(h)),
        })

        steps.append({
            "title": "Completar cuadrado en y",
            "equation": f"k = −D / (2B) = −({D}) / (2·{B})",
            "result": str(_r(k)),
        })

        constant = -E + (C ** 2) / (4 * A) + (D ** 2) / (4 * B)

        steps.append({
            "title": "Constante de normalización K",
            "explanation": (
                "Después de completar cuadrados se obtiene: "
                "A(x−h)² + B(y−k)² = K."
            ),
            "equation": f"K = −({E}) + ({C})²/(4·{A}) + ({D})²/(4·{B})",
            "result": str(_r(constant)),
        })

        x_radius_squared = constant / A
        y_radius_squared = constant / B

        steps.append({
            "title": "Revisar denominadores reales",
            "explanation": (
                "Para que exista una elipse real, los denominadores K/A y K/B "
                "deben ser positivos."
            ),
            "equation": (
                f"K/A = {_r(constant)}/{A} = {_r(x_radius_squared)}   |   "
                f"K/B = {_r(constant)}/{B} = {_r(y_radius_squared)}"
            ),
        })

        canonical = (
            f"({_shift('x', h)})²/({_r(x_radius_squared)}) + "
            f"({_shift('y', k)})²/({_r(y_radius_squared)}) = 1"
        )

        if x_radius_squared < 0 or y_radius_squared < 0:
            steps.append({
                "title": "Elipse imaginaria",
                "explanation": (
                    "Al menos uno de los denominadores es negativo. "
                    "No existen puntos reales que satisfagan la ecuación."
                ),
                "equation": canonical,
            })

            return build_error(
                error="Elipse imaginaria: la ecuación no tiene puntos reales.",
                steps=steps,
                data={
                    "imaginary": True,
                    "degenerate": False,
                    "center": (_r(h), _r(k)),
                    "h": _r(h),
                    "k": _r(k),
                    "a2": _r(x_radius_squared),
                    "b2": _r(y_radius_squared),
                    "x_radius_squared": _r(x_radius_squared),
                    "y_radius_squared": _r(y_radius_squared),
                    "canonical_form": canonical,
                },
            )

        if x_radius_squared == 0 or y_radius_squared == 0:
            steps.append({
                "title": "Elipse degenerada",
                "explanation": (
                    "Uno de los denominadores es cero. "
                    f"La elipse se reduce a un caso degenerado en torno a ({_r(h)}, {_r(k)})."
                ),
                "equation": canonical,
            })

            return build_error(
                error="Elipse degenerada: al menos un denominador es cero.",
                steps=steps,
                data={
                    "imaginary": False,
                    "degenerate": True,
                    "center": (_r(h), _r(k)),
                    "h": _r(h),
                    "k": _r(k),
                    "a2": _r(x_radius_squared),
                    "b2": _r(y_radius_squared),
                    "x_radius_squared": _r(x_radius_squared),
                    "y_radius_squared": _r(y_radius_squared),
                    "canonical_form": canonical,
                },
            )

        semi_major_squared = max(x_radius_squared, y_radius_squared)
        semi_minor_squared = min(x_radius_squared, y_radius_squared)

        a = _sqrt(semi_major_squared)
        b = _sqrt(semi_minor_squared)
        c = _sqrt(semi_major_squared - semi_minor_squared)

        major_axis = "horizontal" if x_radius_squared >= y_radius_squared else "vertical"

        steps.append({
            "title": "Semiejes al cuadrado",
            "equation": (
                f"x² asociado: {_r(x_radius_squared)}   |   "
                f"y² asociado: {_r(y_radius_squared)}"
            ),
            "result": (
                f"a²={_r(semi_major_squared)}  "
                f"b²={_r(semi_minor_squared)}  "
                f"eje mayor={major_axis}"
            ),
        })

        steps.append({
            "title": "Semiejes y distancia focal",
            "explanation": "Para una elipse se cumple c² = a² − b².",
            "equation": (
                f"a = √{_r(semi_major_squared)}   "
                f"b = √{_r(semi_minor_squared)}   "
                f"c = √({_r(semi_major_squared)} − {_r(semi_minor_squared)})"
            ),
            "result": f"a={_r(a)}  b={_r(b)}  c={_r(c)}",
        })

        steps.append({
            "title": "Forma canónica",
            "equation": canonical,
        })

        return build_success(
            conic_type="ellipse",
            explanation="La elipse fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (_r(h), _r(k)),
                "h": _r(h),
                "k": _r(k),
                "a2": _r(x_radius_squared),
                "b2": _r(y_radius_squared),

                "x_radius_squared": _r(x_radius_squared),
                "y_radius_squared": _r(y_radius_squared),
                "semi_major_squared": _r(semi_major_squared),
                "semi_minor_squared": _r(semi_minor_squared),
                "major_axis": major_axis,

                "a": _r(a),
                "b": _r(b),
                "c": _r(c),
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)