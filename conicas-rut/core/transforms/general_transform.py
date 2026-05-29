# conicas-rut/core/transforms/general_transform.py

from core.result_models import build_success, build_error
from core.coef_builder import fraccion_a_texto


def transform_to_general(conic_type: str, transform_data: dict,
                          coef_data: dict) -> dict:
    """
    Reconstruye la ecuación general desde la forma canónica.
    Recibe los datos del transform y los coeficientes originales.
    """
    try:
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


def _circle_to_general(td: dict, cd: dict) -> dict:
    h, k  = td["center"]
    r2    = td["radius_squared"]
    A, B  = cd["A"], cd["B"]
    af, bf = cd["A_frac"], cd["B_frac"]

    steps = []
    steps.append({
        "title": "Punto de partida",
        "equation": td["canonical_form"],
        "explanation": "Ecuación canónica de la circunferencia.",
    })
    steps.append({
        "title": "Expandir (x − h)²",
        "equation": f"(x − {h})² = x² − {2*h}x + {round(h**2, 2)}",
    })
    steps.append({
        "title": "Expandir (y − k)²",
        "equation": f"(y − {k})² = y² − {2*k}y + {round(k**2, 2)}",
    })
    steps.append({
        "title": f"Multiplicar por A = {fraccion_a_texto(*af)}",
        "equation": (
            f"{fraccion_a_texto(*af)}·x² "
            f"− {round(A*2*h,2)}x "
            f"+ {round(A*h**2,2)}"
        ),
    })
    steps.append({
        "title": f"Multiplicar por B = {fraccion_a_texto(*bf)}",
        "equation": (
            f"{fraccion_a_texto(*bf)}·y² "
            f"− {round(B*2*k,2)}y "
            f"+ {round(B*k**2,2)}"
        ),
    })
    steps.append({
        "title": "Restar r² y agrupar = 0",
        "equation": cd.get("equation_str", "—"),
        "result": "Forma general recuperada",
    })
    return build_success(
        conic_type="circle",
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )


def _ellipse_to_general(td: dict, cd: dict) -> dict:
    h, k   = td["center"]
    a2, b2 = td["a2"], td["b2"]
    A, B   = cd["A"], cd["B"]
    af, bf = cd["A_frac"], cd["B_frac"]

    steps = []
    steps.append({
        "title": "Punto de partida",
        "equation": td["canonical_form"],
        "explanation": "Ecuación canónica de la elipse.",
    })
    steps.append({
        "title": "Multiplicar toda la ecuación por a²·b²",
        "explanation": f"Se elimina el denominador multiplicando por {a2}·{b2} = {round(a2*b2,2)}",
        "equation": f"{b2}·(x−{h})² + {a2}·(y−{k})² = {round(a2*b2,2)}",
    })
    steps.append({
        "title": "Expandir (x − h)²",
        "equation": f"(x − {h})² = x² − {2*h}x + {round(h**2,2)}",
    })
    steps.append({
        "title": "Expandir (y − k)²",
        "equation": f"(y − {k})² = y² − {2*k}y + {round(k**2,2)}",
    })
    steps.append({
        "title": "Aplicar coeficientes A y B originales",
        "equation": (
            f"{fraccion_a_texto(*af)}·x² "
            f"+ {fraccion_a_texto(*bf)}·y²"
        ),
        "explanation": f"A={fraccion_a_texto(*af)}  B={fraccion_a_texto(*bf)}",
    })
    steps.append({
        "title": "Agrupar todos los términos = 0",
        "equation": cd.get("equation_str", "—"),
        "result": "Forma general recuperada",
    })
    return build_success(
        conic_type="ellipse",
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )


def _hyperbola_to_general(td: dict, cd: dict) -> dict:
    h, k   = td["center"]
    a2, b2 = td["a2"], td["b2"]
    A, B   = cd["A"], cd["B"]
    af, bf = cd["A_frac"], cd["B_frac"]
    orient = td.get("orientation", "horizontal")

    steps = []
    steps.append({
        "title": "Punto de partida",
        "equation": td["canonical_form"],
        "explanation": f"Ecuación canónica de la hipérbola ({orient}).",
    })
    steps.append({
        "title": "Multiplicar por a²·b²",
        "explanation": f"Se elimina el denominador: {a2}·{b2} = {round(a2*b2,2)}",
        "equation": (
            f"{b2}·(x−{h})² − {a2}·(y−{k})² = {round(a2*b2,2)}"
            if orient == "horizontal"
            else f"{b2}·(y−{k})² − {a2}·(x−{h})² = {round(a2*b2,2)}"
        ),
    })
    steps.append({
        "title": "Expandir cuadrados",
        "equation": (
            f"(x−{h})² = x²−{2*h}x+{round(h**2,2)}  |  "
            f"(y−{k})² = y²−{2*k}y+{round(k**2,2)}"
        ),
    })
    steps.append({
        "title": "Aplicar coeficientes A y B",
        "equation": (
            f"{fraccion_a_texto(*af)}·x² "
            f"+ {fraccion_a_texto(*bf)}·y²"
        ),
        "explanation": f"A={fraccion_a_texto(*af)}  B={fraccion_a_texto(*bf)}",
    })
    steps.append({
        "title": "Agrupar todos los términos = 0",
        "equation": cd.get("equation_str", "—"),
        "result": "Forma general recuperada",
    })
    return build_success(
        conic_type="hyperbola",
        explanation="Canónica → General completada.",
        steps=steps,
        data={"equation_str": cd.get("equation_str", "—")},
    )


def _parabola_to_general(td: dict, cd: dict) -> dict:
    h, k   = td["vertex"]
    p      = td["p"]
    orient = td.get("orientation", "vertical")
    af, bf = cd["A_frac"], cd["B_frac"]

    steps = []
    steps.append({
        "title": "Punto de partida",
        "equation": td["canonical_form"],
        "explanation": f"Ecuación canónica de la parábola ({orient}).",
    })
    if orient == "vertical":
        steps.append({
            "title": "Expandir (x − h)²",
            "equation": f"(x − {h})² = x² − {2*h}x + {round(h**2,2)}",
        })
        steps.append({
            "title": "Despejar y",
            "equation": f"y = x²/{round(4*p,2)} − {round(2*h/(4*p),2)}x + {round(h**2/(4*p)+k,2)}",
        })
    else:
        steps.append({
            "title": "Expandir (y − k)²",
            "equation": f"(y − {k})² = y² − {2*k}y + {round(k**2,2)}",
        })
        steps.append({
            "title": "Despejar x",
            "equation": f"x = y²/{round(4*p,2)} − {round(2*k/(4*p),2)}y + {round(k**2/(4*p)+h,2)}",
        })
    steps.append({
        "title": "Multiplicar por coeficiente",
        "equation": (
            f"{fraccion_a_texto(*af)}·(expansión)"
            if orient == "vertical"
            else f"{fraccion_a_texto(*bf)}·(expansión)"
        ),
    })
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