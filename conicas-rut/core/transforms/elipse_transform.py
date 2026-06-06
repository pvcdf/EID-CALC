# conicas-rut/core/transforms/ellipse_transform.py

from core.result_models import build_success, build_error


def transform_ellipse(A, B, C, D, E):
    steps = []

    try:
        A = round(A, 2)
        B = round(B, 2)
        C = round(C, 2)
        D = round(D, 2)
        E = round(E, 2)
        
        steps.append({
            "title": "Agrupar términos cuadráticos",
            "explanation": "Se separan los grupos en x e y para completar cuadrado.",
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
            "title": "Calcular constante de normalización",
            "equation": f"K = -E + C²/4A + D²/4B = -({E}) + {C}²/{4*A} + {D}²/{4*B}",
            "result": str(constant),
        })

        if constant <= 0:
            return build_error(error="No se pudo normalizar la elipse.", steps=steps)

        a2 = round(constant / A, 2)
        b2 = round(constant / B, 2)
        steps.append({
            "title": "Calcular semiejes al cuadrado",
            "equation": f"a² = K/A = {constant}/{A}    b² = K/B = {constant}/{B}",
            "result": f"a²={a2}  b²={b2}",
        })

        a = round(max(a2, b2) ** 0.5, 2)
        b = round(min(a2, b2) ** 0.5, 2)
        c = round(abs(a**2 - b**2) ** 0.5, 2)
        steps.append({
            "title": "Calcular semiejes y distancia focal",
            "equation": f"a = √{max(a2,b2)}    b = √{min(a2,b2)}    c = √|a²-b²|",
            "result": f"a={a}  b={b}  c={c}",
        })

        canonical = f"(x - {h})²/{a2} + (y - {k})²/{b2} = 1"
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
                "center": (h, k),
                "a": a, "b": b, "c": c,
                "a2": a2, "b2": b2,
            }
        )
    except Exception as ex:
        return build_error(error=str(ex), steps=steps)