from tramo_function import CrearVariables

def calcular_limite_lateral(funcion, a, direccion):
    deltas = [0.1, 0.01, 0.001, 0.0001]
    signo = -1 if direccion == "izquierda" else 1
    ultimo = None
    for delta in deltas:
        x = a + signo * delta
        try:
            ultimo = funcion(x)
        except ZeroDivisionError:
            pass
    return ultimo

def evaluar_en_punto(funcion, a):
    try:
        return funcion(a)
    except ZeroDivisionError:
        return None

def clasificar_discontinuidad(tipo, a, lim_izq, lim_der):
    if tipo == "removible":
        justificacion = f"El limite existe y vale {lim_izq:.4f}, pero f({a}) no esta definida. Es removible porque podria eliminarse definiendo f({a}) = {lim_izq:.4f}."
    elif tipo == "salto":
        justificacion = f"El limite por izquierda ({lim_izq:.4f}) es distinto al limite por derecha ({lim_der:.4f}). El limite bilateral no existe, lo que indica una discontinuidad de salto."
    elif tipo == "infinita":
        justificacion = f"El denominador se anula en x = {a}. Los limites laterales tienden a mas/menos infinito, por lo que hay una asintota vertical en x = {a}."
    return {"tipo": tipo, "justificacion": justificacion}

def AnalizarLimites(Rut):
    datos = CrearVariables(Rut)
    funcion = datos["funcion"]
    a = datos["a"]
    tipo = datos["tipo_discontinuidad"]

    lim_izq = calcular_limite_lateral(funcion, a, "izquierda")
    lim_der = calcular_limite_lateral(funcion, a, "derecha")
    valor_en_punto = evaluar_en_punto(funcion, a)

    if tipo == "infinita":
        limite_existe = False
        es_continua = False
    else:
        limite_existe = lim_izq is not None and lim_der is not None and abs(lim_izq - lim_der) < 0.0001
        es_continua = limite_existe and valor_en_punto is not None and abs(valor_en_punto - lim_izq) < 0.0001

    return {
        "a": a,
        "limite_izquierdo": lim_izq,
        "limite_derecho": lim_der,
        "limite_existe": limite_existe,
        "valor_en_punto": valor_en_punto,
        "es_continua": es_continua,
        "discontinuidad": clasificar_discontinuidad(tipo, a, lim_izq, lim_der)
    }