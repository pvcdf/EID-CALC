# conicas-rut/core/limit_analyzer.py

from core.tramo_function import CrearVariables
from core.value_table import CrearTablaValores, ultimo_valor

def _limites_algebraicos(tipo, a, digitos):
    """
    Calcula límites laterales algebraicamente y genera desarrollo paso a paso.
    Retorna (lim_izq, lim_der, desarrollo).
    """
    d1 = digitos["d1"]
    d2 = digitos["d2"]
    d4 = digitos["d4"]
    d5 = digitos["d5"]

    desarrollo = []

    if tipo == "removible":
        limite = a + d1
        desarrollo.append({
            "title": "Expresión original",
            "explanation": f"f(x) = ((x − {a})(x + {d1})) / (x − {a})",
        })
        desarrollo.append({
            "title": "Cancelación algebraica",
            "explanation": (
                f"Para x ≠ {a}, el factor (x − {a}) se cancela: "
                f"f(x) = x + {d1}"
            ),
        })
        desarrollo.append({
            "title": "Cálculo del límite",
            "explanation": f"lím(x→{a}) f(x) = {a} + {d1} = {limite}",
            "result": str(limite),
        })
        return limite, limite, desarrollo

    elif tipo == "salto":
        lim_izq = a + d2
        lim_der = a + d4
        desarrollo.append({
            "title": "Tramo izquierdo",
            "explanation": f"Para x < {a}: f(x) = x + {d2}",
        })
        desarrollo.append({
            "title": "Límite por izquierda",
            "explanation": f"lím(x→{a}⁻) f(x) = {a} + {d2} = {lim_izq}",
            "result": str(lim_izq),
        })
        desarrollo.append({
            "title": "Tramo derecho",
            "explanation": f"Para x ≥ {a}: f(x) = x + {d4}",
        })
        desarrollo.append({
            "title": "Límite por derecha",
            "explanation": f"lím(x→{a}⁺) f(x) = {a} + {d4} = {lim_der}",
            "result": str(lim_der),
        })
        if lim_izq != lim_der:
            desarrollo.append({
                "title": "Comparación de límites laterales",
                "explanation": (
                    f"{lim_izq} ≠ {lim_der} → el límite bilateral NO existe."
                ),
            })
        else:
            desarrollo.append({
                "title": "Comparación de límites laterales",
                "explanation": (
                    f"{lim_izq} = {lim_der} → el límite bilateral existe "
                    f"y vale {lim_izq}."
                ),
                "result": str(lim_izq),
            })
        return lim_izq, lim_der, desarrollo

    elif tipo == "infinita":
        numerador = d5 + 1
        desarrollo.append({
            "title": "Expresión",
            "explanation": f"f(x) = {numerador} / (x − {a})",
        })
        desarrollo.append({
            "title": "Límite por izquierda",
            "explanation": (
                f"Cuando x → {a}⁻: (x − {a}) → 0⁻  →  "
                f"f(x) → {'−∞' if numerador > 0 else '+∞'}"
            ),
        })
        desarrollo.append({
            "title": "Límite por derecha",
            "explanation": (
                f"Cuando x → {a}⁺: (x − {a}) → 0⁺  →  "
                f"f(x) → {'+∞' if numerador > 0 else '−∞'}"
            ),
        })
        desarrollo.append({
            "title": "Conclusión",
            "explanation": (
                "Los límites laterales divergen. "
                f"El límite bilateral no existe. "
                f"Asíntota vertical en x = {a}."
            ),
        })
        return None, None, desarrollo

    return None, None, []


def AnalizarLimites(rut_data):
    """
    Analiza límites y continuidad de la función en el punto crítico 'a'.
    """
    datos   = CrearVariables(rut_data)
    funcion = datos["funcion"]
    a       = datos["a"]
    tipo    = datos["tipo_discontinuidad"]
    digitos = datos["digitos"]
    tabla = CrearTablaValores(a, funcion)

    # Valor en el punto
    try:
        valor_en_punto = funcion(a)
    except (ZeroDivisionError, ValueError):
        valor_en_punto = None

    # Límites algebraicos y desarrollo
    lim_izq, lim_der, desarrollo = _limites_algebraicos(tipo, a, digitos)

    # Existencia del límite y continuidad
    if tipo == "infinita":
        limite_existe = False
        es_continua   = False
    elif tipo == "removible":
        limite_existe = True
        es_continua   = False   # f(a) no definida
    elif tipo == "salto":
        limite_existe = (lim_izq == lim_der)
        es_continua   = (
            limite_existe
            and valor_en_punto is not None
            and abs(valor_en_punto - lim_izq) < 1e-9
        )
    else:
        limite_existe = False
        es_continua   = False

    # Conclusiones y clasificación de discontinuidad
    if tipo == "infinita":
        conclusion_limite = (
            f"El límite cuando x → {a} NO existe: "
            "los límites laterales divergen hacia ±∞."
        )
        clasificacion = "Discontinuidad Esencial (Infinita)"
        justificacion = (
            f"f(x) = {digitos['d5']+1}/(x−{a}) tiene una asíntota vertical "
            f"en x = {a}. El denominador se anula y el numerador no, "
            "por lo que f(x) crece/decrece sin límite."
        )
    elif tipo == "removible":
        conclusion_limite = (
            f"El límite cuando x → {a} EXISTE y vale {lim_izq}."
        )
        clasificacion = "Discontinuidad Removible"
        justificacion = (
            f"lím(x→{a}) f(x) = {lim_izq} existe, pero f({a}) no está definida. "
            f"Podría «removerse» definiendo f({a}) = {lim_izq}."
        )
    else:  # salto
        if limite_existe:
            conclusion_limite = (
                f"El límite cuando x → {a} EXISTE y vale {lim_izq} "
                "(límites laterales iguales)."
            )
            clasificacion = f"Función Continua en x = {a}"
            justificacion = (
                f"Ambos límites laterales coinciden en {lim_izq} "
                f"y f({a}) = {valor_en_punto}."
            )
        else:
            conclusion_limite = (
                f"El límite cuando x → {a} NO existe: "
                f"lím izquierdo = {lim_izq}, lím derecho = {lim_der}."
            )
            clasificacion = "Discontinuidad de Salto"
            justificacion = (
                f"Los límites laterales son distintos ({lim_izq} ≠ {lim_der}), "
                "por lo que el límite bilateral no existe. "
                f"La función «salta» de {lim_izq} a {lim_der} en x = {a}."
            )

    conclusion_continuidad = (
        f"f ES continua en x = {a}."
        if es_continua
        else f"f NO es continua en x = {a}."
    )

    return {
        "a":                             a,
        "tipo":                          tipo,
        "lim_izquierdo":                 lim_izq,
        "lim_derecho":                   lim_der,
        "limite_existe":                 limite_existe,
        "valor_en_punto":                valor_en_punto,
        "es_continua":                   es_continua,
        "tabla_izquierda":               tabla["izquierda"],
        "tabla_derecha":                 tabla["derecha"],
        "desarrollo_algebraico":         desarrollo,
        "conclusion_limite":             conclusion_limite,
        "conclusion_continuidad":        conclusion_continuidad,
        "clasificacion_discontinuidad":  clasificacion,
        "justificacion":                 justificacion,
    }