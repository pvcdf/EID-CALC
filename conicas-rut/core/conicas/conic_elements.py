# conicas-rut/core/conicas/conic_elements.py

"""
Construye los elementos geométricos principales de cada cónica.
Se usa después de transformar la ecuación a forma canónica.
"""


# ── Campos esperados por tipo de cónica ────────────────────────────────────

def get_conic_element_fields(conic_type: str) -> list[tuple[str, str]]:
    """Devuelve los campos que la interfaz debe mostrar según la cónica."""
    fields = {
        "circle": [
            ("Centro", "centro"), ("Radio", "radio"),
        ],
        "ellipse": [
            ("Centro", "centro"), ("Vértices", "vertices"),
            ("Co-vértices", "covertices"), ("a", "a"),
            ("b", "b"), ("Orientación", "orientacion"),
        ],
        "hyperbola": [
            ("Centro", "centro"), ("Vértices", "vertices"),
            ("a", "a"), ("b", "b"), ("Orientación", "orientacion"),
        ],
        "parabola": [
            ("Vértice", "vertice"), ("Foco", "foco"),
            ("Directriz", "directriz"), ("Orientación", "orientacion"),
        ],
    }

    return fields.get(conic_type, [])


# ── Construcción general de elementos ──────────────────────────────────────

def build_conic_elements(conic_type: str, transform_data: dict) -> dict:
    """Construye los elementos geométricos desde los datos canónicos."""
    if not isinstance(transform_data, dict):
        return _invalid("Datos de transformación inválidos.")

    if transform_data.get("imaginary"):
        return _invalid("Sin elementos reales: cónica imaginaria.")

    if transform_data.get("degenerate"):
        return _invalid("Cónica degenerada.")

    builders = {
        "circle": _circle_elements,
        "ellipse": _ellipse_elements,
        "hyperbola": _hyperbola_elements,
        "parabola": _parabola_elements,
    }

    values = builders.get(conic_type, lambda _: {})(transform_data)

    return {
        "valid": bool(values),
        "reason": "" if values else "No se pudieron construir elementos.",
        "fields": get_conic_element_fields(conic_type),
        "values": values,
    }


def _invalid(reason: str) -> dict:
    """Respuesta estándar para cónicas sin elementos calculables."""
    return {"valid": False, "reason": reason, "fields": [], "values": {}}


# ── Elementos por tipo de cónica ───────────────────────────────────────────

def _circle_elements(td: dict) -> dict:
    """Devuelve centro y radio de una circunferencia."""
    center = td.get("center")
    radius = td.get("radius")

    if center is None or radius is None:
        return {}

    return {
        "centro": _fmt_coord(center),
        "radio": _fmt_number(radius),
    }


def _ellipse_elements(td: dict) -> dict:
    """Devuelve centro, vértices, co-vértices y semiejes de una elipse."""
    center = td.get("center")
    a = td.get("a")  # semieje mayor
    b = td.get("b")  # semieje menor

    if center is None or a is None or b is None:
        return {}

    h, k = center
    orientation = get_ellipse_orientation(td)

    if orientation == "vertical":
        vertices = [(h, k - a), (h, k + a)]
        covertices = [(h - b, k), (h + b, k)]
    else:
        vertices = [(h - a, k), (h + a, k)]
        covertices = [(h, k - b), (h, k + b)]

    return {
        "centro": _fmt_coord(center),
        "vertices": _fmt_points(vertices),
        "covertices": _fmt_points(covertices),
        "a": _fmt_number(a),
        "b": _fmt_number(b),
        "orientacion": orientation,
    }


def _hyperbola_elements(td: dict) -> dict:
    """Devuelve centro, vértices y semiejes de una hipérbola."""
    center = td.get("center")
    a = td.get("a")  # semieje transversal
    b = td.get("b")  # semieje conjugado

    if center is None or a is None or b is None:
        return {}

    h, k = center
    orientation = td.get("orientation", "horizontal")

    if orientation == "vertical":
        vertices = [(h, k - a), (h, k + a)]
    else:
        vertices = [(h - a, k), (h + a, k)]

    return {
        "centro": _fmt_coord(center),
        "vertices": _fmt_points(vertices),
        "a": _fmt_number(a),
        "b": _fmt_number(b),
        "orientacion": orientation,
    }


def _parabola_elements(td: dict) -> dict:
    """Devuelve vértice, foco, directriz y orientación de una parábola."""
    vertex = td.get("vertex")
    p = td.get("p")  # distancia del vértice al foco y a la directriz

    if vertex is None or p is None:
        return {}

    h, k = vertex
    orientation = td.get("orientation", "vertical")

    if orientation == "horizontal":
        focus = td.get("focus", (h + p, k))
        directrix = td.get("directrix", f"x = {_fmt_number(h - p)}")
    else:
        focus = td.get("focus", (h, k + p))
        directrix = td.get("directrix", f"y = {_fmt_number(k - p)}")

    return {
        "vertice": _fmt_coord(vertex),
        "foco": _fmt_coord(focus),
        "directriz": directrix,
        "orientacion": orientation,
    }


# ── Orientación y formato ─────────────────────────────────────────────────

def get_ellipse_orientation(td: dict) -> str:
    """Determina si el eje mayor de la elipse es horizontal o vertical."""
    if not isinstance(td, dict):
        return "horizontal"

    if td.get("major_axis"):
        return td["major_axis"]

    x_radius_squared = td.get("x_radius_squared", td.get("a2", 0))
    y_radius_squared = td.get("y_radius_squared", td.get("b2", 0))

    return "horizontal" if x_radius_squared >= y_radius_squared else "vertical"


def _fmt_number(value, digits=2) -> str:
    """Formatea números para evitar decimales innecesarios."""
    if value is None:
        return "—"

    if isinstance(value, str):
        return value

    value = round(value, digits)

    if value == int(value):
        return str(int(value))

    return f"{value:.{digits}f}"


def _fmt_coord(pair) -> str:
    """Formatea un punto como (x, y)."""
    return f"({_fmt_number(pair[0])}, {_fmt_number(pair[1])})"


def _fmt_points(points) -> str:
    """Formatea una lista de puntos."""
    return " ; ".join(_fmt_coord(point) for point in points)