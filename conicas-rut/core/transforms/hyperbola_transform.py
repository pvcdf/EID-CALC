"""
Transformación canónica de hipérbola

"""

from core.result_models import build_success, build_error


def transform_hyperbola(A, B, C, D, E):

    steps = []
    try:
        steps.append("Se identifican coeficientes con signos opuestos.")

        h = -C / (2 * A)
        k = -D / (2 * B)

        steps.append("Se completa cuadrado en x.")
        steps.append("Se completa cuadrado en y.")

        constant = ( -E + (C**2) / (4 * A) + (D**2) / (4 * B))

        if constant == 0:
            return build_error(
                error="No se pudo obtener la hipérbola.",
                steps=steps
            )

        a2 = abs(constant / A)
        b2 = abs(constant / B)

        a = a2 ** 0.5
        b = b2 ** 0.5
        c = (a2 + b2) ** 0.5

        # Determinar orientación
        if A > 0:

            canonical = (
                f"(x - {h})²/{a2} - "
                f"(y - {k})²/{b2} = 1"
            )

            orientation = "horizontal"

        else:

            canonical = (
                f"(y - {k})²/{b2} - "
                f"(x - {h})²/{a2} = 1"
            )

            orientation = "vertical"

        steps.append("Se obtiene la forma canónica.")

        return build_success(
            conic_type="hyperbola",
            explanation=(
                "La hipérbola fue transformada correctamente."
            ),
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (h, k),
                "orientation": orientation,
                "a": a,
                "b": b,
                "c": c,
                "a2": a2,
                "b2": b2,
            }
        )

    except Exception as ex:

        return build_error(
            error=str(ex),
            steps=steps
        )