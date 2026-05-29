from rut_validator import validate_rut

def CrearVariables(Rut):
    Variables = validate_rut(Rut)
    digitos = Variables["named_digits"]
    a = digitos["d3"]
    residuo = digitos["d8"] % 3
    
    def funcion_removible(x):
        return ((x - a) * (x + digitos["d1"])) / (x - a)
        
    def funcion_salto(x):
        return (x < a) * (x + digitos["d2"]) + (x >= a) * (x + digitos["d4"])
        
    def funcion_infinita(x):
        return (digitos["d5"] + 1) / (x - a)
        
    mapa_funciones = {
        0: (funcion_removible, "removible", f"((x - {a})(x + {digitos['d1']})) / (x - {a})"),
        1: (funcion_salto, "salto", f"{{ x + {digitos['d2']} (x < {a}) ; x + {digitos['d4']} (x >= {a}) }}"),
        2: (funcion_infinita, "infinita", f"({digitos['d5']} + 1) / (x - {a})")
    }
    
    funcion_generada, tipo, estructura = mapa_funciones[residuo]
    
    delta_lejano = 0.01
    delta_cercano = 0.0001
    
    def analizar_lateral(signo_dir):
        try:
            y_lejano = funcion_generada(a + signo_dir * delta_lejano)
            y_cercano = funcion_generada(a + signo_dir * delta_cercano)
            
            crecimiento = abs(y_cercano - y_lejano)
            magnitud = abs(y_cercano)
            signo = "+" if y_cercano > 0 else "-"
            
            if magnitud > 500 and crecimiento > 50:
                return f"{signo}∞", y_cercano
            
            return "converge", y_cercano
        except ZeroDivisionError:
            return "+∞", float('inf')

    estado_izq, val_izq = analizar_lateral(-1)
    estado_der, val_der = analizar_lateral(1)
    
    if "∞" in estado_izq or "∞" in estado_der:
        conclusion = "diverge"
    elif abs(val_izq - val_der) > 0.01:
        conclusion = "diverge por salto"
    else:
        conclusion = "converge"
        
    pasos = [
        f"1. Punto critico 'a': Determinado por el digito d3 = {a}.",
        f"2. Construccion matematica: d8 = {digitos['d8']} modulo 3 = {residuo}.",
        f"   Estructura asignada: f(x) = {estructura}",
        f"3. Analisis numerico de magnitud, tendencia y signo en x = {a}:",
        f"   - Izquierda: tendencia = {estado_izq} (magnitud aprox {val_izq:.4f})",
        f"   - Derecha: tendencia = {estado_der} (magnitud aprox {val_der:.4f})",
        f"4. Conclusion: La funcion {conclusion}."
    ]

    return {
        "funcion": funcion_generada,
        "a": a,
        "explicacion": f"Discontinuidad {tipo}. Al evaluar matematicamente la tendencia, la funcion {conclusion}.",
        "tipo_discontinuidad": tipo,
        "digitos": digitos,
        "pasos_preliminares": pasos
    }