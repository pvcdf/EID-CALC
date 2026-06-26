# conicas-rut/core/conicas/conic_classifier.py

#Clasificación de cónicas a partir de los coeficientes de la ecuación general:

#Ax² + By² + Cx + Dy + E = 0
#Reglas:
#- Parábola: exactamente uno entre A o B es cero.
#- Circunferencia: A = B, ambos no nulos.
#- Elipse: A y B tienen el mismo signo y A ≠ B.
#- Hipérbola: A y B tienen signos opuestos.

from core.utils.result_models import (
    build_success,
    build_error,
    conic_name_es,
)


def _fraccion_a_texto(frac: tuple[int, int]) -> str:
    num, den = frac

    if den == 1:
        return str(num)

    return f"{num}/{den}"

# Cruzamos las fracciones para saber si son iguales sin perder precision
def _fracciones_iguales(frac_a: tuple[int, int], frac_b: tuple[int, int]) -> bool:
    a_num, a_den = frac_a
    b_num, b_den = frac_b

    return a_num * b_den == b_num * a_den


def _signo_fraccion(frac: tuple[int, int]) -> int:
    num, den = frac
    value = num * den

    if value > 0:
        return 1

    if value < 0:
        return -1

    return 0

# Clasifica la conica comparando los coeficientes A y B
def classify_conic(coefficients: dict) -> dict:
    if not isinstance(coefficients, dict) or not coefficients.get("valid"):
        return build_error(
            error="Coeficientes inválidos: no se puede clasificar la cónica."
        )

    data = coefficients["data"]

    A = data["A"]
    B = data["B"]
    C = data["C"]
    D = data["D"]
    E = data["E"]

    A_frac = data.get("A_frac")
    B_frac = data.get("B_frac")

    if not A_frac or not B_frac:
        return build_error(
            error="Faltan fracciones exactas A_frac y B_frac para clasificar la cónica.",
            data=data,
        )

    A_sign = _signo_fraccion(A_frac)
    B_sign = _signo_fraccion(B_frac)
    same_value = _fracciones_iguales(A_frac, B_frac)

    A_text = _fraccion_a_texto(A_frac)
    B_text = _fraccion_a_texto(B_frac)

    adjustments = data.get("adjustments", [])
    equation_str = data.get("equation_str", "")

    steps: list[dict] = [{
        "title": "Identificación de coeficientes",
        "explanation": f"A = {A_text}   B = {B_text}   C = {C}   D = {D}   E = {E}",
        "equation": equation_str,
    }]
    # Si falta A o B es parabola si o si
    if A_sign == 0 or B_sign == 0:
        if A_sign == 0 and B_sign == 0:
            return build_error(
                error="A y B son ambos cero: ecuación degenerada.",
                steps=steps,
                data={
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "E": E,
                    "A_frac": A_frac,
                    "B_frac": B_frac,
                },
            )

        missing_term = "x²" if A_sign == 0 else "y²"

        steps.append({
            "title": "Verificación de coeficientes cuadráticos",
            "explanation": (
                f"El coeficiente del término {missing_term} es cero. "
                "Cuando exactamente uno de los coeficientes cuadráticos es nulo, "
                "la ecuación corresponde a una parábola."
            ),
        })

        steps.append({
            "title": "Conclusión",
            "explanation": "La ecuación corresponde a una Parábola.",
        })

        conic_type = "parabola"

        return build_success(
            conic_type=conic_type,
            explanation="Exactamente uno de los coeficientes cuadráticos es cero.",
            steps=steps,
            data={
                "conic_name_es": conic_name_es(conic_type),
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
                "A_frac": A_frac,
                "B_frac": B_frac,
                "adjustments": adjustments,
                "equation_str": equation_str,
            },
        )
    # Si A y B son exactamente iguales es un circulo
    if same_value: 
        steps.append({
            "title": "Comparación A vs B",
            "explanation": (
                f"A = {A_text} y B = {B_text} son iguales. "
                "Cuando ambos coeficientes cuadráticos son iguales y no nulos, "
                "la cónica se clasifica como circunferencia."
            ),
        })

        if A_sign < 0:
            steps.append({
                "title": "Advertencia — coeficientes negativos",
                "explanation": (
                    f"A = B = {A_text} < 0. La transformación canónica debe verificar "
                    "si existen puntos reales o si corresponde a una circunferencia imaginaria."
                ),
            })

        steps.append({
            "title": "Conclusión",
            "explanation": "La ecuación corresponde a una Circunferencia.",
        })

        conic_type = "circle"

        return build_success(
            conic_type=conic_type,
            explanation="A y B son iguales y ambos son distintos de cero.",
            steps=steps,
            data={
                "conic_name_es": conic_name_es(conic_type),
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
                "A_frac": A_frac,
                "B_frac": B_frac,
                "adjustments": adjustments,
                "equation_str": equation_str,
            },
        )
    # Si tienen mismo signo pero distinto valor es elipse
    if A_sign == B_sign:
        steps.append({
            "title": "Comparación de signos A y B",
            "explanation": (
                f"A = {A_text} y B = {B_text} tienen el mismo signo, "
                "pero son distintos. Esto genera una curva cerrada no circular."
            ),
        })

        steps.append({
            "title": "Conclusión",
            "explanation": "La ecuación corresponde a una Elipse.",
        })

        conic_type = "ellipse"

        return build_success(
            conic_type=conic_type,
            explanation="A y B tienen el mismo signo y son distintos.",
            steps=steps,
            data={
                "conic_name_es": conic_name_es(conic_type),
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
                "A_frac": A_frac,
                "B_frac": B_frac,
                "adjustments": adjustments,
                "equation_str": equation_str,
            },
        )
    # Si son de distinto signo es hiperbola
    if A_sign != B_sign:
        steps.append({
            "title": "Comparación de signos A y B",
            "explanation": (
                f"A = {A_text} y B = {B_text} tienen signos opuestos. "
                "Coeficientes cuadráticos con signos contrarios generan una hipérbola."
            ),
        })

        steps.append({
            "title": "Conclusión",
            "explanation": "La ecuación corresponde a una Hipérbola.",
        })

        conic_type = "hyperbola"

        return build_success(
            conic_type=conic_type,
            explanation="Los coeficientes cuadráticos tienen signos opuestos.",
            steps=steps,
            data={
                "conic_name_es": conic_name_es(conic_type),
                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,
                "A_frac": A_frac,
                "B_frac": B_frac,
                "adjustments": adjustments,
                "equation_str": equation_str,
            },
        )

    return build_error(
        error="No fue posible clasificar la cónica.",
        steps=steps,
        data={
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
            "A_frac": A_frac,
            "B_frac": B_frac,
        },
    )