from core.result_models import build_success, build_error


def transform_circle(A, B, C, D, E):
    steps = []
    try:
        steps.append({
            "title": "Agrupar términos",
            "explanation": "Se identifican los grupos en x e y para completar cuadrado.",
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

        radius_squared = round(h**2 + k**2 - E, 2)
        steps.append({
            "title": "Calcular r²",
            "equation": f"r² = h² + k² - E = {h}² + {k}² - ({E})",
            "result": str(radius_squared),
        })

        if radius_squared <= 0:
            return build_error(error="El radio calculado no es válido.", steps=steps)

        radius = round(radius_squared ** 0.5, 2)
        canonical = f"(x - {h})² + (y - {k})² = {radius_squared}"

        steps.append({
            "title": "Forma canónica",
            "equation": canonical,
            "result": f"r = {radius}",
        })

        return build_success(
            conic_type="circle",
            explanation="La circunferencia fue transformada correctamente.",
            steps=steps,
            data={
                "canonical_form": canonical,
                "center": (h, k),
                "radius": radius,
                "radius_squared": radius_squared,
            }
        )
    except Exception as ex:
        return build_error(error=str(ex), steps=steps)