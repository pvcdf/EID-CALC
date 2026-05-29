<<<<<<< Updated upstream
# Espera recibir un dict con estructura: {"named_digits": {"d1": int, ..., "d8": int}}
# Este dict debe venir del módulo de validación (rut_validator)
=======
from core.rut_validator import validate_rut 
>>>>>>> Stashed changes

def CrearVariables(rut_data):
    digitos = rut_data["named_digits"]
    a = digitos["d3"]
    residuo = digitos["d8"] % 3
    
    pasos = []
    pasos.append(f"1. Punto critico 'a': Determinado por el digito d3 = {a}.")
    pasos.append(f"2. Analisis de discontinuidad: d8 = {digitos['d8']}. Se calcula {digitos['d8']} modulo 3 = {residuo}.")

    if residuo == 2:
        def FuncionInfinita(x):
            return (digitos["d5"] + 1) / (x - a)
            
        funcion_generada = FuncionInfinita
        explicacion = "es una discontinuidad infinita porque d8 deja residuo 2 al dividirse por 3"
        tipo = "infinita"
        pasos.append("3. Residuo 2 indica Discontinuidad Infinita.")
        pasos.append("   Estructura algebraica generica: f(x) = (d5 + 1) / (x - a)")
        pasos.append(f"   Funcion final reemplazada: f(x) = ({digitos['d5']} + 1) / (x - {a})")
        
    elif residuo == 1:
        def FuncionSalto(x):
            if x < a:
                return x + digitos["d2"]
            elif x >= a:
                return x + digitos["d4"]
                
        funcion_generada = FuncionSalto
        explicacion = "es una discontinuidad de salto porque d8 deja residuo 1 al dividirse por 3"
        tipo = "salto"
        pasos.append("3. Residuo 1 indica Discontinuidad de Salto.")
        pasos.append("   Estructura algebraica generica: f(x) = { x + d2 (x < a) ; x + d4 (x >= a) }")
        pasos.append(f"   Funcion final reemplazada: f(x) = {{ x + {digitos['d2']} si x < {a} ; x + {digitos['d4']} si x >= {a} }}")
        
    elif residuo == 0:
        def FuncionRemovible(x):
            return ((x - a) * (x + digitos["d1"])) / (x - a)
            
        funcion_generada = FuncionRemovible
        explicacion = "es una discontinuidad removible porque d8 deja residuo 0 al dividirse por 3"
        tipo = "removible"
        pasos.append("3. Residuo 0 indica Discontinuidad Removible.")
        pasos.append("   Estructura algebraica generica: f(x) = ((x - a)(x + d1)) / (x - a)")
        pasos.append(f"   Funcion final reemplazada: f(x) = ((x - {a})(x + {digitos['d1']})) / (x - {a})")

    return {
        "funcion": funcion_generada,
        "a": a,
        "explicacion": explicacion,
        "tipo_discontinuidad": tipo,
        "digitos": digitos,
        "pasos_preliminares": pasos
    }