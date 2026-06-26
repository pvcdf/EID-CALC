# conicas-rut/core/limites/tramo_function.py
def _extraer_digitos(rut_data: dict) -> dict:
    if not isinstance(rut_data, dict):
        raise ValueError("Datos de RUT inválidos para construir la función por tramos.")

    if "named_digits" in rut_data:
        return rut_data["named_digits"]

    data = rut_data.get("data", {})

    if "named_digits" in data:
        return data["named_digits"]

    raise ValueError("No se encontraron los dígitos nombrados del RUT.")


def CrearVariables(rut_data):
    digitos = _extraer_digitos(rut_data)

    d1 = digitos["d1"]
    d2 = digitos["d2"]
    d3 = digitos["d3"]
    d4 = digitos["d4"]
    d5 = digitos["d5"]
    d8 = digitos["d8"]
    #Se decide si la discontinuidad es removible, salto o infinita
    # d8 mod 3 = 0 (Removible)
    # d8 mod 3 = 1 (De salto)
    # d8 mod 3 = 2 (Infinita)
    a = d3
    residuo = d8 % 3

    pasos = [
        f"Punto crítico a determinado por d3 = {a}.",
        (
            f"Clasificación de discontinuidad: d8 = {d8}, "
            f"residuo d8 mod 3 = {residuo}."
        ),
    ]

    if residuo == 0: #Removible
        
        limite = a + d1
        #Funcion racional (x-a)(x+d1)/x-a
        #Forzamos el ZeroDivisionError cuando x = a para reconocer matematicamente
        #Que la funcion original no esta definida en el punto
        expr_f1 = f"((x - {a})(x + {d1})) / (x - {a})"
        expr_f2 = f"x + {d1}  para x ≠ {a}"

        def funcion(x):
            if x == a:
                raise ZeroDivisionError("f(a) no definida")
            return ((x - a) * (x + d1)) / (x - a)

        def funcion_removible(x, _a=a, _d1=d1):
            if x == _a:
                raise ZeroDivisionError("hueco en x = a")
            return x + _d1

        funcion_tramos = [
            {
                "func": funcion_removible,
                "x_min": a - 6,
                "x_max": a + 6,
                "color": None,
                "discontinuity_type": "removable",
                "hole_x": a,
                "hole_y": limite,
            }
        ]

        tipo = "removible"

        explicacion = (
            f"d8 = {d8} deja residuo 0 al dividirse por 3. "
            f"Se genera f(x) = ((x−{a})(x+{d1}))/(x−{a}). "
            f"El factor (x−{a}) se cancela algebraicamente, pero f({a}) no está definida. "
            f"El límite bilateral existe y vale {limite}."
        )

        pasos.extend([
            "Residuo 0 → Discontinuidad Removible.",
            "Estructura: f(x) = ((x − a)(x + d1)) / (x − a).",
            f"Sustituyendo: f(x) = ((x − {a})(x + {d1})) / (x − {a}).",
            f"Simplificación algebraica: el factor (x − {a}) se cancela.",
            f"Función equivalente: f(x) = x + {d1} para x ≠ {a}.",
            f"f({a}) no está definida porque el denominador se hace cero.",
            f"lím(x→{a}) f(x) = {a} + {d1} = {limite}.",
        ])

    elif residuo == 1: #De salto
        #Se construyen dos tramos con comportamientos distintos al acercarse al punto "a"
        #Valores menores: x + d2
        #Valores mayores: x + d4
        lim_izq = a + d2
        lim_der = a + d4

        expr_f1 = f"x + {d2}  si x < {a}"
        expr_f2 = f"x + {d4}  si x ≥ {a}"

        def funcion(x):
            if x < a:
                return x + d2
            return x + d4

        def funcion_salto_izquierda(x, _d2=d2):
            return x + _d2

        def funcion_salto_derecha(x, _d4=d4):
            return x + _d4

        funcion_tramos = [
            {
                "func": funcion_salto_izquierda,
                "x_min": a - 6,
                "x_max": a,
                "color": None,
                "discontinuity_type": None,
                "open_right": True,
                "endpoint_y": lim_izq,
            },
            {
                "func": funcion_salto_derecha,
                "x_min": a,
                "x_max": a + 6,
                "color": None,
                "discontinuity_type": None,
                "closed_left": True,
                "endpoint_y": lim_der,
            },
        ]

        tipo = "salto"

        explicacion = (
            f"d8 = {d8} deja residuo 1 al dividirse por 3. "
            f"Se generan dos tramos: f(x) = x+{d2} para x<{a} "
            f"y f(x) = x+{d4} para x≥{a}. "
            f"Límite izquierdo = {lim_izq}, límite derecho = {lim_der}."
        )

        pasos.extend([
            "Residuo 1 → Discontinuidad de Salto.",
            "Estructura: f(x) = { x + d2 si x < a ; x + d4 si x ≥ a }.",
            f"Sustituyendo: f(x) = {{ x + {d2} si x < {a} ; x + {d4} si x ≥ {a} }}.",
            f"lím(x→{a}⁻) f(x) = {a} + {d2} = {lim_izq}.",
            f"lím(x→{a}⁺) f(x) = {a} + {d4} = {lim_der}.",
        ])

        if lim_izq != lim_der:
            pasos.append(
                f"Como {lim_izq} ≠ {lim_der}, el límite bilateral NO existe."
            )
        else:
            pasos.append(
                f"Como {lim_izq} = {lim_der}, el límite bilateral existe y vale {lim_izq}."
            )

    else: #Infinito
        #Construimos una funcion racional en el que el denominador se anula en el punto de analisis "a"
        #El numerador se define como d5 + 1 para evitar un numerador nulo
        #Levantamos ZeroDivisionError cuando queremos indicar la presencia de la asintota vertical
        numerador = d5 + 1

        expr_f1 = f"{numerador} / (x − {a})"
        expr_f2 = expr_f1

        def funcion(x):
            if x == a:
                raise ZeroDivisionError("asíntota vertical")
            return numerador / (x - a)

        def funcion_infinita(x, _a=a, _n=numerador):
            if x == _a:
                raise ZeroDivisionError("asíntota vertical")
            return _n / (x - _a)

        funcion_tramos = [
            {
                "func": funcion_infinita,
                "x_min": a - 6,
                "x_max": a - 0.01,
                "color": None,
                "discontinuity_type": "infinite",
                "asymptote_x": a,
            },
            {
                "func": funcion_infinita,
                "x_min": a + 0.01,
                "x_max": a + 6,
                "color": None,
                "discontinuity_type": None,
            },
        ]

        tipo = "infinita"

        limite_izq = "−∞" if numerador > 0 else "+∞"
        limite_der = "+∞" if numerador > 0 else "−∞"

        explicacion = (
            f"d8 = {d8} deja residuo 2 al dividirse por 3. "
            f"Se genera f(x) = {numerador}/(x−{a}). "
            f"Al acercarse x→{a}, el denominador tiende a 0. "
            f"Existe asíntota vertical en x = {a}."
        )

        pasos.extend([
            "Residuo 2 → Discontinuidad Infinita.",
            "Estructura: f(x) = (d5 + 1) / (x - a).",
            f"Sustituyendo: f(x) = ({d5} + 1) / (x - {a}) = {numerador} / (x - {a}).",
            (
                f"Cuando x → {a}⁻, (x - {a}) → 0⁻, "
                f"por lo que f(x) → {limite_izq}."
            ),
            (
                f"Cuando x → {a}⁺, (x - {a}) → 0⁺, "
                f"por lo que f(x) → {limite_der}."
            ),
            f"Asíntota vertical en x = {a}.",
        ])

    return {
        "funcion": funcion,
        "funcion_tramos": funcion_tramos,
        "a": a,
        "tipo_discontinuidad": tipo,
        "explicacion": explicacion,
        "digitos": digitos,
        "pasos_preliminares": pasos,
        "expr_f1": expr_f1,
        "expr_f2": expr_f2,
    }