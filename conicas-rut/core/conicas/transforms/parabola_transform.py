# conicas-rut/core/conicas/transforms/parabola_transform.py

from core.utils.manual_math import round_value, shift_text
from core.utils.result_models import build_success, build_error


def transform_parabola(A, B, C, D, E) -> dict:
    """
    Transforma una parábola desde forma general a forma canónica.
    """
    steps = []

    try:
        A = round_value(A, 6)
        B = round_value(B, 6)
        C = round_value(C, 6)
        D = round_value(D, 6)
        E = round_value(E, 6)

        steps.append({
            "title": "Ecuación general",
            "explanation": "Se parte desde Ax² + By² + Cx + Dy + E = 0.",
            "equation": f"{A}x² + {B}y² + {C}x + {D}y + {E} = 0",
        })

        if B == 0 and A != 0:
            return _transform_vertical_parabola(A, C, D, E, steps)

        if A == 0 and B != 0:
            return _transform_horizontal_parabola(B, C, D, E, steps)

        return build_error(
            error="No se puede transformar como parábola: exactamente uno entre A o B debe ser cero.",
            steps=steps,
            data={
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
            },
        )

    except Exception as error:
        return build_error(
            error=f"Error al transformar parábola: {error}",
            steps=steps,
        )


def _transform_vertical_parabola(A, C, D, E, steps):
    """
    Caso B = 0:

        Ax² + Cx + Dy + E = 0

    Forma canónica:

        (x−h)² = 4p(y−k)
    """
    if D == 0:
        return build_error(
            error="Parábola vertical degenerada: D = 0.",
            steps=steps,
            data={
                "A": A,
                "C": C,
                "D": D,
                "E": E,
                "orientation": "vertical",
                "degenerate": True,
            },
        )

    h = -C / (2 * A)
    k = ((C**2) / (4 * A) - E) / D
    p = -D / (4 * A)

    canonical_form = (
        f"({shift_text('x', h)})² = "
        f"{round_value(4 * p)}({shift_text('y', k)})"
    )

    focus = (h, k + p)
    directrix = f"y = {round_value(k - p)}"
    axis = f"x = {round_value(h)}"

    steps.append({
        "title": "Tipo de parábola",
        "explanation": (
            "Como B = 0 y A ≠ 0, falta el término y². "
            "La parábola tiene eje vertical."
        ),
        "result": "Parábola vertical",
    })

    steps.append({
        "title": "Vértice",
        "explanation": (
            "Para Ax² + Cx + Dy + E = 0 se completa cuadrado en x."
        ),
        "equation": (
            f"h = −C/(2A) = −({C})/(2·{A}) = {round_value(h)} ; "
            f"k = (C²/(4A) − E)/D = {round_value(k)}"
        ),
        "result": f"Vértice = ({round_value(h)}, {round_value(k)})",
    })

    steps.append({
        "title": "Parámetro p",
        "explanation": (
            "Al comparar con (x−h)² = 4p(y−k), "
            "se obtiene p = −D/(4A)."
        ),
        "equation": f"p = −({D})/(4·{A}) = {round_value(p)}",
        "result": f"p = {round_value(p)}",
    })

    steps.append({
        "title": "Elementos",
        "explanation": "Se calculan foco, directriz y eje de simetría.",
        "result": (
            f"Foco = ({round_value(focus[0])}, {round_value(focus[1])}) ; "
            f"Directriz: {directrix} ; "
            f"Eje: {axis}"
        ),
    })

    steps.append({
        "title": "Forma canónica",
        "explanation": "Se obtiene la forma canónica de la parábola vertical.",
        "equation": canonical_form,
    })

    return build_success(
        conic_type="parabola",
        explanation="La parábola vertical fue transformada a forma canónica.",
        steps=steps,
        data={
            "A": A,
            "B": 0,
            "C": C,
            "D": D,
            "E": E,
            "vertex": (round_value(h), round_value(k)),
            "h": round_value(h),
            "k": round_value(k),
            "p": round_value(p),
            "focus": (round_value(focus[0]), round_value(focus[1])),
            "directrix": directrix,
            "axis": axis,
            "orientation": "vertical",
            "canonical_form": canonical_form,
            "imaginary": False,
            "degenerate": False,
        },
    )


def _transform_horizontal_parabola(B, C, D, E, steps):
    """
    Caso A = 0:

        By² + Cx + Dy + E = 0

    Forma canónica:

        (y−k)² = 4p(x−h)
    """
    if C == 0:
        return build_error(
            error="Parábola horizontal degenerada: C = 0.",
            steps=steps,
            data={
                "A": 0,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
                "orientation": "horizontal",
                "degenerate": True,
            },
        )

    k = -D / (2 * B)
    h = ((D**2) / (4 * B) - E) / C
    p = -C / (4 * B)

    canonical_form = (
        f"({shift_text('y', k)})² = "
        f"{round_value(4 * p)}({shift_text('x', h)})"
    )

    focus = (h + p, k)
    directrix = f"x = {round_value(h - p)}"
    axis = f"y = {round_value(k)}"

    steps.append({
        "title": "Tipo de parábola",
        "explanation": (
            "Como A = 0 y B ≠ 0, falta el término x². "
            "La parábola tiene eje horizontal."
        ),
        "result": "Parábola horizontal",
    })

    steps.append({
        "title": "Vértice",
        "explanation": (
            "Para By² + Cx + Dy + E = 0 se completa cuadrado en y."
        ),
        "equation": (
            f"k = −D/(2B) = −({D})/(2·{B}) = {round_value(k)} ; "
            f"h = (D²/(4B) − E)/C = {round_value(h)}"
        ),
        "result": f"Vértice = ({round_value(h)}, {round_value(k)})",
    })

    steps.append({
        "title": "Parámetro p",
        "explanation": (
            "Al comparar con (y−k)² = 4p(x−h), "
            "se obtiene p = −C/(4B)."
        ),
        "equation": f"p = −({C})/(4·{B}) = {round_value(p)}",
        "result": f"p = {round_value(p)}",
    })

    steps.append({
        "title": "Elementos",
        "explanation": "Se calculan foco, directriz y eje de simetría.",
        "result": (
            f"Foco = ({round_value(focus[0])}, {round_value(focus[1])}) ; "
            f"Directriz: {directrix} ; "
            f"Eje: {axis}"
        ),
    })

    steps.append({
        "title": "Forma canónica",
        "explanation": "Se obtiene la forma canónica de la parábola horizontal.",
        "equation": canonical_form,
    })

    return build_success(
        conic_type="parabola",
        explanation="La parábola horizontal fue transformada a forma canónica.",
        steps=steps,
        data={
            "A": 0,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
            "vertex": (round_value(h), round_value(k)),
            "h": round_value(h),
            "k": round_value(k),
            "p": round_value(p),
            "focus": (round_value(focus[0]), round_value(focus[1])),
            "directrix": directrix,
            "axis": axis,
            "orientation": "horizontal",
            "canonical_form": canonical_form,
            "imaginary": False,
            "degenerate": False,
        },
    )