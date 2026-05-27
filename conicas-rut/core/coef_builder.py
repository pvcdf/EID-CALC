from core.result_models import build_success, build_error


#  Utilidades de fracciones
def maximo_comun_divisor(a: int, b: int) -> int:
    # Calcula el MCD de dos enteros usando el algoritmo de Euclides.
    # Se usa para reducir la fracción A o B a su mínima expresión.
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a if a != 0 else 1


def simplificar_fraccion(numerator: int, denominator: int) -> tuple:
    # Reduce la fracción numerator/denominator usando el MCD.
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
    # Convierte una fracción (num, den) a string legible.
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def ecuacion_a_texto(A_frac, B_frac, C: int, D: int, E: int) -> str:
    # Construye el string de la ecuación general Ax²+By²+Cx+Dy+E=0
    # omitiendo los términos con coeficiente cero.
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


# ─────────────────────────────────────────────
#  Función principal
# ─────────────────────────────────────────────

def build_coefficients(rut_data: dict) -> dict:

    if (
        not isinstance(rut_data, dict)
        or not rut_data.get("valid")
    ):

        return build_error(
            error=(
                "RUT inválido: "
                "no se pueden construir coeficientes"
            )
        )

    steps = []
    adjustments_applied = []

    # Ahora los datos vienen dentro de data
    data = rut_data["data"]
    nd = data["named_digits"]

    v = data["v"]
    d1 = nd["d1"]; d2 = nd["d2"]; d3 = nd["d3"]; d4 = nd["d4"]
    d5 = nd["d5"]; d6 = nd["d6"]; d7 = nd["d7"]; d8 = nd["d8"]

    #  PASO 1 — Coeficientes base
    steps.append("PASO 1: Coeficientes base ══")
    steps.append(
        f"Dígitos: d1={d1} d2={d2} d3={d3} d4={d4} "
        f"d5={d5} d6={d6} d7={d7} d8={d8}"
    )
    steps.append(f"Variable auxiliar v = {v}  (derivada del DV '{data['dv_input']}')")
    steps.append(" ")

    # A = (d1 + d2) / v
    A_num, A_den, A_val = simplificar_fraccion(d1 + d2, v)
    steps.append(f"A = (d1 + d2) / v")
    steps.append(f"A = ({d1} + {d2}) / {v}")
    steps.append(f"A = {d1 + d2} / {v}  →  simplificado: {fraccion_a_texto(A_num, A_den)}  =  {A_val:.6f}")
    steps.append(" ")

    # B = (d3 + d4) / v
    B_num, B_den, B_val = simplificar_fraccion(d3 + d4, v)
    steps.append(f"B = (d3 + d4) / v")
    steps.append(f"B = ({d3} + {d4}) / {v}")
    steps.append(f"B = {d3 + d4} / {v}  →  simplificado: {fraccion_a_texto(B_num, B_den)}  =  {B_val:.6f}")
    steps.append(" ")

    # C = -(d5 + d6)   ← entero, sin denominador
    C = -(d5 + d6)
    steps.append(f"C = -(d5 + d6) = -({d5} + {d6}) = {C}")

    # D = -(d7 + d8)   ← entero, sin denominador
    D = -(d7 + d8)
    steps.append(f"D = -(d7 + d8) = -({d7} + {d8}) = {D}")

    # E = d1 + d3 + d5 + d7   ← entero
    E = d1 + d3 + d5 + d7
    steps.append(f"E = d1 + d3 + d5 + d7 = {d1} + {d3} + {d5} + {d7} = {E}")

    #  PASO 2 — Ajustes para variedad de cónicas

    steps.append(" ")
    steps.append("PASO 2: Ajustes para variedad de cónicas ══")

    # ── Regla 1: d8 impar → B = -B  (hipérbola) ──────────────────────
    steps.append(f"\n[Regla 1] d8 = {d8} → {'impar' if d8 % 2 != 0 else 'par'}")
    if d8 % 2 != 0:
        B_num = -B_num          # solo cambia el signo del numerador
        B_val = -B_val
        steps.append(f"  d8 es impar → B = -B = {fraccion_a_texto(B_num, B_den)}  ({B_val:.6f})")
        adjustments_applied.append("d8_impar: B negado")
    else:
        steps.append(f"  d8 es par → B no cambia")

    # ── Regla 2: d1 == d2 → B = A  (circunferencia) ──────────────────
    steps.append(f"\n[Regla 2] d1 = {d1}, d2 = {d2} → {'iguales' if d1 == d2 else 'distintos'}")
    if d1 == d2:
        B_num, B_den, B_val = A_num, A_den, A_val
        steps.append(f"  d1 == d2 → B = A = {fraccion_a_texto(B_num, B_den)}  ({B_val:.6f})")
        adjustments_applied.append("d1==d2: B igualado a A")
    else:
        steps.append(f"  d1 ≠ d2 → B no cambia")

    # ── Regla 3: (d5+d6) múltiplo de 3 → parábola ────────────────────
    suma_56 = d5 + d6
    steps.append(f"\n[Regla 3] d5 + d6 = {d5} + {d6} = {suma_56}  →  {suma_56} % 3 = {suma_56 % 3}")
    if suma_56 % 3 == 0:
        steps.append(f"  {suma_56} es múltiplo de 3 → se fuerza parábola")
        steps.append(f"  d7 = {d7} → {'par' if d7 % 2 == 0 else 'impar'}")
        if d7 % 2 == 0:
            B_num, B_den, B_val = 0, 1, 0.0
            steps.append("  d7 es par → B = 0  (parábola de eje vertical)")
            adjustments_applied.append("parabola_vertical: B=0")
        else:
            A_num, A_den, A_val = 0, 1, 0.0
            steps.append("  d7 es impar → A = 0  (parábola de eje horizontal)")
            adjustments_applied.append("parabola_horizontal: A=0")
    else:
        steps.append(f"  {suma_56} no es múltiplo de 3 → sin ajuste de parábola")

    #  PASO 3 — Resumen final

    steps.append(" ")
    steps.append("PASO 3: Coeficientes finales ══")
    steps.append(f"A = {fraccion_a_texto(A_num, A_den)}  ({A_val:.6f})")
    steps.append(f"B = {fraccion_a_texto(B_num, B_den)}  ({B_val:.6f})")
    steps.append(f"C = {C}")
    steps.append(f"D = {D}")
    steps.append(f"E = {E}")

    eq_str = ecuacion_a_texto((A_num, A_den), (B_num, B_den), C, D, E)
    steps.append(f"\nEcuación general:\n  {eq_str}")

    if adjustments_applied:
        steps.append("\nAjustes aplicados:")
        for adj in adjustments_applied:
            steps.append(f"  • {adj}")
    else:
        steps.append("\nNo se aplicó ningún ajuste especial.")

    return build_success(
        explanation=(
            "Los coeficientes de la ecuación "
            "fueron generados correctamente."
        ),
        steps=steps,
        data={
            # Valores numéricos
            "A": A_val,
            "B": B_val,
            "C": C,
            "D": D,
            "E": E,

            # Fracciones exactas
            "A_frac": (A_num, A_den),
            "B_frac": (B_num, B_den),

            # Información auxiliar
            "adjustments": adjustments_applied,
            "equation_str": eq_str,

            # Datos heredados del RUT
            "digits": nd,
            "v": v,
        }
    )