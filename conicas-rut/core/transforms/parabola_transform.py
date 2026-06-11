# conicas-rut/core/transforms/parabola_transform.py

from core.result_models import build_success, build_error


def transform_parabola(A, B, C, D, E):
    steps = []

    try:
        # ✓ FIX: redondeo a 6 decimales, consistente con circle_transform y ellipse_transform
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        if B == 0:
            # ── Parábola vertical: (x − h)² = 4p(y − k) ─────────────────
            steps.append({
                "title": "Identificar tipo",
                "explanation": "B = 0 → parábola vertical, el eje es paralelo a y.",
                "equation": f"({A})x² + ({C})x + ({D})y + {E} = 0",
            })

            h = round(-C / (2 * A), 6)
            steps.append({
                "title": "Completar cuadrado en x",
                "equation": f"h = −C / 2A = −({C}) / 2·({A})",
                "result": str(round(h, 4)),
            })

            if D == 0:
                steps.append({
                    "title": "Coeficiente D = 0",
                    "explanation": (
                        "D = -(d7 + d8) = 0. No hay término lineal en y. "
                        "La ecuación no corresponde a una parábola estándar "
                        "con este método de transformación."
                    ),
                })
                return build_error(
                    error="Parábola degenerada: D = 0, no hay término lineal en y.",
                    steps=steps,
                    data={"imaginary": False, "degenerate": True},
                )

            k = round((-E + (C ** 2 / (4 * A))) / D, 6)
            steps.append({
                "title": "Despejar k",
                "equation": (
                    f"k = (−E + C²/4A) / D = "
                    f"(−{E} + {round(C**2/(4*A), 4)}) / {D}"
                ),
                "result": str(round(k, 4)),
            })

            p = round(D / 4, 6)
            steps.append({
                "title": "Calcular p (distancia focal)",
                "explanation": "De la forma (x−h)² = 4p(y−k) → 4p = D → p = D/4",
                "equation": f"p = {D} / 4",
                "result": str(round(p, 4)),
            })

            canonical  = f"(x − {round(h,4)})² = {round(4*p,4)}(y − {round(k,4)})"
            orientation = "vertical"

        elif A == 0:
            # ── Parábola horizontal: (y − k)² = 4p(x − h) ───────────────
            steps.append({
                "title": "Identificar tipo",
                "explanation": "A = 0 → parábola horizontal, el eje es paralelo a x.",
                "equation": f"({B})y² + ({D})y + ({C})x + {E} = 0",
            })

            k = round(-D / (2 * B), 6)
            steps.append({
                "title": "Completar cuadrado en y",
                "equation": f"k = −D / 2B = −({D}) / 2·({B})",
                "result": str(round(k, 4)),
            })

            # ✓ FIX: guard C = 0 — evita ZeroDivisionError
            if C == 0:
                steps.append({
                    "title": "Coeficiente C = 0",
                    "explanation": (
                        "C = -(d5 + d6) = 0. No hay término lineal en x. "
                        "La ecuación no corresponde a una parábola estándar "
                        "con este método de transformación."
                    ),
                })
                return build_error(
                    error="Parábola degenerada: C = 0, no hay término lineal en x.",
                    steps=steps,
                    data={"imaginary": False, "degenerate": True},
                )

            h = round((-E + (D ** 2 / (4 * B))) / C, 6)
            steps.append({
                "title": "Despejar h",
                "equation": (
                    f"h = (−E + D²/4B) / C = "
                    f"(−{E} + {round(D**2/(4*B), 4)}) / {C}"
                ),
                "result": str(round(h, 4)),
            })

            p = round(C / 4, 6)
            steps.append({
                "title": "Calcular p (distancia focal)",
                "explanation": "De la forma (y−k)² = 4p(x−h) → 4p = C → p = C/4",
                "equation": f"p = {C} / 4",
                "result": str(round(p, 4)),
            })

            canonical  = f"(y − {round(k,4)})² = {round(4*p,4)}(x − {round(h,4)})"
            orientation = "horizontal"

        else:
            return build_error(
                error="La ecuación no corresponde a una parábola (A ≠ 0 y B ≠ 0).",
                steps=steps,
            )

        steps.append({
            "title": "Forma canónica",
            "explanation": (
                f"Orientación: {orientation}   |   "
                f"Vértice: ({round(h,4)}, {round(k,4)})   |   "
                f"p = {round(p,4)}"
            ),
            "equation": canonical,
        })

        return build_success(
            conic_type="parabola",
            explanation="La parábola fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "orientation":    orientation,
                "vertex":         (round(h, 4), round(k, 4)),
                "p":              round(p, 4),
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)