# conicas-rut/core/coef_builder.py

from core.result_models import build_success, build_error


def maximo_comun_divisor(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a if a != 0 else 1


def simplificar_fraccion(numerator: int, denominator: int) -> tuple:
    if denominator == 0:
        raise ValueError("Denominador cero al simplificar fracción")
    sign = -1 if (numerator * denominator < 0) else 1
    num = abs(numerator)
    den = abs(denominator)
    common = maximo_comun_divisor(num, den)
    num //= common
    den //= common
    return (sign * num, den, (sign * num) / den)


def fraccion_a_texto(num: int, den: int) -> str:
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def ecuacion_a_texto(A_frac, B_frac, C: int, D: int, E: int) -> str:
    terms = []
    a_str = fraccion_a_texto(*A_frac)
    b_str = fraccion_a_texto(*B_frac)
    if A_frac[0] != 0:
        terms.append(f"({a_str})x²")
    if B_frac[0] != 0:
        terms.append(f"({b_str})y²")
    if C != 0:
        terms.append(f"({C})x")
    if D != 0:
        terms.append(f"({D})y")
    if E != 0:
        terms.append(str(E))
    if not terms:
        terms.append("0")
    return " + ".join(terms) + " = 0"


def build_coefficients(rut_data: dict) -> dict:

    if not isinstance(rut_data, dict) or not rut_data.get("valid"):
        return build_error(
            error="RUT inválido: no se pueden construir coeficientes"
        )

    steps = []
    adjustments_applied = []

    data = rut_data["data"]
    nd   = data["named_digits"]
    v    = data["v"]

    d1 = nd["d1"]; d2 = nd["d2"]; d3 = nd["d3"]; d4 = nd["d4"]
    d5 = nd["d5"]; d6 = nd["d6"]; d7 = nd["d7"]; d8 = nd["d8"]

    # ── PASO 1: Cálculo base ──────────────────────────────────────────────
    steps.append({
        "title": "Paso 1 — Coeficientes base",
        "explanation": (
            f"d1={d1}  d2={d2}  d3={d3}  d4={d4}  "
            f"d5={d5}  d6={d6}  d7={d7}  d8={d8}  |  v={v}"
        ),
    })

    A_num, A_den, A_val = simplificar_fraccion(d1 + d2, v)
    steps.append({
        "title": "A = (d1 + d2) / v",
        "equation": f"({d1} + {d2}) / {v} = {d1+d2}/{v}",
        "result": fraccion_a_texto(A_num, A_den),
    })

    B_num, B_den, B_val = simplificar_fraccion(d3 + d4, v)
    steps.append({
        "title": "B = (d3 + d4) / v",
        "equation": f"({d3} + {d4}) / {v} = {d3+d4}/{v}",
        "result": fraccion_a_texto(B_num, B_den),
    })

    C = -(d5 + d6)
    steps.append({
        "title": "C = -(d5 + d6)",
        "equation": f"-({d5} + {d6})",
        "result": str(C),
    })

    D = -(d7 + d8)
    steps.append({
        "title": "D = -(d7 + d8)",
        "equation": f"-({d7} + {d8})",
        "result": str(D),
    })

    E = d1 + d3 + d5 + d7
    steps.append({
        "title": "E = d1 + d3 + d5 + d7",
        "equation": f"{d1} + {d3} + {d5} + {d7}",
        "result": str(E),
    })

    # ── PASO 2: Ajustes ───────────────────────────────────────────────────
    steps.append({
        "title": "Paso 2 — Ajustes para variedad de cónicas",
        "explanation": (
            "Se aplican las reglas en orden. "
            "Cada condición es independiente: si aplica, modifica el coeficiente."
        ),
    })

    # ── Regla 1: d8 impar → B = -B ───────────────────────────────────────
    if d8 % 2 != 0:
        B_num = -B_num
        B_val = -B_val
        adjustments_applied.append("d8_impar: B negado")
    steps.append({
        "title": f"Regla 1 — d8 = {d8}  ({'impar' if d8 % 2 != 0 else 'par'})",
        "explanation": "d8 impar → B = −B" if d8 % 2 != 0 else "d8 par → B no cambia",
        "result": fraccion_a_texto(B_num, B_den) if d8 % 2 != 0 else None,
    })

    # ── Regla 2: d1 == d2 → B = A ────────────────────────────────────────
    if d1 == d2:
        B_num, B_den, B_val = A_num, A_den, A_val
        adjustments_applied.append("d1==d2: B igualado a A")
    steps.append({
        "title": f"Regla 2 — d1={d1}, d2={d2}  ({'iguales' if d1 == d2 else 'distintos'})",
        "explanation": "d1 == d2 → B = A" if d1 == d2 else "d1 ≠ d2 → B no cambia",
        "result": fraccion_a_texto(B_num, B_den) if d1 == d2 else None,
    })

    # ── Regla 3: (d5+d6) múltiplo de 3 → parábola ────────────────────────
    suma_56 = d5 + d6
    if suma_56 % 3 == 0:
        if d7 % 2 == 0:
            B_num, B_den, B_val = 0, 1, 0.0
            adjustments_applied.append("parabola_vertical: B=0")
        else:
            A_num, A_den, A_val = 0, 1, 0.0
            adjustments_applied.append("parabola_horizontal: A=0")
    steps.append({
        "title": (
            f"Regla 3 — d5+d6 = {suma_56}  "
            f"({'múltiplo de 3' if suma_56 % 3 == 0 else 'no múltiplo de 3'})"
        ),
        "explanation": (
            f"parábola {'vertical (B=0)' if d7 % 2 == 0 else 'horizontal (A=0)'}"
            if suma_56 % 3 == 0 else "sin ajuste de parábola"
        ),
    })

    # ── PASO 3: Resumen ───────────────────────────────────────────────────
    eq_str = ecuacion_a_texto((A_num, A_den), (B_num, B_den), C, D, E)
    steps.append({
        "title": "Paso 3 — Coeficientes finales",
        "explanation": (
            f"A={fraccion_a_texto(A_num,A_den)}  "
            f"B={fraccion_a_texto(B_num,B_den)}  "
            f"C={C}  D={D}  E={E}"
        ),
        "equation": eq_str,
    })

    return build_success(
        explanation="Los coeficientes de la ecuación fueron generados correctamente.",
        steps=steps,
        data={
            "A":          A_val,
            "B":          B_val,
            "C":          C,
            "D":          D,
            "E":          E,
            "A_frac":     (A_num, A_den),
            "B_frac":     (B_num, B_den),
            "adjustments": adjustments_applied,
            "equation_str": eq_str,
            "digits":     nd,
            "v":          v,
        }
    )