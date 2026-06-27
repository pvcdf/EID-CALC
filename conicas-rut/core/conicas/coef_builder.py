# conicas-rut/core/conicas/coef_builder.py

from core.utils.result_models import build_success, build_error


# ── Utilidades para fracciones ─────────────────────────────────────────────

def maximo_comun_divisor(a: int, b: int) -> int:
    """Calcula el MCD usando el algoritmo de Euclides."""
    a = abs(a)
    b = abs(b)

    while b:
        a, b = b, a % b

    return a if a != 0 else 1


def simplificar_fraccion(numerator: int, denominator: int) -> tuple[int, int, float]:
    """Reduce una fracción y también devuelve su valor decimal."""
    if denominator == 0:
        raise ValueError("Denominador cero al simplificar fracción.")

    sign = -1 if numerator * denominator < 0 else 1
    num = abs(numerator)
    den = abs(denominator)

    common = maximo_comun_divisor(num, den)
    num //= common
    den //= common

    final_num = sign * num

    return final_num, den, final_num / den


def fraccion_a_texto(num: int, den: int) -> str:
    """Convierte una fracción a texto para mostrarla en la interfaz."""
    if den == 1:
        return str(num)

    return f"{num}/{den}"


# ── Formateo de ecuación general ───────────────────────────────────────────

def _agregar_termino(terms: list[str], coefficient: int | str, variable: str = "") -> None:
    """Agrega un término algebraico manteniendo signos limpios."""
    coef_text = str(coefficient)

    if coef_text.startswith("-"):
        terms.append(f"- {coef_text[1:]}{variable}")
    else:
        if terms:
            terms.append(f"+ {coef_text}{variable}")
        else:
            terms.append(f"{coef_text}{variable}")


def ecuacion_a_texto(
    A_frac: tuple[int, int],
    B_frac: tuple[int, int],
    C: int,
    D: int,
    E: int,
) -> str:
    """Construye el texto de Ax² + By² + Cx + Dy + E = 0."""
    terms: list[str] = []

    a_num, a_den = A_frac
    b_num, b_den = B_frac

    if a_num != 0:
        _agregar_termino(terms, fraccion_a_texto(a_num, a_den), "x²")

    if b_num != 0:
        _agregar_termino(terms, fraccion_a_texto(b_num, b_den), "y²")

    if C != 0:
        _agregar_termino(terms, C, "x")

    if D != 0:
        _agregar_termino(terms, D, "y")

    if E != 0:
        _agregar_termino(terms, E)

    if not terms:
        terms.append("0")

    return " ".join(terms) + " = 0"


# ── Construcción de coeficientes ───────────────────────────────────────────
# Ecuación general usada:
# Ax² + By² + Cx + Dy + E = 0

