from core.result_models import build_success, build_error


def transform_hyperbola(A, B, C, D, E):
    steps = []
    try:
        steps.append({
            "title": "Identificar coeficientes",
            "explanation": "A y B tienen signos opuestos, lo que confirma la hipérbola.",
            "equation": f"({A})x² + ({C})x  +  ({B})y² + ({D})y + {E} = 0",
        })

        h = round(-C / (2 * A), 2)
        steps.append({
            "title": "Completar cuadrado en x",
            "equation": f"h = -C / 2A = -({C}) / 2({A})",
            "result": str(h),
        })

        k = round(-D / (2 * B), 2)
        steps.append({
            "title": "Completar cuadrado en y",
            "equation": f"k = -D / 2B = -({D}) / 2({B})",
            "result": str(k),
        })

        constant = round(-E + (C**2) / (4 * A) + (D**2) / (4 * B), 2)
        steps.append({
            "title": "Calcular constante",
            "equation": f"K = -E + C²/4A + D²/4B = -({E}) + {C}²/{4*A} + {D}²/{4*B}",
            "result": str(constant),
        })

        if constant == 0:
            return build_error(error="No se pudo obtener la hipérbola.", steps=steps)

        a2 = round(abs(constant / A), 2)
        b2 = round(abs(constant / B), 2)
        steps.append({
            "title": "Calcular semiejes al cuadrado",
            "equation": f"a² = |K/A| = |{constant}/{A}|    b² = |K/B| = |{constant}/{B}|",
            "result": f"a²={a2}  b²={b2}",
        })

        a  = round(a2 ** 0.5, 2)
        b  = round(b2 ** 0.5, 2)
        c  = round((a2 + b2) ** 0.5, 2)
        orientation = "horizontal" if A > 0 else "vertical"
        steps.append({
            "title": "Calcular semiejes y focal",
            "equation": f"a = √{a2}    b = √{b2}    c = √(a²+b²) = √{a2+b2}",
            "result": f"a={a}  b={b}  c={c}",
        })

        if A > 0:
            canonical = f"(x - {h})²/{a2} - (y - {k})²/{b2} = 1"
        else:
            canonical = f"(y - {k})²/{b2} - (x - {h})²/{a2} = 1"

        steps.append({
            "title": "Forma canónica",
            "explanation": f"Orientación {orientation}",
            "equation": canonical,
        })

        return build_success(
            conic_type="hyperbola",
            explanation="La hipérbola fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (h, k),
                "orientation": orientation,
                "a": a, "b": b, "c": c,
                "a2": a2, "b2": b2,
            }
        )
    except Exception as ex:
        return build_error(error=str(ex), steps=steps)