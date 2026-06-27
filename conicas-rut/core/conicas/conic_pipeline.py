# conicas-rut/core/conicas/conic_pipeline.py

from core.conicas.coef_builder import build_coefficients
from core.conicas.conic_classifier import classify_conic
from core.conicas.transforms.canonical_transform import transform_conic
from core.conicas.transforms.general_transform import transform_to_general
from core.utils.result_models import build_error


# ── Pipeline principal de cónicas ──────────────────────────────────────────

def run_pipeline(rut_result: dict) -> dict:
    """Ejecuta el proceso completo de análisis de cónicas."""
    coefs = build_coefficients(rut_result)

    if not coefs["valid"]:
        return build_error(
            error=f"Error en coeficientes: {coefs['error']}",
            steps=coefs.get("steps", []),
            data=coefs.get("data", {}),
        ) | {
            "stage": "coef_builder",
            "coefs": coefs,
            "classifier": {},
            "transform": {},
            "to_general": {},
        }

    classifier = classify_conic(coefs)

    if not classifier["valid"]:
        return build_error(
            error=f"Error en clasificación: {classifier['error']}",
            steps=classifier.get("steps", []),
            data=classifier.get("data", {}),
        ) | {
            "stage": "conic_classifier",
            "coefs": coefs,
            "classifier": classifier,
            "transform": {},
            "to_general": {},
        }

    d = coefs["data"]

    # Transformación desde forma general hacia forma canónica.
    transform = transform_conic(
        conic_type=classifier["conic_type"],
        A=d["A"],
        B=d["B"],
        C=d["C"],
        D=d["D"],
        E=d["E"],
    )

    if not transform["valid"]:
        # Una cónica imaginaria no se grafica, pero sí se muestra como resultado válido.
        if transform.get("data", {}).get("imaginary", False):
            return {
                "valid": True,
                "error": None,
                "stage": "imaginary_conic",
                "coefs": coefs,
                "classifier": classifier,
                "transform": transform,
                "to_general": {},
            }

        return build_error(
            error=f"Error en transformación: {transform['error']}",
            steps=transform.get("steps", []),
            data=transform.get("data", {}),
        ) | {
            "stage": "canonical_transform",
            "coefs": coefs,
            "classifier": classifier,
            "transform": transform,
            "to_general": {},
        }

    # Reconstruye la forma general desde la canónica para verificar consistencia.
    to_general = transform_to_general(
        conic_type=classifier["conic_type"],
        transform_data=transform["data"],
        coef_data=coefs["data"],
    )

    return {
        "valid": True,
        "error": None,
        "stage": "complete",
        "coefs": coefs,
        "classifier": classifier,
        "transform": transform,
        "to_general": to_general,
    }