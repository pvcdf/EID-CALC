# conicas-rut/core/transforms/ellipse_transform.py

from core.result_models import build_success, build_error


def transform_ellipse(A, B, C, D, E):
    steps = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        steps.append({
            "title": "Agrupar términos cuadráticos",
            "explanation": (
                "Se separan los grupos en x e y "
                "para completar el cuadrado."
            ),
            "equation": (
                f"({A})x² + ({C})x  +  ({B})y² + ({D})y + {E} = 0"
            ),
        })

        # ── Completar cuadrado ────────────────────────────────────────────
        h = round(-C / (2 * A), 6)
        steps.append({
            "title": "Completar cuadrado en x",
            "equation": f"h = -C / (2A) = -({C}) / (2·{A})",
            "result": str(round(h, 4)),
        })

        k = round(-D / (2 * B), 6)
        steps.append({
            "title": "Completar cuadrado en y",
            "equation": f"k = -D / (2B) = -({D}) / (2·{B})",
            "result": str(round(k, 4)),
        })

        # ── Constante de normalización ────────────────────────────────────
        constant = round(-E + (C ** 2) / (4 * A) + (D ** 2) / (4 * B), 6)
        steps.append({
            "title": "Constante de normalización K",
            "explanation": (
                "K = −E + C²/(4A) + D²/(4B)\n"
                "A(x−h)² + B(y−k)² = K"
            ),
            "equation": (
                f"K = −({E}) + ({C})²/(4·{A}) + ({D})²/(4·{B})"
            ),
            "result": str(round(constant, 4)),
        })

        # ── Detección de elipse imaginaria o degenerada ───────────────────
        if constant < 0:
            a2_imag = round(constant / A, 4)
            b2_imag = round(constant / B, 4)
            steps.append({
                "title": "Elipse imaginaria",
                "explanation": (
                    f"K = {round(constant, 4)} < 0. "
                    "La ecuación no tiene solución real: "
                    "la elipse es imaginaria."
                ),
                "result": f"a²={a2_imag}  b²={b2_imag}",
            })
            canonical_imag = (
                f"(x − {round(h,4)})²/({a2_imag}) + "
                f"(y − {round(k,4)})²/({b2_imag}) = 1"
            )
            return build_error(
                error=(
                    "Elipse imaginaria: "
                    f"K = {round(constant, 4)} < 0. "
                    "La ecuación no tiene puntos reales."
                ),
                steps=steps,
                data={
                    "imaginary": True,
                    "center": (round(h, 4), round(k, 4)),
                    "a2": a2_imag,
                    "b2": b2_imag,
                    "canonical_form": canonical_imag,
                },
            )

        if constant == 0:
            steps.append({
                "title": "Elipse degenerada (punto)",
                "explanation": (
                    f"K = 0. La elipse se reduce "
                    f"al punto ({round(h,4)}, {round(k,4)})."
                ),
            })
            return build_error(
                error=(
                    "Elipse degenerada: K = 0. "
                    f"Se reduce al punto ({round(h,4)}, {round(k,4)})."
                ),
                steps=steps,
                data={
                    "imaginary": False,
                    "degenerate": True,
                    "center": (round(h, 4), round(k, 4)),
                    "canonical_form": (
                        f"(x − {round(h,4)})²/0 + "
                        f"(y − {round(k,4)})²/0 = 1"
                    ),
                },
            )

        # ── Elipse real ───────────────────────────────────────────────────
        a2 = round(constant / A, 4)
        b2 = round(constant / B, 4)
        steps.append({
            "title": "Semiejes al cuadrado",
            "equation": (
                f"a² = K/A = {round(constant,4)}/{A}    "
                f"b² = K/B = {round(constant,4)}/{B}"
            ),
            "result": f"a²={a2}  b²={b2}",
        })

        a = round(max(a2, b2) ** 0.5, 4)
        b = round(min(a2, b2) ** 0.5, 4)
        c = round(abs(a ** 2 - b ** 2) ** 0.5, 4)
        steps.append({
            "title": "Semiejes y distancia focal",
            "equation": (
                f"a = √{max(a2,b2)}    "
                f"b = √{min(a2,b2)}    "
                f"c = √|a²−b²|"
            ),
            "result": f"a={a}  b={b}  c={c}",
        })

        canonical = (
            f"(x − {round(h,4)})²/{a2} + "
            f"(y − {round(k,4)})²/{b2} = 1"
        )
        steps.append({
            "title": "Forma canónica",
            "equation": canonical,
        })

        return build_success(
            conic_type="ellipse",
            explanation="La elipse fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (round(h, 4), round(k, 4)),
                "a": a, "b": b, "c": c,
                "a2": a2, "b2": b2,
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)