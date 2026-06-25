# conicas-rut/core/conicas/transforms/general_transform.py

from core.utils.result_models import build_success, build_error
from core.conicas.coef_builder import fraccion_a_texto


def transform_to_general(conic_type, transform_data, coef_data):
    try:
        if not isinstance(transform_data, dict) or not isinstance(coef_data, dict):
            return build_error(error="Datos insuficientes para transformar a forma general.")

        if transform_data.get("imaginary") or transform_data.get("degenerate"):
            return build_error(
                error="No se ejecuta procedimiento inverso para cónicas imaginarias o degeneradas.",
                data={
                    "canonical_form": transform_data.get("canonical_form", "—"),
                    "equation_str": coef_data.get("equation_str", "—"),
                },
            )

        if conic_type == "circle":
            return _circle_to_general(transform_data, coef_data)

        if conic_type == "ellipse":
            return _ellipse_to_general(transform_data, coef_data)

        if conic_type == "hyperbola":
            return _hyperbola_to_general(transform_data, coef_data)

        if conic_type == "parabola":
            return _parabola_to_general(transform_data, coef_data)

        return build_error(error=f"Tipo '{conic_type}' no reconocido.")

    except Exception as ex:
        return build_error(error=str(ex))

#helpers internos para no repetir lógica en cada transform.
def r(n):
    return round(n, 2)


def _get_center(td):
    if "center" in td:
        return td["center"]

    if "vertex" in td:
        return td["vertex"]

    return td.get("h", 0), td.get("k", 0)


def _circle_to_general(td, cd):
    h, k = _get_center(td)

    A = cd["A"]
    B = cd["B"]
    af = cd["A_frac"]
    bf = cd["B_frac"]

    Ar = r(A)
    Br = r(B)

    Ax2h = r(A * 2 * h)
    Ah2 = r(A * h ** 2)
    By2k = r(B * 2 * k)
    Bk2 = r(B * k ** 2)

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": "Ecuación canónica de la circunferencia.",
        },
        {
            "title": "Expandir (x − h)²",
            "equation": f"(x − {h})² = x² − {r(2 * h)}x + {r(h ** 2)}",
        },
        {
            "title": "Expandir (y − k)²",
            "equation": f"(y − {k})² = y² − {r(2 * k)}y + {r(k ** 2)}",
        },
        {
            "title": f"Multiplicar por A = {fraccion_a_texto(*af)}",
            "equation": f"{fraccion_a_texto(*af)}·x² − {Ax2h}x + {Ah2}",
            "explanation": f"A = {fraccion_a_texto(*af)} = {Ar}",
        },
        {
            "title": f"Multiplicar por B = {fraccion_a_texto(*bf)}",
            "equation": f"{fraccion_a_texto(*bf)}·y² − {By2k}y + {Bk2}",
            "explanation": f"B = {fraccion_a_texto(*bf)} = {Br}",
        },
        {
            "title": "Restar r² y agrupar = 0",
            "equation": cd.get("equation_str", "—"),
            "result": "Forma general recuperada",
        },
    ]

    return build_success(
        conic_type="circle",
        explanation="Canónica → general completada.",
        steps=steps,
        data={
            "equation_str": cd.get("equation_str", "—"),
        },
    )


def _ellipse_to_general(td, cd):
    h, k = _get_center(td)

    x_radius_squared = td.get("x_radius_squared", td.get("a2"))
    y_radius_squared = td.get("y_radius_squared", td.get("b2"))

    A = cd["A"]
    B = cd["B"]
    af = cd["A_frac"]
    bf = cd["B_frac"]

    Ar = r(A)
    Br = r(B)

    prod = r(x_radius_squared * y_radius_squared)

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": "Ecuación canónica de la elipse.",
        },
        {
            "title": "Eliminar denominadores",
            "explanation": (
                f"Se multiplica por el producto de los denominadores: "
                f"{x_radius_squared}·{y_radius_squared} = {prod}."
            ),
            "equation": (
                f"{y_radius_squared}·(x−{h})² + "
                f"{x_radius_squared}·(y−{k})² = {prod}"
            ),
        },
        {
            "title": "Expandir cuadrados",
            "equation": (
                f"(x−{h})² = x²−{r(2 * h)}x+{r(h ** 2)}  |  "
                f"(y−{k})² = y²−{r(2 * k)}y+{r(k ** 2)}"
            ),
        },
        {
            "title": "Aplicar coeficientes originales",
            "equation": f"{fraccion_a_texto(*af)}·x² + {fraccion_a_texto(*bf)}·y² + ... = 0",
            "explanation": f"A = {fraccion_a_texto(*af)} = {Ar}   B = {fraccion_a_texto(*bf)} = {Br}",
        },
        {
            "title": "Agrupar todos los términos = 0",
            "equation": cd.get("equation_str", "—"),
            "result": "Forma general recuperada",
        },
    ]

    return build_success(
        conic_type="ellipse",
        explanation="Canónica → general completada.",
        steps=steps,
        data={
            "equation_str": cd.get("equation_str", "—"),
        },
    )


