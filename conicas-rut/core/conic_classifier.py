# conicas-rut/core/conic_classifier.py

"""
Usa reglas matemáticas reales basadas en:
- Signos de A y B
- Igualdad de coeficientes
- Coeficientes nulos
"""

from core.result_models import (
    build_success,
    build_error,
    conic_name_es,
)


def classify_conic(coefficients: dict):
    """
    Clasifica una cónica usando los coeficientes
    generados por build_coefficients().
    """

    if (
        not isinstance(coefficients, dict)
        or not coefficients.get("valid")
    ):
        return build_error(
            error=(
                "Coeficientes inválidos: "
                "no se puede clasificar la cónica."
            )
        )

    data = coefficients["data"]

    A = data["A"]
    B = data["B"]
    C = data["C"]
    D = data["D"]
    E = data["E"]

    adjustments = data.get("adjustments", [])

    steps = []
    steps.append({
        "title": "Identificación de coeficientes",
        "explanation": f"A = {A}   B = {B}   C = {C}   D = {D}   E = {E}",
    })

    # ── Parábola ──────────────────────────────────────────────────────────

    if A == 0 or B == 0:
        if A == 0 and B == 0:
            # Caso degenerado 
            return build_error(
                error="A y B son ambos cero: ecuación degenerada.",
                steps=steps,
            )

        which = "x²" if A == 0 else "y²"
        steps.append({
            "title": "Verificación de coeficientes cuadráticos",
            "explanation": (
                f"El coeficiente del término {which} es cero. "
                "Cuando uno de los coeficientes cuadráticos es nulo, "
                "la curva solo se curva en una dirección."
            ),
        })
        steps.append({
            "title": "Conclusión",
            "explanation": "La ecuación corresponde a una Parábola.",
        })

        conic_type = "parabola"
        return build_success(
            conic_type=conic_type,
            explanation="Uno de los coeficientes cuadráticos es cero.",
            steps=steps,
            data={
                "conic_name_es": conic_name_es(conic_type),
                "A": A, "B": B, "C": C, "D": D, "E": E,
                "adjustments": adjustments,
            }
        )

    # ── Circunferencia ────────────────────────────────────────────────────

    if A == B:
        steps.append({
            "title": "Comparación A vs B",
            "explanation": (
                f"A = {A} y B = {B} son iguales. "
                "Cuando ambos coeficientes cuadráticos son iguales, "
                "la curva tiene la misma amplitud en x e y."
            ),
        })

        # Advertir si ambos son negativos (cónica imaginaria posible)
        if A < 0:
            steps.append({
                "title": "Advertencia — coeficientes negativos",
                "explanation": (
                    f"A = B = {A} < 0. La ecuación puede corresponder "
                    "a una circunferencia imaginaria (sin puntos reales). "
                    "Se verificará en la transformación canónica."
                ),
            })

        steps.append({
            "title": "Conclusión",
            "explanation": "La ecuación corresponde a una Circunferencia.",
        })

        conic_type = "circle"
        return build_success(
            conic_type=conic_type,
            explanation="A y B son iguales.",
            steps=steps,
            data={
                "conic_name_es": conic_name_es(conic_type),
                "A": A, "B": B, "C": C, "D": D, "E": E,
                "adjustments": adjustments,
            }
        )

    # ── Elipse ────────────────────────────────────────────────────────────

    if A * B > 0:
        steps.append({
            "title": "Comparación de signos A · B",
            "explanation": (
                f"A = {A} y B = {B} tienen el mismo signo (A · B = {A*B:.2f} > 0). "
                "Coeficientes distintos con igual signo generan una curva cerrada asimétrica."
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
                "A": A, "B": B, "C": C, "D": D, "E": E,
                "adjustments": adjustments,
            }
        )

    # ── Hipérbola ─────────────────────────────────────────────────────────

    if A * B < 0:
        steps.append({
            "title": "Comparación de signos A · B",
            "explanation": (
                f"A = {A} y B = {B} tienen signos opuestos (A · B = {A*B:.2f} < 0). "
                "Coeficientes con signo contrario generan una curva abierta en dos ramas."
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
                "A": A, "B": B, "C": C, "D": D, "E": E,
                "adjustments": adjustments,
            }
        )

    return build_error(
        error="No fue posible clasificar la cónica.",
        steps=steps,
        data={"A": A, "B": B, "C": C, "D": D, "E": E}
    )