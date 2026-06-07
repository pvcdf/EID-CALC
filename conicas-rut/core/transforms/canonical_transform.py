# conicas-rut/core/transforms/canonical_transform.py

from core.result_models import build_error
from core.transforms.circle_transform import (transform_circle)
from core.transforms.elipse_transform import (transform_ellipse)
from core.transforms.hyperbola_transform import (transform_hyperbola)
from core.transforms.parabola_transform import (transform_parabola)


def transform_conic(
    conic_type,
    A,
    B,
    C,
    D,
    E
):
    """
    Ejecuta la transformación correspondiente
    según el tipo de cónica.
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
        error=(
            f"No existe transformación "
            f"para '{conic_type}'."
        )
    )