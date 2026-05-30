#conicas-rut/core/limit_analyzer.py

from core.tramo_function import CrearVariables 
from core.result_models import build_success, build_error

def generar_tabla_aproximacion(funcion, a, direccion):
    deltas = [0.1, 0.01, 0.001, 0.0001]
    signo = -1 if direccion == "izquierda" else 1
    simbolo = "-" if direccion == "izquierda" else "+"
    
    valores_y = []
    for delta in deltas:
        x = a + signo * delta
        try:
            y = funcion(x)
            valores_y.append(f"{y:.4f}")
        except ZeroDivisionError:
            valores_y.append("Indef")
            
    texto_aproximacion = f"x -> {a}{simbolo} -> f(x) = " + ", ".join(valores_y)
    ultimo_valor = None
    if valores_y[-1] != "Indef":
        ultimo_valor = float(valores_y[-1])
        
    return {
        "texto": texto_aproximacion,
        "ultimo_valor": ultimo_valor,
        "progresion": valores_y
    }

def evaluar_en_punto(funcion, a):
    try:
        return funcion(a)
    except ZeroDivisionError:
        return None

def limites_algebraicos_estructurados(tipo, a, digitos):
    explicacion_formal = {
        "identificacion": f"Analisis de discontinuidad en x = {a} basada en el digito d8 ({digitos['d8']}).",
        "preliminar": "",
        "demostracion": []
    }
    
    if tipo == "removible":
        limite = a + digitos["d1"]
        explicacion_formal["preliminar"] = f"Se construyo f(x) = ((x - {a})(x + {digitos['d1']})) / (x - {a})"
        explicacion_formal["demostracion"].append(f"Simplificando el factor (x - {a}), la funcion equivalente es f(x) = x + {digitos['d1']} para todo x distinto de {a}.")
        explicacion_formal["demostracion"].append(f"Evaluando el limite directamente: {a} + {digitos['d1']} = {limite}.")
        return limite, limite, explicacion_formal
        
    elif tipo == "salto":
        lim_izq = a + digitos["d2"]
        lim_der = a + digitos["d4"]
        explicacion_formal["preliminar"] = f"Funcion definida por tramos separada en x = {a}."
        explicacion_formal["demostracion"].append(f"Limite por izquierda (x < {a}): se evalua (x + {digitos['d2']}) resultando en {a} + {digitos['d2']} = {lim_izq}.")
        explicacion_formal["demostracion"].append(f"Limite por derecha (x >= {a}): se evalua (x + {digitos['d4']}) resultando en {a} + {digitos['d4']} = {lim_der}.")
        explicacion_formal["demostracion"].append(f"Como {lim_izq} es distinto de {lim_der}, el limite bilateral no existe.")
        return lim_izq, lim_der, explicacion_formal
        
    elif tipo == "infinita":
        numerador = digitos["d5"] + 1
        explicacion_formal["preliminar"] = f"Se construyo la fraccion f(x) = {numerador} / (x - {a})."
        explicacion_formal["demostracion"].append(f"Al evaluar x -> {a}, el denominador tiende a 0 mientras el numerador se mantiene en {numerador}.")
        explicacion_formal["demostracion"].append(f"La division por cero genera un crecimiento infinito (asintota vertical).")
        return None, None, explicacion_formal
        
    return None, None, explicacion_formal

def AnalizarLimites(Rut):
    datos = CrearVariables(Rut)
    funcion = datos["funcion"]
    a = datos["a"]
    tipo = datos["tipo_discontinuidad"]
    digitos = datos["digitos"]

    tabla_izq = generar_tabla_aproximacion(funcion, a, "izquierda")
    tabla_der = generar_tabla_aproximacion(funcion, a, "derecha")
    valor_en_punto = evaluar_en_punto(funcion, a)
    
    lim_izq_alg, lim_der_alg, explicacion = limites_algebraicos_estructurados(tipo, a, digitos)

    if tipo == "infinita":
        limite_existe = False
        es_continua = False
        conclusion_tabla = f"Ambos limites divergen hacia infinito, confirmando asintota en x = {a}."
    else:
        limite_existe = lim_izq_alg == lim_der_alg
        es_continua = limite_existe and valor_en_punto is not None and abs(valor_en_punto - lim_izq_alg) < 0.0001
        
        if limite_existe:
            conclusion_tabla = f"Ambos limites se aproximan a {lim_izq_alg}, por lo tanto el limite bilateral existe."
        else:
            conclusion_tabla = f"Los limites se aproximan a valores distintos ({lim_izq_alg} y {lim_der_alg}), el limite bilateral no existe."

    return {
        "a": a,
        "valor_en_punto": valor_en_punto,
        "limite_existe": limite_existe,
        "es_continua": es_continua,
        "tablas_aproximacion": {
            "izquierda": tabla_izq["texto"],
            "derecha": tabla_der["texto"],
            "conclusion": conclusion_tabla
        },
        "explicacion_formal": explicacion
    }