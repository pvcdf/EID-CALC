from core.rut_validator import validate_rut
from core.limit_analyzer import AnalizarLimites

def encontrar_dv_valido(cuerpo):
    for dv in "0123456789K":
        res = validate_rut(f"{cuerpo}-{dv}")
        if res["valid"]:
            return dv
    return "0"

def prueba_exhaustiva():
    print("INICIANDO VALIDACIÓN EXHAUSTIVA DE TRAMOS\n")
    
    cuerpos = ["12345670", "12345671", "12345672"] 
    
    for cuerpo in cuerpos:
        dv = encontrar_dv_valido(cuerpo)
        rut_completo = f"{cuerpo}-{dv}"
        
        resultado_rut = validate_rut(rut_completo)
        datos_rut = resultado_rut["data"]
        
        d8 = datos_rut["named_digits"]["d8"]
        esperado = d8 % 3
        
        analisis = AnalizarLimites(datos_rut)
        
        print(f"RUT Probado: {rut_completo}")
        print(f"Dígito d8: {d8} | Residuo (d8 mod 3): {esperado}")
        print(f"Tipo de Discontinuidad: {analisis['tipo']}")
        print(f"Límite izquierdo: {analisis['lim_izquierdo']}")
        print(f"Límite derecho: {analisis['lim_derecho']}")
        print(f"Conclusión: {analisis['conclusion_limite']}")
        print("-" * 60)

if __name__ == "__main__":
    prueba_exhaustiva()