# conicas-rut/core/limit_analyzer.py

from core.tramo_function import CrearVariables


def _generar_tabla_aproximacion(funcion, a, direccion):
    """
    Evalúa f(x) en puntos que se aproximan a 'a' por izquierda o derecha.
    """
    deltas = [1, 0.1, 0.01, 0.001]
    signo  = -1 if direccion == "izquierda" else 1
    simbolo = "⁻" if direccion == "izquierda" else "⁺"

    filas = []
    for delta in (reversed(deltas) if direccion == "izquierda" else deltas):
        x = round(a + signo * delta, 6)
        try:
            y = funcion(x)
            filas.append({"x": x, "y": y, "y_str": f"{y:.6f}"})
        except (ZeroDivisionError, ValueError):
            filas.append({"x": x, "y": None, "y_str": "Indef."})

    ultimo = next((f["y"] for f in reversed(filas) if f["y"] is not None), None)
    return {
        "filas":        filas,
        "ultimo_valor": ultimo,
        "simbolo":      simbolo,
    }


def _limites_algebraicos(tipo, a, digitos):
    """
    Calcula límites laterales y genera el desarrollo paso a paso para mostrar
    """
    d1 = digitos["d1"]
    d2 = digitos["d2"]
    d4 = digitos["d4"]
    d5 = digitos["d5"]

    desarrollo = []

    if tipo == "removible":
        limite = a + d1
        desarrollo.append(
            f"f(x) = ((x − {a})(x + {d1})) / (x − {a})"
        )
        desarrollo.append(
            f"Para x ≠ {a}, se cancela el factor (x − {a}):"
        )
        desarrollo.append(
            f"f(x) = x + {d1}"
        )
        desarrollo.append(
            f"lím(x→{a}) f(x) = {a} + {d1} = {limite}"
        )
        return limite, limite, desarrollo

    elif tipo == "salto":
        lim_izq = a + d2
        lim_der = a + d4
        desarrollo.append(
            f"Tramo izquierdo (x < {a}): f(x) = x + {d2}"
        )
        desarrollo.append(
            f"lím(x→{a}⁻) f(x) = {a} + {d2} = {lim_izq}"
        )
        desarrollo.append(
            f"Tramo derecho (x ≥ {a}): f(x) = x + {d4}"
        )
        desarrollo.append(
            f"lím(x→{a}⁺) f(x) = {a} + {d4} = {lim_der}"
        )
        if lim_izq != lim_der:
            desarrollo.append(
                f"Como {lim_izq} ≠ {lim_der}, el límite bilateral NO existe."
            )
        else:
            desarrollo.append(
                f"Como {lim_izq} = {lim_der}, el límite bilateral existe y vale {lim_izq}."
            )
        return lim_izq, lim_der, desarrollo

    elif tipo == "infinita":
        numerador = d5 + 1
        desarrollo.append(
            f"f(x) = {numerador} / (x − {a})"
        )
        desarrollo.append(
            f"Cuando x → {a}⁻: (x − {a}) → 0⁻  →  f(x) → "
            f"{'−∞' if numerador > 0 else '+∞'}"
        )
        desarrollo.append(
            f"Cuando x → {a}⁺: (x − {a}) → 0⁺  →  f(x) → "
            f"{'+∞' if numerador > 0 else '−∞'}"
        )
        desarrollo.append(
            f"Los límites laterales divergen. El límite bilateral no existe."
        )
        desarrollo.append(
            f"Asíntota vertical en x = {a}."
        )
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

    # Tablas numéricas
    t_izq = _generar_tabla_aproximacion(funcion, a, "izquierda")
    t_der = _generar_tabla_aproximacion(funcion, a, "derecha")

    # Valor en el punto
    try:
        valor_en_punto = funcion(a)
    except (ZeroDivisionError, ValueError):
        valor_en_punto = None

    # Límites algebraicos
    lim_izq, lim_der, desarrollo = _limites_algebraicos(tipo, a, digitos)

    # Determinar existencia del límite
    if tipo == "infinita":
        limite_existe = False
        es_continua   = False
    elif tipo == "removible":
        limite_existe = True     # lim_izq == lim_der == a + d1
        es_continua   = False    # f(a) no está definida
    elif tipo == "salto":
        limite_existe = (lim_izq == lim_der)
        es_continua   = limite_existe and valor_en_punto is not None and abs(valor_en_punto - lim_izq) < 1e-9
    else:
        limite_existe = False
        es_continua   = False

    # Conclusiones en texto
    if tipo == "infinita":
        conclusion_limite = (
            f"El límite cuando x → {a} NO existe: "
            f"los límites laterales divergen hacia ±∞."
        )
        clasificacion = "Discontinuidad Esencial (Infinita)"
        justificacion = (
            f"f(x) = {digitos['d5']+1}/(x−{a}) tiene una asíntota vertical "
            f"en x = {a}. El denominador se anula en ese punto y el numerador "
            f"no, por lo que f(x) crece/decrece sin límite."
        )
    elif tipo == "removible":
        lim_val = lim_izq
        conclusion_limite = (
            f"El límite cuando x → {a} EXISTE y vale {lim_val}."
        )
        clasificacion = "Discontinuidad Removible"
        justificacion = (
            f"lím(x→{a}) f(x) = {lim_val} existe, pero f({a}) no está definida. "
            f"Podría «removerse» definiendo f({a}) = {lim_val}."
        )
    else:  # salto
        if limite_existe:
            conclusion_limite = (
                f"El límite cuando x → {a} EXISTE y vale {lim_izq} "
                f"(límites laterales iguales)."
            )
            clasificacion = "Función Continua en x = " + str(a)
            justificacion = (
                f"Ambos límites laterales coinciden en {lim_izq} y f({a}) = {valor_en_punto}."
            )
        else:
            conclusion_limite = (
                f"El límite cuando x → {a} NO existe: "
                f"lím izquierdo = {lim_izq}, lím derecho = {lim_der}."
            )
            clasificacion = "Discontinuidad de Salto"
            justificacion = (
                f"Los límites laterales son distintos ({lim_izq} ≠ {lim_der}), "
                f"por lo que el límite bilateral no existe. "
                f"La función «salta» de {lim_izq} a {lim_der} en x = {a}."
            )

    if es_continua:
        conclusion_continuidad = f"f es CONTINUA en x = {a}."
    else:
        conclusion_continuidad = f"f NO es continua en x = {a}."

    return {
        "a":                    a,
        "tipo":                 tipo,
        "lim_izquierdo":        lim_izq,
        "lim_derecho":          lim_der,
        "limite_existe":        limite_existe,
        "valor_en_punto":       valor_en_punto,
        "es_continua":          es_continua,
        "tabla_izquierda":      t_izq["filas"],
        "tabla_derecha":        t_der["filas"],
        "desarrollo_algebraico": desarrollo,
        "conclusion_limite":    conclusion_limite,
        "conclusion_continuidad": conclusion_continuidad,
        "clasificacion_discontinuidad": clasificacion,
        "justificacion":        justificacion,
    }