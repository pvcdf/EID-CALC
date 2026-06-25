# conicas-rut/core/conicas/transforms/circle_transform.py

from core.utils.result_models import build_success, build_error

#helpers internos para no repetir lógica en cada transform.
def _r(value: float, digits: int = 4) -> float:
    return round(value, digits)

#Redondea valores para mostrar en pasos, canónicas y data  
def _sqrt(value: float) -> float:
    return value ** 0.5


def _shift(variable: str, value: float) -> str:
    value = _r(value)

    if value == 0:
        return variable

    if value > 0:
        return f"{variable} − {value}"

    return f"{variable} + {_r(-value)}"


def transform_circle(A, B, C, D, E):
    steps: list[dict] = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        if A == 0 or B == 0:
            return build_error(
                error="No se puede transformar como circunferencia porque A o B es cero.",
                steps=steps,
            )

        steps.append({
            "title": "Ecuación general de la circunferencia",
            "explanation": (
                "Como A = B, la ecuación general tiene la forma "
                "A·x² + A·y² + C·x + D·y + E = 0."
            ),
            "equation": f"({A})x² + ({B})y² + ({C})x + ({D})y + {E} = 0",
        })

        CA = C / A
        DA = D / A
        EA = E / A

        steps.append({
            "title": "Paso 1 — Dividir por A",
            "explanation": "Se divide toda la ecuación por A para dejar coeficientes cuadráticos iguales a 1.",
            "equation": f"x² + y² + ({_r(CA)})x + ({_r(DA)})y + {_r(EA)} = 0",
        })

        steps.append({
            "title": "Paso 2 — Agrupar y despejar constante",
            "explanation": "Se agrupan los términos en x e y, pasando E/A al lado derecho.",
            "equation": f"(x² + ({_r(CA)})x) + (y² + ({_r(DA)})y) = {_r(-EA)}",
        })

        h = -C / (2 * A)
        k = -D / (2 * A)

        term_x = (C / (2 * A)) ** 2
        term_y = (D / (2 * A)) ** 2

        steps.append({
            "title": "Paso 3 — Completar cuadrado",
            "explanation": (
                f"Se suma (C/2A)² = {_r(term_x)} y "
                f"(D/2A)² = {_r(term_y)} a ambos lados."
            ),
            "equation": (
                f"({_shift('x', h)})² + ({_shift('y', k)})² = "
                f"{_r(-EA)} + {_r(term_x)} + {_r(term_y)}"
            ),
        })

        radius_squared = h ** 2 + k ** 2 - E / A

        steps.append({
            "title": "Paso 4 — Calcular r²",
            "explanation": (
                "Dado que h = −C/2A y k = −D/2A, "
                "el lado derecho se simplifica como r² = h² + k² − E/A."
            ),
            "equation": (
                f"r² = ({_r(h)})² + ({_r(k)})² − ({_r(EA)}) "
                f"= {_r(h ** 2)} + {_r(k ** 2)} − ({_r(EA)})"
            ),
            "result": str(_r(radius_squared)),
        })

        canonical = (
            f"({_shift('x', h)})² + ({_shift('y', k)})² = {_r(radius_squared)}"
        )

        if radius_squared < 0:
            steps.append({
                "title": "Circunferencia imaginaria",
                "explanation": (
                    f"r² = {_r(radius_squared)} < 0. "
                    "No existe radio real, por lo tanto la ecuación no tiene puntos reales."
                ),
                "equation": canonical,
            })

            return build_error(
                error=(
                    f"Circunferencia imaginaria: r² = {_r(radius_squared)} < 0. "
                    "La ecuación no tiene puntos reales."
                ),
                steps=steps,
                data={
                    "imaginary": True,
                    "degenerate": False,
                    "center": (_r(h), _r(k)),
                    "radius_squared": _r(radius_squared),
                    "canonical_form": canonical,
                },
            )

        if radius_squared == 0:
            steps.append({
                "title": "Circunferencia degenerada",
                "explanation": (
                    f"r² = 0. La circunferencia se reduce al punto ({_r(h)}, {_r(k)})."
                ),
                "equation": canonical,
            })

            return build_error(
                error=f"Circunferencia degenerada: se reduce al punto ({_r(h)}, {_r(k)}).",
                steps=steps,
                data={
                    "imaginary": False,
                    "degenerate": True,
                    "center": (_r(h), _r(k)),
                    "radius_squared": 0.0,
                    "canonical_form": canonical,
                },
            )

        radius = _sqrt(radius_squared)

        steps.append({
            "title": "Paso 5 — Forma canónica",
            "equation": canonical,
            "result": f"Centro = ({_r(h)}, {_r(k)})   r = {_r(radius)}",
        })

        return build_success(
            conic_type="circle",
            explanation="La circunferencia fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (_r(h), _r(k)),
                "h": _r(h),
                "k": _r(k),
                "radius": _r(radius),
                "radius_squared": _r(radius_squared),
                "imaginary": False,
                "degenerate": False,
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)