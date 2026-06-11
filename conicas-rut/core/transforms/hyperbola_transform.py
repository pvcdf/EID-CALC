# conicas-rut/core/transforms/hyperbola_transform.py

from core.result_models import build_success, build_error


def transform_hyperbola(A, B, C, D, E):
    steps = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        steps.append({
            "title": "Identificar coeficientes",
            "explanation": "A y B tienen signos opuestos, lo que confirma la hipérbola.",
            "equation": f"({A})x² + ({C})x  +  ({B})y² + ({D})y + {E} = 0",
        })

        h = round(-C / (2 * A), 6)
        steps.append({
            "title": "Completar cuadrado en x",
            "equation": f"h = −C / 2A = −({C}) / 2·({A})",
            "result": str(round(h, 4)),
        })

        k = round(-D / (2 * B), 6)
        steps.append({
            "title": "Completar cuadrado en y",
            "equation": f"k = −D / 2B = −({D}) / 2·({B})",
            "result": str(round(k, 4)),
        })

        constant = round(-E + (C ** 2) / (4 * A) + (D ** 2) / (4 * B), 6)
        steps.append({
            "title": "Calcular constante K",
            "explanation": "K = −E + C²/4A + D²/4B",
            "equation": f"K = −({E}) + ({C})²/{round(4*A,4)} + ({D})²/{round(4*B,4)}",
            "result": str(round(constant, 4)),
        })

        if constant == 0:
            steps.append({
                "title": "Hipérbola degenerada",
                "explanation": (
                    "K = 0. La ecuación se reduce a dos rectas que se cruzan en el centro. "
                    f"Centro: ({round(h,4)}, {round(k,4)})."
                ),
            })
            return build_error(
                error="Hipérbola degenerada: K = 0 (par de rectas).",
                steps=steps,
                data={
                    "imaginary":  False,
                    "degenerate": True,
                    "center":     (round(h, 4), round(k, 4)),
                    "canonical_form": (
                        f"(x − {round(h,4)})²/0 − (y − {round(k,4)})²/0 = 1"
                    ),
                },
            )

        a2 = round(abs(constant / A), 6)
        b2 = round(abs(constant / B), 6)
        steps.append({
            "title": "Semiejes al cuadrado",
            "equation": (
                f"a² = |K/A| = |{round(constant,4)}/{A}|    "
                f"b² = |K/B| = |{round(constant,4)}/{B}|"
            ),
            "result": f"a²={round(a2,4)}  b²={round(b2,4)}",
        })

        a = round(a2 ** 0.5, 4)
        b = round(b2 ** 0.5, 4)
        c = round((a2 + b2) ** 0.5, 4)
        orientation = "horizontal" if A > 0 else "vertical"

        steps.append({
            "title": "Semiejes y distancia focal",
            "explanation": "Para hipérbola: c² = a² + b²",
            "equation": (
                f"a = √{round(a2,4)}    "
                f"b = √{round(b2,4)}    "
                f"c = √({round(a2,4)} + {round(b2,4)})"
            ),
            "result": f"a={a}  b={b}  c={c}",
        })

        if A > 0:
            canonical = (
                f"(x − {round(h,4)})²/{round(a2,4)} − "
                f"(y − {round(k,4)})²/{round(b2,4)} = 1"
            )
        else:
            canonical = (
                f"(y − {round(k,4)})²/{round(b2,4)} − "
                f"(x − {round(h,4)})²/{round(a2,4)} = 1"
            )

        steps.append({
            "title": "Forma canónica",
            "explanation": f"Orientación: {orientation}",
            "equation": canonical,
        })

        return build_success(
            conic_type="hyperbola",
            explanation="La hipérbola fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center":         (round(h, 4), round(k, 4)),
                "orientation":    orientation,
                "a":  a,  "b":  b,  "c":  c,
                "a2": round(a2, 4), "b2": round(b2, 4),
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)