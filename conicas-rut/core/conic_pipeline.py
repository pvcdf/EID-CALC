# conicas-rut/core/conic_pipeline.py

from core.coef_builder import build_coefficients
from core.conic_classifier import classify_conic
from core.transforms.canonical_transform import transform_conic
from core.result_models import build_error
from core.transforms.general_transform import transform_to_general


def run_pipeline(rut_result: dict) -> dict:
    """
    Ejecuta el pipeline completo:
        rut_validator → coef_builder → conic_classifier → canonical_transform

    Retorna un dict con:
        "valid"      : bool
        "error"      : str | None
        "coefs"      : resultado de build_coefficients
        "classifier" : resultado de classify_conic
        "transform"  : resultado de transform_conic
    """

    # ── coef_builder ──────────────────────────────────────────────────────
    coefs = build_coefficients(rut_result)
    if not coefs["valid"]:
        return build_error(
            error=f"Error en coeficientes: {coefs['error']}"
        ) | {"stage": "coef_builder"}

    # ── conic_classifier ──────────────────────────────────────────────────
    classifier = classify_conic(coefs)
    if not classifier["valid"]:
        return build_error(
            error=f"Error en clasificación: {classifier['error']}"
        ) | {"stage": "conic_classifier"}

    # ── canonical_transform ───────────────────────────────────────────────
    d = coefs["data"]
    transform = transform_conic(
        conic_type=classifier["conic_type"],
        A=d["A"], B=d["B"], C=d["C"], D=d["D"], E=d["E"],
    )
    if not transform["valid"]:
        return build_error(
            error=f"Error en transformación: {transform['error']}"
        ) | {"stage": "canonical_transform"}

    to_general = transform_to_general(
        conic_type=classifier["conic_type"],
        transform_data=transform["data"],
        coef_data=coefs["data"],
    )

    return {
        "valid":      True,
        "error":      None,
        "stage":      "complete",
        "coefs":      coefs,
        "classifier": classifier,
        "transform":  transform,
        "to_general": to_general, 
    }