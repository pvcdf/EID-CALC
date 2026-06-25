# conicas-rut/core/conicas/transforms/parabola_transform.py

from core.utils.result_models import build_success, build_error

#helpers internos para no repetir lógica en cada transform.
def _r(value: float, digits: int = 4) -> float:
    return round(value, digits)

#Calcula raíz cuadrada sin math.sqrt
def _shift(variable: str, value: float) -> str:
    value = _r(value)

    if value == 0:
        return variable

    if value > 0:
        return f"{variable} − {value}"

    return f"{variable} + {_r(-value)}"


def transform_parabola(A, B, C, D, E):
    steps: list[dict] = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        if B == 0 and A != 0:
            steps.append({
                "title": "Identificar tipo",
                "explanation": "B = 0 → parábola vertical, con eje paralelo al eje y.",
                "equation": f"({A})x² + ({C})x + ({D})y + {E} = 0",
            })

            h = -C / (2 * A)

            steps.append({
                "title": "Completar cuadrado en x",
                "equation": f"h = −C / (2A) = −({C}) / (2·{A})",
                "result": str(_r(h)),
            })

            if D == 0:
                steps.append({
                    "title": "Coeficiente D = 0",
                    "explanation": (
                        "No hay término lineal en y, por lo tanto no se puede obtener "
                        "la forma estándar (x−h)² = 4p(y−k)."
                    ),
                })

                return build_error(
                    error="Parábola degenerada: D = 0, no hay término lineal en y.",
                    steps=steps,
                    data={
                        "imaginary": False,
                        "degenerate": True,
                    },
                )

            k = ((C ** 2) / (4 * A) - E) / D
            p = -D / (4 * A)

            steps.append({
                "title": "Despejar k",
                "explanation": "Al completar cuadrado se obtiene el vértice (h, k).",
                "equation": f"k = (C²/4A − E) / D = ({_r((C ** 2) / (4 * A))} − {E}) / {D}",
                "result": str(_r(k)),
            })

            steps.append({
                "title": "Calcular p",
                "explanation": "De la forma (x−h)² = 4p(y−k), se cumple 4p = −D/A.",
                "equation": f"p = −D/(4A) = −({D})/(4·{A})",
                "result": str(_r(p)),
            })

            canonical = f"({_shift('x', h)})² = {_r(4 * p)}({_shift('y', k)})"
            orientation = "vertical"

        elif A == 0 and B != 0:
            steps.append({
                "title": "Identificar tipo",
                "explanation": "A = 0 → parábola horizontal, con eje paralelo al eje x.",
                "equation": f"({B})y² + ({D})y + ({C})x + {E} = 0",
            })

            k = -D / (2 * B)

            steps.append({
                "title": "Completar cuadrado en y",
                "equation": f"k = −D / (2B) = −({D}) / (2·{B})",
                "result": str(_r(k)),
            })

            if C == 0:
                steps.append({
                    "title": "Coeficiente C = 0",
                    "explanation": (
                        "No hay término lineal en x, por lo tanto no se puede obtener "
                        "la forma estándar (y−k)² = 4p(x−h)."
                    ),
                })

                return build_error(
                    error="Parábola degenerada: C = 0, no hay término lineal en x.",
                    steps=steps,
                    data={
                        "imaginary": False,
                        "degenerate": True,
                    },
                )

            h = ((D ** 2) / (4 * B) - E) / C
            p = -C / (4 * B)

            steps.append({
                "title": "Despejar h",
                "explanation": "Al completar cuadrado se obtiene el vértice (h, k).",
                "equation": f"h = (D²/4B − E) / C = ({_r((D ** 2) / (4 * B))} − {E}) / {C}",
                "result": str(_r(h)),
            })

            steps.append({
                "title": "Calcular p",
                "explanation": "De la forma (y−k)² = 4p(x−h), se cumple 4p = −C/B.",
                "equation": f"p = −C/(4B) = −({C})/(4·{B})",
                "result": str(_r(p)),
            })

            canonical = f"({_shift('y', k)})² = {_r(4 * p)}({_shift('x', h)})"
            orientation = "horizontal"

        else:
            return build_error(
                error="La ecuación no corresponde a una parábola estándar: se requiere A = 0 o B = 0, pero no ambos.",
                steps=steps,
            )

        focus = None
        directrix = None
        axis = None

        if orientation == "vertical":
            focus = (_r(h), _r(k + p))
            directrix = f"y = {_r(k - p)}"
            axis = f"x = {_r(h)}"
        elif orientation == "horizontal":
            focus = (_r(h + p), _r(k))
            directrix = f"x = {_r(h - p)}"
            axis = f"y = {_r(k)}"

        steps.append({
            "title": "Forma canónica",
            "explanation": (
                f"Orientación: {orientation}   |   "
                f"Vértice: ({_r(h)}, {_r(k)})   |   "
                f"p = {_r(p)}"
            ),
            "equation": canonical,
        })

        steps.append({
            "title": "Elementos principales",
            "explanation": "A partir de p se obtiene el foco, la directriz y el eje de simetría.",
            "result": f"Foco = {focus}   |   Directriz: {directrix}   |   Eje: {axis}",
        })

        return build_success(
            conic_type="parabola",
            explanation="La parábola fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "orientation": orientation,
                "vertex": (_r(h), _r(k)),
                "h": _r(h),
                "k": _r(k),
                "p": _r(p),
                "focus": focus,
                "directrix": directrix,
                "axis": axis,
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)