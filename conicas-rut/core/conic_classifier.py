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

    # ─────────────────────────────────────────────
    # Validación de entrada
    # ─────────────────────────────────────────────

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

    # ─────────────────────────────────────────────
    # Extraer datos
    # ─────────────────────────────────────────────

    data = coefficients["data"]

    A = data["A"]
    B = data["B"]
    C = data["C"]
    D = data["D"]
    E = data["E"]

    adjustments = data.get(
        "adjustments",
        []
    )

    steps = []

    steps.append(
        "Se identifican los coeficientes principales:"
    )

    steps.append(
        f"A = {A}"
    )

    steps.append(
        f"B = {B}"
    )

    # ─────────────────────────────────────────────
    # Parábola
    # ─────────────────────────────────────────────

    if A == 0 or B == 0:

        steps.append(
            "Uno de los coeficientes cuadráticos es cero."
        )

        if A == 0:

            steps.append(
                "El término x² desaparece."
            )

        if B == 0:

            steps.append(
                "El término y² desaparece."
            )

        steps.append(
            "La ecuación corresponde a una parábola."
        )

        conic_type = "parabola"

        return build_success(
            conic_type=conic_type,
            explanation=(
                "Uno de los coeficientes cuadráticos es cero."
            ),
            steps=steps,
            data={
                "conic_name_es": conic_name_es(
                    conic_type
                ),

                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,

                "adjustments": adjustments,
            }
        )

    # ─────────────────────────────────────────────
    # Circunferencia
    # ─────────────────────────────────────────────

    if A == B:

        steps.append(
            "Los coeficientes A y B son iguales."
        )

        steps.append(
            "Ambos términos cuadráticos "
            "tienen el mismo peso."
        )

        steps.append(
            "La ecuación corresponde "
            "a una circunferencia."
        )

        conic_type = "circle"

        return build_success(
            conic_type=conic_type,
            explanation=(
                "A y B son iguales "
                "y tienen el mismo signo."
            ),
            steps=steps,
            data={
                "conic_name_es": conic_name_es(
                    conic_type
                ),

                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,

                "adjustments": adjustments,
            }
        )

    # ─────────────────────────────────────────────
    # Elipse
    # ─────────────────────────────────────────────

    if A * B > 0:

        steps.append(
            "A y B tienen el mismo signo."
        )

        steps.append(
            "Los coeficientes cuadráticos "
            "son distintos."
        )

        steps.append(
            "La ecuación corresponde "
            "a una elipse."
        )

        conic_type = "ellipse"

        return build_success(
            conic_type=conic_type,
            explanation=(
                "A y B tienen el mismo signo "
                "y son distintos."
            ),
            steps=steps,
            data={
                "conic_name_es": conic_name_es(
                    conic_type
                ),

                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,

                "adjustments": adjustments,
            }
        )

    # ─────────────────────────────────────────────
    # Hipérbola
    # ─────────────────────────────────────────────

    if A * B < 0:

        steps.append(
            "A y B tienen signos opuestos."
        )

        steps.append(
            "La ecuación corresponde "
            "a una hipérbola."
        )

        conic_type = "hyperbola"

        return build_success(
            conic_type=conic_type,
            explanation=(
                "Los coeficientes cuadráticos "
                "tienen signos opuestos."
            ),
            steps=steps,
            data={
                "conic_name_es": conic_name_es(
                    conic_type
                ),

                "A": A,
                "B": B,
                "C": C,
                "D": D,
                "E": E,

                "adjustments": adjustments,
            }
        )

    # ─────────────────────────────────────────────
    # Error
    # ─────────────────────────────────────────────

    return build_error(
        error="No fue posible clasificar la cónica.",
        steps=steps,
        data={
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
        }
    )