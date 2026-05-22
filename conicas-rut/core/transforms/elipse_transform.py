"""
Transformación canónica de elipse

"""

from core.result_models import build_success, build_error


def transform_ellipse(A, B, C, D, E):

    steps = []
    try:
        steps.append("Se agrupan términos cuadráticos.")

        h = -C / (2 * A)
        k = -D / (2 * B)
        steps.append("Se completa cuadrado en x.")
        steps.append("Se completa cuadrado en y.")

        constant = ( -E + (C**2) / (4 * A) + (D**2) / (4 * B) )

        if constant <= 0:
            return build_error(
                error="No se pudo normalizar la elipse.",
                steps=steps
            )

        a2 = constant / A
        b2 = constant / B

        a = max(a2, b2) ** 0.5
        b = min(a2, b2) ** 0.5
        c = abs(a**2 - b**2) ** 0.5

        canonical = (
            f"(x - {h})²/{a2} + "
            f"(y - {k})²/{b2} = 1"
        )

        steps.append("Se reorganiza la ecuación.")
        steps.append("Se obtiene la forma canónica.")

        return build_success(
            conic_type="ellipse",
            explanation=(
                "La elipse fue transformada correctamente."
            ),
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (h, k),
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