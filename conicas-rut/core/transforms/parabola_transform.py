"""
Transformación canónica de parábola
"""
from core.result_models import build_success, build_error

def transform_parabola(A, B, C, D, E):

    steps = []
    try:
        # Parábola vertical
        if B == 0:
            steps.append("La parábola es vertical porque B = 0.")

            h = -C / (2 * A)
            k = ( -E + (C**2 / (4 * A)) ) / D
            p = D / 4

            canonical = (
                f"(x - {h})² = "
                f"{4*p}(y - {k})"
            )
            orientation = "vertical"


        # Parábola horizontal
        elif A == 0:
            steps.append("La parábola es horizontal porque A = 0.")

            k = -D / (2 * B)
            h = ( -E + (D**2 / (4 * B)) ) / C
            p = C / 4

            canonical = (
                f"(y - {k})² = "
                f"{4*p}(x - {h})"
            )
            orientation = "horizontal"

        else:

            return build_error(
                error="La ecuación no corresponde a una parábola.",
                steps=steps
            )

        steps.append("Se completa cuadrado.")
        steps.append("Se obtiene la forma canónica.")

        return build_success(
            conic_type="parabola",
            explanation=(
                "La parábola fue transformada correctamente."
            ),
            steps=steps,
            data={
                "canonical_form": canonical,
                "orientation": orientation,
                "vertex": (h, k),
                "p": p,
            }
        )

    except Exception as ex:

        return build_error(
            error=str(ex),
            steps=steps
        )