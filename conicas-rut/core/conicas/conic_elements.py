# conicas-rut/core/conicas/conic_elements.py

"""
Construcción de elementos geométricos de cónicas.

Este módulo separa la lógica matemática de elementos desde ConicView.
"""

from core.utils.manual_math import safe_div


def get_conic_element_fields(conic_type: str) -> list[tuple[str, str]]:
    """
    Retorna los campos que debe mostrar la UI para cada tipo de cónica.

    """
    fields = {
        "circle": [
            ("Centro", "centro"),
            ("Radio", "radio"),
        ],
        "ellipse": [
            ("Centro", "centro"),
            ("Vértices", "vertices"),
            ("Co-vértices", "covertices"),
            ("Focos", "focos"),
            ("a", "a"),
            ("b", "b"),
            ("c", "c"),
            ("Eje mayor", "eje_mayor"),
            ("Eje menor", "eje_menor"),
            ("Orientación", "orientacion"),
        ],
        "hyperbola": [
            ("Centro", "centro"),
            ("Vértices", "vertices"),
            ("Focos", "focos"),
            ("a", "a"),
            ("b", "b"),
            ("c", "c"),
            ("Eje transverso", "eje_transverso"),
            ("Eje conjugado", "eje_conjugado"),
            ("Asíntotas", "asintotas"),
            ("Orientación", "orientacion"),
        ],
        "parabola": [
            ("Vértice", "vertice"),
            ("Foco", "foco"),
            ("Directriz", "directriz"),
            ("Eje de simetría", "eje"),
            ("p", "p"),
            ("Orientación", "orientacion"),
        ],
    }

    return fields.get(conic_type, [])


def build_conic_elements(conic_type: str, transform_data: dict) -> dict:
    """
    Construye los elementos geométricos de una cónica.
    """
    if not isinstance(transform_data, dict):
        return {
            "valid": False,
            "reason": "Datos de transformación inválidos.",
            "fields": [],
            "values": {},
        }

    if transform_data.get("imaginary"):
        return {
            "valid": False,
            "reason": "Sin elementos reales: cónica imaginaria.",
            "fields": [],
            "values": {},
        }

    if transform_data.get("degenerate"):
        return {
            "valid": False,
            "reason": "Cónica degenerada.",
            "fields": [],
            "values": {},
        }

    fields = get_conic_element_fields(conic_type)

    if conic_type == "circle":
        values = _circle_elements(transform_data)

    elif conic_type == "ellipse":
        values = _ellipse_elements(transform_data)

    elif conic_type == "hyperbola":
        values = _hyperbola_elements(transform_data)

    elif conic_type == "parabola":
        values = _parabola_elements(transform_data)

    else:
        values = {}

    return {
        "valid": bool(values),
        "reason": "" if values else "No se pudieron construir elementos.",
        "fields": fields,
        "values": values,
    }


def _circle_elements(td: dict) -> dict:
    center = td.get("center")
    radius = td.get("radius")

    if center is None or radius is None:
        return {}

    return {
        "centro": _fmt_coord(center),
        "radio": _fmt_number(radius),
    }


def _ellipse_elements(td: dict) -> dict:
    center = td.get("center")
    a = td.get("a")
    b = td.get("b")
    c = td.get("c")

    if center is None or a is None or b is None or c is None:
        return {}

    h, k = center
    orientation = _ellipse_orientation(td)

    if orientation == "horizontal":
        vertices = [(h - a, k), (h + a, k)]
        covertices = [(h, k - b), (h, k + b)]
        foci = [(h - c, k), (h + c, k)]
        eje_mayor = f"y = {_fmt_number(k)}"
        eje_menor = f"x = {_fmt_number(h)}"

    else:
        vertices = [(h, k - a), (h, k + a)]
        covertices = [(h - b, k), (h + b, k)]
        foci = [(h, k - c), (h, k + c)]
        eje_mayor = f"x = {_fmt_number(h)}"
        eje_menor = f"y = {_fmt_number(k)}"

    return {
        "centro": _fmt_coord(center),
        "vertices": _fmt_points(vertices),
        "covertices": _fmt_points(covertices),
        "focos": _fmt_points(foci),
        "a": _fmt_number(a),
        "b": _fmt_number(b),
        "c": _fmt_number(c),
        "eje_mayor": eje_mayor,
        "eje_menor": eje_menor,
        "orientacion": orientation,
    }


def _hyperbola_elements(td: dict) -> dict:
    center = td.get("center")
    a = td.get("a")
    b = td.get("b")
    c = td.get("c")

    if center is None or a is None or b is None or c is None:
        return {}

    h, k = center
    orientation = td.get("orientation", "horizontal")

    if orientation == "horizontal":
        vertices = [(h - a, k), (h + a, k)]
        foci = [(h - c, k), (h + c, k)]
        eje_transverso = f"y = {_fmt_number(k)}"
        eje_conjugado = f"x = {_fmt_number(h)}"
        pendiente = safe_div(b, a)

    else:
        vertices = [(h, k - a), (h, k + a)]
        foci = [(h, k - c), (h, k + c)]
        eje_transverso = f"x = {_fmt_number(h)}"
        eje_conjugado = f"y = {_fmt_number(k)}"
        pendiente = safe_div(a, b)

    asintotas = (
        f"y − {_fmt_number(k)} = ±{_fmt_number(pendiente)}"
        f"(x − {_fmt_number(h)})"
    )

    return {
        "centro": _fmt_coord(center),
        "vertices": _fmt_points(vertices),
        "focos": _fmt_points(foci),
        "a": _fmt_number(a),
        "b": _fmt_number(b),
        "c": _fmt_number(c),
        "eje_transverso": eje_transverso,
        "eje_conjugado": eje_conjugado,
        "asintotas": asintotas,
        "orientacion": orientation,
    }


def _parabola_elements(td: dict) -> dict:
    vertex = td.get("vertex")
    p = td.get("p")

    if vertex is None or p is None:
        return {}

    h, k = vertex
    orientation = td.get("orientation", "vertical")

    if orientation == "vertical":
        focus = td.get("focus", (h, k + p))
        directrix = td.get("directrix", f"y = {_fmt_number(k - p)}")
        axis = td.get("axis", f"x = {_fmt_number(h)}")

    else:
        focus = td.get("focus", (h + p, k))
        directrix = td.get("directrix", f"x = {_fmt_number(h - p)}")
        axis = td.get("axis", f"y = {_fmt_number(k)}")

    return {
        "vertice": _fmt_coord(vertex),
        "foco": _fmt_coord(focus),
        "directriz": directrix,
        "eje": axis,
        "p": _fmt_number(p),
        "orientacion": orientation,
    }


def _ellipse_orientation(td: dict) -> str:
    """
    Determina si el eje mayor de la elipse es horizontal o vertical.
    """
    if td.get("major_axis"):
        return td["major_axis"]

    x_radius_squared = td.get("x_radius_squared", td.get("a2", 0))
    y_radius_squared = td.get("y_radius_squared", td.get("b2", 0))

    return "horizontal" if x_radius_squared >= y_radius_squared else "vertical"


def _fmt_number(value, digits=2) -> str:
    """
    Formatea números para mostrarlos en la UI.
    """
    if value is None:
        return "—"

    if isinstance(value, str):
        return value

    value = round(value, digits)

    if value == int(value):
        return str(int(value))

    return f"{value:.{digits}f}"


def _fmt_coord(pair) -> str:
    return f"({_fmt_number(pair[0])}, {_fmt_number(pair[1])})"


def _fmt_points(points) -> str:
    return " ; ".join(_fmt_coord(point) for point in points)