def _hyperbola_to_general(td, cd):
    h, k = _get_center(td)

    x_radius_squared = td.get("x_radius_squared", td.get("a2"))
    y_radius_squared = td.get("y_radius_squared", td.get("b2"))
    orientation = td.get("orientation", "horizontal")

    A = cd["A"]
    B = cd["B"]
    af = cd["A_frac"]
    bf = cd["B_frac"]

    Ar = r(A)
    Br = r(B)
    prod = r(x_radius_squared * y_radius_squared)

    if orientation == "horizontal":
        expanded = (
            f"{y_radius_squared}·(x−{h})² − "
            f"{x_radius_squared}·(y−{k})² = {prod}"
        )
    else:
        expanded = (
            f"{x_radius_squared}·(y−{k})² − "
            f"{y_radius_squared}·(x−{h})² = {prod}"
        )

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": f"Ecuación canónica de la hipérbola ({orientation}).",
        },
        {
            "title": "Eliminar denominadores",
            "explanation": (
                f"Se multiplica por el producto de los denominadores: "
                f"{x_radius_squared}·{y_radius_squared} = {prod}."
            ),
            "equation": expanded,
        },
        {
            "title": "Expandir cuadrados",
            "equation": (
                f"(x−{h})² = x²−{r(2 * h)}x+{r(h ** 2)}  |  "
                f"(y−{k})² = y²−{r(2 * k)}y+{r(k ** 2)}"
            ),
        },
        {
            "title": "Aplicar coeficientes originales",
            "equation": f"{fraccion_a_texto(*af)}·x² + {fraccion_a_texto(*bf)}·y² + ... = 0",
            "explanation": f"A = {fraccion_a_texto(*af)} = {Ar}   B = {fraccion_a_texto(*bf)} = {Br}",
        },
        {
            "title": "Agrupar todos los términos = 0",
            "equation": cd.get("equation_str", "—"),
            "result": "Forma general recuperada",
        },
    ]

    return build_success(
        conic_type="hyperbola",
        explanation="Canónica → general completada.",
        steps=steps,
        data={
            "equation_str": cd.get("equation_str", "—"),
        },
    )


def _parabola_to_general(td, cd):
    h, k = _get_center(td)
    p = td["p"]
    orientation = td.get("orientation", "vertical")

    af = cd["A_frac"]
    bf = cd["B_frac"]
    A = cd["A"]
    B = cd["B"]

    Ar = r(A)
    Br = r(B)

    p4 = r(4 * p)

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": f"Ecuación canónica de la parábola ({orientation}).",
        },
    ]

    if orientation == "vertical":
        coef_str = fraccion_a_texto(*af)

        steps += [
            {
                "title": "Expandir (x − h)²",
                "equation": f"(x − {h})² = x² − {r(2 * h)}x + {r(h ** 2)}",
            },
            {
                "title": "Despejar hacia forma general",
                "equation": f"(x − {h})² = {p4}(y − {k})",
            },
            {
                "title": f"Relacionar con A = {coef_str}",
                "equation": f"{coef_str}x² + ... = 0",
                "explanation": f"A = {coef_str} = {Ar}",
            },
        ]

    else:
        coef_str = fraccion_a_texto(*bf)

        steps += [
            {
                "title": "Expandir (y − k)²",
                "equation": f"(y − {k})² = y² − {r(2 * k)}y + {r(k ** 2)}",
            },
            {
                "title": "Despejar hacia forma general",
                "equation": f"(y − {k})² = {p4}(x − {h})",
            },
            {
                "title": f"Relacionar con B = {coef_str}",
                "equation": f"{coef_str}y² + ... = 0",
                "explanation": f"B = {coef_str} = {Br}",
            },
        ]

    steps.append({
        "title": "Agrupar todos los términos = 0",
        "equation": cd.get("equation_str", "—"),
        "result": "Forma general recuperada",
    })

    return build_success(
        conic_type="parabola",
        explanation="Canónica → general completada.",
        steps=steps,
        data={
            "equation_str": cd.get("equation_str", "—"),
        },
    )