def build_coefficients(rut_data: dict) -> dict:
    """Genera los coeficientes A, B, C, D y E desde los dígitos del RUT."""
    if not isinstance(rut_data, dict) or not rut_data.get("valid"):
        return build_error(
            error="RUT inválido: no se pueden construir coeficientes."
        )

    steps: list[dict] = []              # pasos mostrados en la interfaz
    adjustments_applied: list[str] = [] # reglas especiales aplicadas

    data = rut_data["data"]
    nd = data["named_digits"]  # dígitos del RUT etiquetados como d1...d8
    v = data["v"]              # valor auxiliar usado como divisor

    d1 = nd["d1"]
    d2 = nd["d2"]
    d3 = nd["d3"]
    d4 = nd["d4"]
    d5 = nd["d5"]
    d6 = nd["d6"]
    d7 = nd["d7"]
    d8 = nd["d8"]

    steps.append({
        "title": "Paso 1 — Coeficientes base",
        "explanation": (
            f"d1={d1}  d2={d2}  d3={d3}  d4={d4}  "
            f"d5={d5}  d6={d6}  d7={d7}  d8={d8}  |  v={v}"
        ),
    })

    # Coeficientes cuadráticos: determinan el tipo principal de cónica.
    A_num, A_den, A_val = simplificar_fraccion(d1 + d2, v)
    steps.append({
        "title": "A = (d1 + d2) / v",
        "equation": f"({d1} + {d2}) / {v} = {d1 + d2}/{v}",
        "result": fraccion_a_texto(A_num, A_den),
    })

    B_num, B_den, B_val = simplificar_fraccion(d3 + d4, v)
    steps.append({
        "title": "B = (d3 + d4) / v",
        "equation": f"({d3} + {d4}) / {v} = {d3 + d4}/{v}",
        "result": fraccion_a_texto(B_num, B_den),
    })

    # Coeficientes lineales y término independiente.
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

    steps.append({
        "title": "Paso 2 — Ajustes para variedad de cónicas",
        "explanation": (
            "Se aplican las reglas especiales en orden. "
            "Si una regla se cumple, modifica los coeficientes antes de clasificar."
        ),
    })

    # Regla 1: si d8 es impar, se invierte B para permitir hipérbolas.
    if d8 % 2 != 0:
        B_num = -B_num
        B_val = -B_val
        adjustments_applied.append("d8_impar: B negado")

    steps.append({
        "title": f"Regla 1 — d8 = {d8} ({'impar' if d8 % 2 != 0 else 'par'})",
        "explanation": "d8 impar → B = −B" if d8 % 2 != 0 else "d8 par → B no cambia",
        "result": fraccion_a_texto(B_num, B_den) if d8 % 2 != 0 else None,
    })

    # Regla 2: si A y B quedan iguales, la cónica se fuerza a circunferencia.
    if d1 == d2:
        B_num = A_num
        B_den = A_den
        B_val = A_val
        adjustments_applied.append("d1==d2: B igualado a A")

    steps.append({
        "title": f"Regla 2 — d1={d1}, d2={d2} ({'iguales' if d1 == d2 else 'distintos'})",
        "explanation": "d1 == d2 → B = A" if d1 == d2 else "d1 ≠ d2 → B no cambia",
        "result": fraccion_a_texto(B_num, B_den) if d1 == d2 else None,
    })

    suma_56 = d5 + d6

    # Regla 3: si d5+d6 es múltiplo de 3, se anula A o B para generar parábola.
    if suma_56 % 3 == 0:
        if d7 % 2 == 0:
            B_num = 0
            B_den = 1
            B_val = 0.0
            adjustments_applied.append("parabola_vertical: B=0")
            parabola_result = "B = 0"
            parabola_orientation = "vertical"
        else:
            A_num = 0
            A_den = 1
            A_val = 0.0
            adjustments_applied.append("parabola_horizontal: A=0")
            parabola_result = "A = 0"
            parabola_orientation = "horizontal"
    else:
        parabola_result = None
        parabola_orientation = None

    steps.append({
        "title": (
            f"Regla 3 — d5+d6 = {suma_56} "
            f"({'múltiplo de 3' if suma_56 % 3 == 0 else 'no múltiplo de 3'})"
        ),
        "explanation": (
            f"Se genera una parábola de eje {parabola_orientation}."
            if suma_56 % 3 == 0
            else "No se aplica ajuste de parábola."
        ),
        "result": parabola_result,
    })

    eq_str = ecuacion_a_texto(
        (A_num, A_den),
        (B_num, B_den),
        C,
        D,
        E,
    )

    steps.append({
        "title": "Paso 3 — Coeficientes finales",
        "explanation": (
            f"A={fraccion_a_texto(A_num, A_den)}  "
            f"B={fraccion_a_texto(B_num, B_den)}  "
            f"C={C}  D={D}  E={E}"
        ),
        "equation": eq_str,
    })

    return build_success(
        explanation="Los coeficientes de la ecuación fueron generados correctamente.",
        steps=steps,
        data={
            "A": A_val,                         # valor decimal de A
            "B": B_val,                         # valor decimal de B
            "C": C,                             # coeficiente lineal de x
            "D": D,                             # coeficiente lineal de y
            "E": E,                             # término independiente
            "A_frac": (A_num, A_den),           # fracción exacta de A
            "B_frac": (B_num, B_den),           # fracción exacta de B
            "adjustments": adjustments_applied, # reglas aplicadas
            "equation_str": eq_str,             # ecuación general en texto
            "digits": nd,                       # dígitos d1...d8
            "v": v,                             # valor auxiliar del RUT
        },
    )