"""
Transformación canónica de circunferencia

"""

from core.result_models import build_success, build_error


def transform_circle(A, B, C, D, E):

    steps = []
    try:
        steps.append("Se agrupan términos en x e y.")

        h = -C / (2 * A)
        k = -D / (2 * B)

        steps.append("Se completa cuadrado en x.")
        steps.append("Se completa cuadrado en y.")
        radius_squared = ( h**2 + k**2 -E)

        if radius_squared <= 0:
            return build_error(
                error="El radio calculado no es válido.",
                steps=steps)

        radius = radius_squared ** 0.5
        canonical = (
            f"(x - {h})² + "
            f"(y - {k})² = {radius_squared}"
        )

        steps.append("Se obtiene la forma canónica.")
        return build_success(
            conic_type="circle",
            explanation=(
                "La circunferencia fue transformada correctamente."
            ),
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (h, k),
                "radius": radius,
                "radius_squared": radius_squared,
            }
        )

    except Exception as ex:

        return build_error(
            error=str(ex),
            steps=steps
        )