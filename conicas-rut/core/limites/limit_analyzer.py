# conicas-rut/core/limites/limit_analyzer.py

from core.limites.tramo_function import CrearVariables
from core.limites.value_table import CrearTablaValores


# ── Cálculo algebraico de límites ──────────────────────────────────────────
# Según el tipo de discontinuidad, calcula límites laterales y genera
# los pasos explicativos que se muestran en la interfaz.

def _limites_algebraicos(tipo, a, digitos):
    """
    Calcula límites laterales algebraicamente y genera desarrollo paso a paso.

    Retorna:
        lim_izq, lim_der, desarrollo
    """
    d1 = digitos["d1"]
    d2 = digitos["d2"]
    d4 = digitos["d4"]
    d5 = digitos["d5"]

    desarrollo = []

    if tipo == "removible":
        limite = a + d1  # límite luego de cancelar el factor problemático

        desarrollo.append({
            "title": "Expresión original",
            "explanation": f"f(x) = ((x − {a})(x + {d1})) / (x − {a})",
        })

        desarrollo.append({
            "title": "Cancelación algebraica",
            "explanation": (
                f"Para x ≠ {a}, el factor (x − {a}) se cancela. "
                f"Entonces f(x) = x + {d1}."
            ),
        })

        desarrollo.append({
            "title": "Cálculo del límite",
            "explanation": f"lím(x→{a}) f(x) = {a} + {d1} = {limite}",
            "result": str(limite),
        })

        return limite, limite, desarrollo

    if tipo == "salto":
        lim_izq = a + d2  # límite lateral por la izquierda
        lim_der = a + d4  # límite lateral por la derecha

        desarrollo.append({
            "title": "Tramo izquierdo",
            "explanation": f"Para x < {a}: f(x) = x + {d2}.",
        })

        desarrollo.append({
            "title": "Límite por izquierda",
            "explanation": f"lím(x→{a}⁻) f(x) = {a} + {d2} = {lim_izq}",
            "result": str(lim_izq),
        })

        desarrollo.append({
            "title": "Tramo derecho",
            "explanation": f"Para x ≥ {a}: f(x) = x + {d4}.",
        })

        desarrollo.append({
            "title": "Límite por derecha",
            "explanation": f"lím(x→{a}⁺) f(x) = {a} + {d4} = {lim_der}",
            "result": str(lim_der),
        })

        if lim_izq != lim_der:
            desarrollo.append({
                "title": "Comparación de límites laterales",
                "explanation": f"{lim_izq} ≠ {lim_der} → el límite bilateral NO existe.",
            })
        else:
            desarrollo.append({
                "title": "Comparación de límites laterales",
                "explanation": f"{lim_izq} = {lim_der} → el límite bilateral existe.",
                "result": str(lim_izq),
            })

        return lim_izq, lim_der, desarrollo

    if tipo == "infinita":
        numerador = d5 + 1  # se evita numerador cero para forzar asíntota vertical
        lim_izq = "−∞" if numerador > 0 else "+∞"
        lim_der = "+∞" if numerador > 0 else "−∞"

        desarrollo.append({
            "title": "Expresión",
            "explanation": f"f(x) = {numerador} / (x − {a})",
        })

        desarrollo.append({
            "title": "Límite por izquierda",
            "explanation": (
                f"Cuando x → {a}⁻: (x − {a}) → 0⁻, "
                f"por lo tanto f(x) → {lim_izq}."
            ),
            "result": lim_izq,
        })

        desarrollo.append({
            "title": "Límite por derecha",
            "explanation": (
                f"Cuando x → {a}⁺: (x − {a}) → 0⁺, "
                f"por lo tanto f(x) → {lim_der}."
            ),
            "result": lim_der,
        })

        desarrollo.append({
            "title": "Conclusión",
            "explanation": (
                "Los límites laterales divergen, por lo que el límite bilateral no existe. "
                f"Existe una asíntota vertical en x = {a}."
            ),
        })

        return lim_izq, lim_der, desarrollo

    return None, None, []


# ── Análisis principal de límites y continuidad ────────────────────────────

