# conicas-rut/core/transforms/general_transform.py

from core.result_models import build_success, build_error
from core.coef_builder import fraccion_a_texto


def transform_to_general(conic_type, transform_data, coef_data):
    try:
        if conic_type == "circle":    return _circle_to_general(transform_data, coef_data)
        if conic_type == "ellipse":   return _ellipse_to_general(transform_data, coef_data)
        if conic_type == "hyperbola": return _hyperbola_to_general(transform_data, coef_data)
        if conic_type == "parabola":  return _parabola_to_general(transform_data, coef_data)
        return build_error(error=f"Tipo '{conic_type}' no reconocido.")
    except Exception as ex:
        return build_error(error=str(ex))


def r(n): return round(n, 2)


def _circle_to_general(td, cd):
    h, k   = td["center"]
    A, B   = cd["A"], cd["B"]
    af, bf = cd["A_frac"], cd["B_frac"]
    Ar, Br = r(A), r(B)

    Ax2h   = r(A * 2 * h);  Ah2  = r(A * h**2)
    By2k   = r(B * 2 * k);  Bk2  = r(B * k**2)

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": "Ecuación canónica de la circunferencia.",
        },
        {
            "title": "Expandir (x − h)²",
            "equation": f"(x − {h})² = x² − {r(2*h)}x + {r(h**2)}",
        },
        {
            "title": "Expandir (y − k)²",
            "equation": f"(y − {k})² = y² − {r(2*k)}y + {r(k**2)}",
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
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )


def _ellipse_to_general(td, cd):
    h, k   = td["center"]
    a2, b2 = td["a2"], td["b2"]
    A, B   = cd["A"], cd["B"]
    af, bf = cd["A_frac"], cd["B_frac"]
    Ar, Br = r(A), r(B)

    prod   = r(a2 * b2)
    exp_x  = r(2 * h);  exp_x2 = r(h**2)
    exp_y  = r(2 * k);  exp_y2 = r(k**2)

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": "Ecuación canónica de la elipse.",
        },
        {
            "title": "Multiplicar por a²·b²",
            "explanation": f"Se elimina el denominador: {a2}·{b2} = {prod}",
            "equation": f"{b2}·(x−{h})² + {a2}·(y−{k})² = {prod}",
        },
        {
            "title": "Expandir (x − h)²",
            "equation": f"(x − {h})² = x² − {exp_x}x + {exp_x2}",
        },
        {
            "title": "Expandir (y − k)²",
            "equation": f"(y − {k})² = y² − {exp_y}y + {exp_y2}",
        },
        {
            "title": "Aplicar coeficientes A y B originales",
            "equation": f"{fraccion_a_texto(*af)}·x² + {fraccion_a_texto(*bf)}·y²",
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
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )


def _hyperbola_to_general(td, cd):
    h, k   = td["center"]
    a2, b2 = td["a2"], td["b2"]
    A, B   = cd["A"], cd["B"]
    af, bf = cd["A_frac"], cd["B_frac"]
    Ar, Br = r(A), r(B)
    orient = td.get("orientation", "horizontal")

    prod   = r(a2 * b2)
    exp_x  = r(2 * h);  exp_x2 = r(h**2)
    exp_y  = r(2 * k);  exp_y2 = r(k**2)

    if orient == "horizontal":
        expanded = f"{b2}·(x−{h})² − {a2}·(y−{k})² = {prod}"
    else:
        expanded = f"{b2}·(y−{k})² − {a2}·(x−{h})² = {prod}"

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": f"Ecuación canónica de la hipérbola ({orient}).",
        },
        {
            "title": "Multiplicar por a²·b²",
            "explanation": f"Se elimina el denominador: {a2}·{b2} = {prod}",
            "equation": expanded,
        },
        {
            "title": "Expandir cuadrados",
            "equation": (
                f"(x−{h})² = x²−{exp_x}x+{exp_x2}  |  "
                f"(y−{k})² = y²−{exp_y}y+{exp_y2}"
            ),
        },
        {
            "title": "Aplicar coeficientes A y B",
            "equation": f"{fraccion_a_texto(*af)}·x² + {fraccion_a_texto(*bf)}·y²",
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
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )


def _parabola_to_general(td, cd):
    h, k   = td["vertex"]
    p      = td["p"]
    orient = td.get("orientation", "vertical")
    af, bf = cd["A_frac"], cd["B_frac"]
    A, B   = cd["A"], cd["B"]
    Ar, Br = r(A), r(B)

    p4     = r(4 * p)
    exp_2h = r(2 * h);  exp_h2 = r(h**2)
    exp_2k = r(2 * k);  exp_k2 = r(k**2)

    steps = [
        {
            "title": "Punto de partida",
            "equation": td["canonical_form"],
            "explanation": f"Ecuación canónica de la parábola ({orient}).",
        },
    ]

    if orient == "vertical":
        coef_str = fraccion_a_texto(*af)
        dy       = r(exp_2h / p4) if p4 else "?"
        fy       = r(exp_h2 / p4 + k) if p4 else "?"
        steps += [
            {
                "title": "Expandir (x − h)²",
                "equation": f"(x − {h})² = x² − {exp_2h}x + {exp_h2}",
            },
            {
                "title": "Despejar y",
                "equation": (
                    f"{p4}·y = x² − {exp_2h}x + {exp_h2}  →  "
                    f"y = x²/{p4} − {dy}x + {fy}"
                ),
            },
            {
                "title": f"Multiplicar por A = {coef_str}",
                "equation": f"{coef_str}·(expansión anterior)",
                "explanation": f"A = {coef_str} = {Ar}",
            },
        ]
    else:
        coef_str = fraccion_a_texto(*bf)
        dx       = r(exp_2k / p4) if p4 else "?"
        fx       = r(exp_k2 / p4 + h) if p4 else "?"
        steps += [
            {
                "title": "Expandir (y − k)²",
                "equation": f"(y − {k})² = y² − {exp_2k}y + {exp_k2}",
            },
            {
                "title": "Despejar x",
                "equation": (
                    f"{p4}·x = y² − {exp_2k}y + {exp_k2}  →  "
                    f"x = y²/{p4} − {dx}y + {fx}"
                ),
            },
            {
                "title": f"Multiplicar por B = {coef_str}",
                "equation": f"{coef_str}·(expansión anterior)",
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
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )