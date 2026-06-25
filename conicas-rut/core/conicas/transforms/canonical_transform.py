# conicas-rut/core/conicas/transforms/canonical_transform.py

from core.conicas.transforms.circle_transform import transform_circle
from core.conicas.transforms.elipse_transform import transform_ellipse
from core.conicas.transforms.hyperbola_transform import transform_hyperbola
from core.conicas.transforms.parabola_transform import transform_parabola
from core.utils.result_models import build_error


def transform_conic(conic_type: str, A, B, C, D, E) -> dict:
    """
    Redirige la transformación canónica según el tipo de cónica.
    """
    if conic_type == "circle":
        return transform_circle(A, B, C, D, E)

    if conic_type == "ellipse":
        return transform_ellipse(A, B, C, D, E)

    if conic_type == "hyperbola":
        return transform_hyperbola(A, B, C, D, E)

    if conic_type == "parabola":
        return transform_parabola(A, B, C, D, E)

    return build_error(
        error=f"Tipo de cónica no soportado: {conic_type}"
    )