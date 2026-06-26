# conicas-rut/core/conicas/transforms/canonical_transform.py

from core.conicas.transforms.circle_transform import transform_circle
from core.conicas.transforms.elipse_transform import transform_ellipse
from core.conicas.transforms.hyperbola_transform import transform_hyperbola
from core.conicas.transforms.parabola_transform import transform_parabola
from core.utils.result_models import build_error

def transform_conic(conic_type: str, A, B, C, D, E) -> dict:
    """
    este metodo solo redirige al transformador q corresponde segun el tipo
    """
    if conic_type == "circle":
        # Completacion de cuadrados pal centro del circulo
        return transform_circle(A, B, C, D, E)

    if conic_type == "ellipse":
        # Saca semiejes a y b
        return transform_ellipse(A, B, C, D, E)

    if conic_type == "hyperbola":
        # Revisa el signo para saber donde se abre
        return transform_hyperbola(A, B, C, D, E)

    if conic_type == "parabola":
        # Averigua si falta x^2 o y^2 pa sacar el vertice y foco
        return transform_parabola(A, B, C, D, E)

    return build_error(
        error=f"Tipo de conica no soportado: {conic_type}"
    )