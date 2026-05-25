# Espera recibir un dict con estructura: {"named_digits": {"d1": int, ..., "d8": int}}
# Este dict debe venir del módulo de validación (rut_validator)

def CrearVariables(rut_data):
    digitos = rut_data["named_digits"]
    a = digitos["d3"]
    residuo = digitos["d8"] % 3
    if residuo == 2: # discontinuidad infinita
        funcion_generada = lambda x: ((digitos["d5"]+1))/(x-a)
        explicacion = "es una discontinuidad infinita porque d8 deja residuo 2 al dividirse por 3"
        tipo = "infinita"
    elif residuo == 1: # discontinuidad de salto
        def FuncionTramos(x):
            if x < a:
                return x + digitos["d2"]
            elif x >= a:
                return x + digitos["d4"]
        funcion_generada = FuncionTramos
        explicacion = "es una discontinuidad de salto porque d8 deja residuo 1 al dividirse por 3"
        tipo = "salto"
    elif residuo == 0: # discontinuidad removible
        funcion_generada = lambda x: ((x-a)*(x+digitos["d1"]))/(x-a)
        explicacion = "es una discontinuidad removible porque d8 deja residuo 0 al dividirse por 3"
        tipo = "removible"
    return {
        "funcion": funcion_generada,
        "a": a,
        "explicacion": explicacion,
        "tipo_discontinuidad": tipo
    }
