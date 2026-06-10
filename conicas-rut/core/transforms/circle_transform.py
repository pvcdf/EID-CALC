# conicas-rut/core/transforms/circle_transform.py

from core.result_models import build_success, build_error


def transform_circle(A, B, C, D, E):
    steps = []

    try:
        A = round(A, 6)
        B = round(B, 6)
        C = round(C, 6)
        D = round(D, 6)
        E = round(E, 6)

        steps.append({
            "title": "Ecuación general de la circunferencia",
            "explanation": (
                "Como A = B, la ecuación general tiene la forma "
                "A·x² + A·y² + C·x + D·y + E = 0"
            ),
            "equation": f"({A})x² + ({A})y² + ({C})x + ({D})y + {E} = 0",
        })

        # ── Paso 1: Dividir por A ─────────────────────────────────────────
        CA = round(C / A, 6)
        DA = round(D / A, 6)
        EA = round(E / A, 6)
        steps.append({
            "title": "Paso 1 — Dividir por A",
            "explanation": "Dividimos toda la ecuación por A para dejar coeficientes cuadráticos igual a 1.",
            "equation": f"x² + y² + ({round(CA,4)})x + ({round(DA,4)})y + {round(EA,4)} = 0",
        })

        # ── Paso 2: Agrupar y pasar constante al lado derecho ─────────────
        steps.append({
            "title": "Paso 2 — Agrupar y despejar constante",
            "explanation": "Se agrupan los términos en x e y, pasando E/A al lado derecho.",
            "equation": (
                f"(x² + ({round(CA,4)})x) + (y² + ({round(DA,4)})y) = {round(-EA,4)}"
            ),
        })

        # ── Paso 3: Completar cuadrado ────────────────────────────────────
        h = round(-C / (2 * A), 6)
        k = round(-D / (2 * A), 6)
        term_x = round((C / (2 * A)) ** 2, 6)   # C²/4A²
        term_y = round((D / (2 * A)) ** 2, 6)   # D²/4A²

        steps.append({
            "title": "Paso 3 — Completar cuadrado",
            "explanation": (
                f"Se suma (C/2A)² = {round(term_x,4)} en x "
                f"y (D/2A)² = {round(term_y,4)} en y a ambos lados."
            ),
            "equation": (
                f"(x + {round(C/(2*A),4)})² + (y + {round(D/(2*A),4)})² = "
                f"{round(-EA,4)} + {round(term_x,4)} + {round(term_y,4)}"
            ),
        })

        # ── Paso 4: Forma canónica y r² ───────────────────────────────────
        radius_squared = round(h ** 2 + k ** 2 - E / A, 6)

        steps.append({
            "title": "Paso 4 — Calcular r²",
            "explanation": (
                "Dado que h = −C/2A y k = −D/2A, "
                "el lado derecho se simplifica a: r² = h² + k² − E/A"
            ),
            "equation": (
                f"r² = ({round(h,4)})² + ({round(k,4)})² − {round(EA,4)} "
                f"= {round(h**2,4)} + {round(k**2,4)} − {round(EA,4)}"
            ),
            "result": str(round(radius_squared, 4)),
        })

        # ── Detección de círculo imaginario o degenerado ──────────────────
        if radius_squared < 0:
            steps.append({
                "title": "Círculo imaginario",
                "explanation": (
                    f"r² = {round(radius_squared,4)} < 0. "
                    "La ecuación no tiene solución real: "
                    "la circunferencia es imaginaria."
                ),
            })
            return build_error(
                error=(
                    f"Circunferencia imaginaria: r² = {round(radius_squared,4)} < 0. "
                    "La ecuación no tiene puntos reales."
                ),
                steps=steps,
                data={
                    "imaginary": True,
                    "center": (round(h, 4), round(k, 4)),
                    "radius_squared": round(radius_squared, 4),
                    "canonical_form": (
                        f"(x − {round(h,4)})² + (y − {round(k,4)})² = "
                        f"{round(radius_squared,4)}"
                    ),
                },
            )

        if radius_squared == 0:
            steps.append({
                "title": "Circunferencia degenerada (punto)",
                "explanation": (
                    f"r² = 0. La circunferencia se reduce "
                    f"al punto ({round(h,4)}, {round(k,4)})."
                ),
            })
            return build_error(
                error=(
                    f"Circunferencia degenerada: r² = 0. "
                    f"Se reduce al punto ({round(h,4)}, {round(k,4)})."
                ),
                steps=steps,
                data={
                    "imaginary": False,
                    "degenerate": True,
                    "center": (round(h, 4), round(k, 4)),
                    "radius_squared": 0.0,
                    "canonical_form": (
                        f"(x − {round(h,4)})² + (y − {round(k,4)})² = 0"
                    ),
                },
            )

        # ── Círculo real ──────────────────────────────────────────────────
        radius = round(radius_squared ** 0.5, 4)
        canonical = (
            f"(x − {round(h,4)})² + (y − {round(k,4)})² = {round(radius_squared,4)}"
        )

        steps.append({
            "title": "Paso 5 — Forma canónica",
            "equation": canonical,
            "result": f"Centro = ({round(h,4)}, {round(k,4)})   r = {radius}",
        })

        return build_success(
            conic_type="circle",
            explanation="La circunferencia fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (round(h, 4), round(k, 4)),
                "radius": radius,
                "radius_squared": round(radius_squared, 4),
            },
        )

    except Exception as ex:
        return build_error(error=str(ex), steps=steps)