def AnalizarLimites(rut_data):
    """Calcula límites laterales, continuidad y clasificación de discontinuidad."""
    datos = CrearVariables(rut_data)

    funcion = datos["funcion"]                  # función evaluable
    a = datos["a"]                              # punto crítico
    tipo = datos["tipo_discontinuidad"]         # removible, salto o infinita
    digitos = datos["digitos"]                  # dígitos d1...d8 usados en reglas

    tabla = CrearTablaValores(a, funcion)

    try:
        valor_en_punto = funcion(a)             # f(a), si está definida

        if isinstance(valor_en_punto, float):
            valor_en_punto = round(valor_en_punto, 6)

    except (ZeroDivisionError, ValueError):
        valor_en_punto = None                   # f(a) no existe

    lim_izq, lim_der, desarrollo = _limites_algebraicos(tipo, a, digitos)

    # Condición general: el límite bilateral existe si ambos laterales coinciden.
    if tipo == "infinita":
        limite_existe = False
        es_continua = False

    elif tipo == "removible":
        limite_existe = True
        es_continua = False

    elif tipo == "salto":
        limite_existe = lim_izq == lim_der
        es_continua = (
            limite_existe
            and valor_en_punto is not None
            and abs(valor_en_punto - lim_izq) < 0.000001
        )

    else:
        limite_existe = False
        es_continua = False

    # ── Conclusiones para la interfaz ──────────────────────────────────────

    if tipo == "infinita":
        conclusion_limite = (
            f"El límite cuando x → {a} NO existe: "
            f"los límites laterales divergen ({lim_izq} y {lim_der})."
        )

        clasificacion = "Discontinuidad Infinita"

        justificacion = (
            f"f(x) = {digitos['d5'] + 1}/(x−{a}) tiene una asíntota vertical "
            f"en x = {a}. El denominador se anula y el numerador no, "
            "por lo que la función crece o decrece sin límite."
        )

    elif tipo == "removible":
        conclusion_limite = f"El límite cuando x → {a} EXISTE y vale {lim_izq}."

        clasificacion = "Discontinuidad Removible"

        justificacion = (
            f"El límite lím(x→{a}) f(x) = {lim_izq} existe, "
            f"pero f({a}) no está definida. "
            f"La discontinuidad podría removerse definiendo f({a}) = {lim_izq}."
        )

    else:
        if limite_existe:
            conclusion_limite = (
                f"El límite cuando x → {a} EXISTE y vale {lim_izq}, "
                "porque los límites laterales son iguales."
            )

            clasificacion = f"Función Continua en x = {a}"

            justificacion = (
                f"Ambos límites laterales coinciden en {lim_izq} "
                f"y f({a}) = {valor_en_punto}. "
                "Por lo tanto, el valor de la función coincide con el límite."
            )

        else:
            conclusion_limite = (
                f"El límite cuando x → {a} NO existe: "
                f"límite izquierdo = {lim_izq}, límite derecho = {lim_der}."
            )

            clasificacion = "Discontinuidad de Salto"

            justificacion = (
                f"Los límites laterales son distintos ({lim_izq} ≠ {lim_der}), "
                "por lo que el límite bilateral no existe. "
                f"La función salta de {lim_izq} a {lim_der} en x = {a}."
            )

    conclusion_continuidad = (
        f"f ES continua en x = {a}."
        if es_continua
        else f"f NO es continua en x = {a}."
    )

    return {
        "a": a,                                                # punto crítico
        "tipo": tipo,                                          # tipo interno de discontinuidad
        "lim_izquierdo": lim_izq,                              # límite por izquierda
        "lim_derecho": lim_der,                                # límite por derecha
        "limite_existe": limite_existe,                        # existencia del límite bilateral
        "valor_en_punto": valor_en_punto,                      # f(a)
        "es_continua": es_continua,                            # continuidad en x = a
        "tabla_izquierda": tabla["izquierda"],                 # valores con x < a
        "tabla_derecha": tabla["derecha"],                     # valores con x > a
        "desarrollo_algebraico": desarrollo,                   # pasos matemáticos
        "pasos_preliminares": datos.get("pasos_preliminares", []),
        "expr_f1": datos.get("expr_f1"),                       # expresión del primer tramo
        "expr_f2": datos.get("expr_f2"),                       # expresión del segundo tramo
        "funcion_tramos": datos.get("funcion_tramos", []),     # datos para graficar
        "explicacion": datos.get("explicacion", ""),
        "conclusion_limite": conclusion_limite,
        "conclusion_continuidad": conclusion_continuidad,
        "clasificacion_discontinuidad": clasificacion,
        "justificacion": justificacion,
    }