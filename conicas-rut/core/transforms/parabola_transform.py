# conicas-rut/core/transforms/parabola_transform.py

from core.result_models import build_success, build_error


def transform_parabola(A, B, C, D, E):
    steps = []

    try:
        A = round(A, 2)
        B = round(B, 2)
        C = round(C, 2)
        D = round(D, 2)
        E = round(E, 2)
        
        if B == 0:
            steps.append({
                "title": "Identificar tipo",
                "explanation": "B = 0 → parábola vertical, el eje es paralelo a y.",
                "equation": f"({A})x² + ({C})x + ({D})y + {E} = 0",
            })

            h = round(-C / (2 * A), 2)
            steps.append({
                "title": "Completar cuadrado en x",
                "equation": f"h = -C / 2A = -({C}) / 2({A})",
                "result": str(h),
            })

            k = round((-E + (C**2 / (4 * A))) / D, 2)
            steps.append({
                "title": "Despejar k",
                "equation": f"k = (-E + C²/4A) / D = (-{E} + {round(C**2/(4*A),2)}) / {D}",
                "result": str(k),
            })

            p = round(D / 4, 2)
            steps.append({
                "title": "Calcular p",
                "equation": f"p = D / 4 = {D} / 4",
                "result": str(p),
            })

            canonical = f"(x - {h})² = {4*p}(y - {k})"
            orientation = "vertical"

        elif A == 0:
            steps.append({
                "title": "Identificar tipo",
                "explanation": "A = 0 → parábola horizontal, el eje es paralelo a x.",
                "equation": f"({B})y² + ({D})y + ({C})x + {E} = 0",
            })

            k = round(-D / (2 * B), 2)
            steps.append({
                "title": "Completar cuadrado en y",
                "equation": f"k = -D / 2B = -({D}) / 2({B})",
                "result": str(k),
            })

            h = round((-E + (D**2 / (4 * B))) / C, 2)
            steps.append({
                "title": "Despejar h",
                "equation": f"h = (-E + D²/4B) / C = (-{E} + {round(D**2/(4*B),2)}) / {C}",
                "result": str(h),
            })

            p = round(C / 4, 2)
            steps.append({
                "title": "Calcular p",
                "equation": f"p = C / 4 = {C} / 4",
                "result": str(p),
            })

            canonical = f"(y - {k})² = {4*p}(x - {h})"
            orientation = "horizontal"

        else:
            return build_error(
                error="La ecuación no corresponde a una parábola.",
                steps=steps
            )

        steps.append({
            "title": "Forma canónica",
            "explanation": f"Orientación {orientation}  |  vértice ({h}, {k})  |  p = {p}",
            "equation": canonical,
        })

        return build_success(
            conic_type="parabola",
            explanation="La parábola fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "orientation": orientation,
                "vertex": (h, k),
                "p": p,
            }
        )
    except Exception as ex:
        return build_error(error=str(ex), steps=steps)