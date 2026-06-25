# conicas-rut/core/conicas/transforms/hyperbola_transform.py

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


def transform_hyperbola(A, B, C, D, E):
    steps: list[dict] = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        if A == 0 or B == 0:
            return build_error(
                error="No se puede transformar como hipérbola porque A o B es cero.",
                steps=steps,
            )

        steps.append({
            "title": "Identificar coeficientes",
            "explanation": "A y B tienen signos opuestos, por lo tanto la cónica se clasifica como hipérbola.",
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
            "title": "Calcular constante K",
            "explanation": "Después de completar cuadrados se obtiene A(x−h)² + B(y−k)² = K.",
            "equation": f"K = −({E}) + ({C})²/(4·{A}) + ({D})²/(4·{B})",
            "result": str(_r(constant)),
        })

        if constant == 0:
            steps.append({
                "title": "Hipérbola degenerada",
                "explanation": (
                    "K = 0. La ecuación se reduce a un par de rectas que se cruzan "
                    f"en el centro ({_r(h)}, {_r(k)})."
                ),
            })

            return build_error(
                error="Hipérbola degenerada: K = 0 (par de rectas).",
                steps=steps,
                data={
                    "imaginary": False,
                    "degenerate": True,
                    "center": (_r(h), _r(k)),
                    "h": _r(h),
                    "k": _r(k),
                },
            )

        x_denominator = constant / A
        y_denominator = constant / B

        x_positive = x_denominator > 0
        y_positive = y_denominator > 0

        if x_positive == y_positive:
            return build_error(
                error="No fue posible normalizar la hipérbola: los signos no generan una resta válida.",
                steps=steps,
                data={
                    "center": (_r(h), _r(k)),
                    "x_denominator": _r(x_denominator),
                    "y_denominator": _r(y_denominator),
                },
            )

        orientation = "horizontal" if x_positive else "vertical"

        x_radius_squared = abs(x_denominator)
        y_radius_squared = abs(y_denominator)

        if orientation == "horizontal":
            transverse_squared = x_radius_squared
            conjugate_squared = y_radius_squared
            canonical = (
                f"({_shift('x', h)})²/{_r(x_radius_squared)} − "
                f"({_shift('y', k)})²/{_r(y_radius_squared)} = 1"
            )
        else:
            transverse_squared = y_radius_squared
            conjugate_squared = x_radius_squared
            canonical = (
                f"({_shift('y', k)})²/{_r(y_radius_squared)} − "
                f"({_shift('x', h)})²/{_r(x_radius_squared)} = 1"
            )

        a = _sqrt(transverse_squared)
        b = _sqrt(conjugate_squared)
        c = _sqrt(transverse_squared + conjugate_squared)

        steps.append({
            "title": "Normalizar la ecuación",
            "explanation": (
                "Se divide por K. El término que queda positivo define la orientación "
                "de la hipérbola."
            ),
            "equation": (
                f"K/A = {_r(x_denominator)}   |   "
                f"K/B = {_r(y_denominator)}"
            ),
            "result": f"Orientación: {orientation}",
        })

        steps.append({
            "title": "Semiejes y distancia focal",
            "explanation": "Para una hipérbola se cumple c² = a² + b².",
            "equation": (
                f"a = √{_r(transverse_squared)}   "
                f"b = √{_r(conjugate_squared)}   "
                f"c = √({_r(transverse_squared)} + {_r(conjugate_squared)})"
            ),
            "result": f"a={_r(a)}  b={_r(b)}  c={_r(c)}",
        })

        steps.append({
            "title": "Forma canónica",
            "explanation": f"Orientación: {orientation}",
            "equation": canonical,
        })

        return build_success(
            conic_type="hyperbola",
            explanation="La hipérbola fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (_r(h), _r(k)),
                "h": _r(h),
                "k": _r(k),
                "orientation": orientation,
                "a2": _r(x_radius_squared),
                "b2": _r(y_radius_squared),

                # Nombres explícitos:
                "x_radius_squared": _r(x_radius_squared),
                "y_radius_squared": _r(y_radius_squared),
                "transverse_squared": _r(transverse_squared),
                "conjugate_squared": _r(conjugate_squared),

                "a": _r(a),
                "b": _r(b),
                "c": _r(c),
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)