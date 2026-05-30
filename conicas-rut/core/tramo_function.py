# conicas-rut/core/tramo_function.py


def CrearVariables(rut_data):
    digitos = rut_data["named_digits"]
    d1 = digitos["d1"]
    d2 = digitos["d2"]
    d3 = digitos["d3"]
    d4 = digitos["d4"]
    d5 = digitos["d5"]
    d8 = digitos["d8"]

    a = d3
    residuo = d8 % 3

    pasos = []
    pasos.append(
        f"Punto crítico 'a' determinado por d3 = {a}."
    )
    pasos.append(
        f"Clasificación de discontinuidad: d8 = {d8}, "
        f"residuo d8 mod 3 = {residuo}."
    )

    # ── CASO 0: Discontinuidad Removible ────────────────────────────────
    if residuo == 0:
        limite = a + d1
        expr_f1 = f"((x - {a})(x + {d1})) / (x - {a})"
        expr_f2 = f"x + {d1}  (x ≠ {a})"

        def funcion(x):
            if x == a:
                raise ZeroDivisionError("f(a) no definida")
            return ((x - a) * (x + d1)) / (x - a)

        # Para el plotter: un solo tramo con hueco en x=a
        def _f_removible(x, _a=a, _d1=d1):
            if x == _a:
                raise ZeroDivisionError("hueco en x = a")
            return x + _d1

        funcion_tramos = [
            {
                "func": _f_removible,
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
        pasos.append(
            f"Residuo 0 → Discontinuidad Removible."
        )
        pasos.append(
            f"Estructura: f(x) = ((x − a)(x + d1)) / (x − a)"
        )
        pasos.append(
            f"Sustituyendo: f(x) = ((x − {a})(x + {d1})) / (x − {a})"
        )
        pasos.append(
            f"Simplificación algebraica: el factor (x − {a}) se cancela."
        )
        pasos.append(
            f"Función equivalente: f(x) = x + {d1}  para x ≠ {a}."
        )
        pasos.append(
            f"f({a}) no está definida (denominador = 0)."
        )
        pasos.append(
            f"lím(x→{a}) f(x) = {a} + {d1} = {limite}."
        )

    # ── CASO 1: Discontinuidad de Salto ─────────────────────────────────
    elif residuo == 1:
        lim_izq = a + d2
        lim_der = a + d4
        expr_f1 = f"x + {d2}  si x < {a}"
        expr_f2 = f"x + {d4}  si x ≥ {a}"

        def funcion(x):
            if x < a:
                return x + d2
            return x + d4

        funcion_tramos = [
            {
                "func": lambda x, _a=a, _d2=d2: x + _d2,
                "x_min": a - 6,
                "x_max": a,          # tramo izquierdo: hasta a (sin incluir)
                "color": None,
                "discontinuity_type": None,
                "open_right": True,  # punto abierto en x=a por izquierda
                "endpoint_y": lim_izq,
            },
            {
                "func": lambda x, _a=a, _d4=d4: x + _d4,
                "x_min": a,          # tramo derecho: desde a (incluido)
                "x_max": a + 6,
                "color": None,
                "discontinuity_type": None,
                "closed_left": True, # punto cerrado en x=a por derecha
                "endpoint_y": lim_der,
            },
        ]

        tipo = "salto"
        explicacion = (
            f"d8 = {d8} deja residuo 1 al dividirse por 3. "
            f"Se generan dos tramos: f(x) = x+{d2} (x<{a}) y f(x) = x+{d4} (x≥{a}). "
            f"Límite izquierdo = {lim_izq}, límite derecho = {lim_der}. "
            f"Como son distintos, el límite bilateral no existe."
        )
        pasos.append("Residuo 1 → Discontinuidad de Salto.")
        pasos.append(
            f"Estructura: f(x) = {{ x + d2  si x < a  ;  x + d4  si x ≥ a }}"
        )
        pasos.append(
            f"Sustituyendo: f(x) = {{ x + {d2}  si x < {a}  ;  x + {d4}  si x ≥ {a} }}"
        )
        pasos.append(
            f"lím(x→{a}⁻) f(x) = {a} + {d2} = {lim_izq}."
        )
        pasos.append(
            f"lím(x→{a}⁺) f(x) = {a} + {d4} = {lim_der}."
        )
        if lim_izq != lim_der:
            pasos.append(
                f"Como {lim_izq} ≠ {lim_der}, el límite bilateral NO existe."
            )
        else:
            pasos.append(
                f"Como {lim_izq} = {lim_der}, el límite bilateral existe y vale {lim_izq}."
            )

    # ── CASO 2: Discontinuidad Infinita ─────────────────────────────────
    else:
        numerador = d5 + 1
        expr_f1 = f"{numerador} / (x − {a})"
        expr_f2 = expr_f1

        def funcion(x):
            if x == a:
                raise ZeroDivisionError("asíntota vertical")
            return numerador / (x - a)

        funcion_tramos = [
            {
                "func": lambda x, _a=a, _n=numerador: _n / (x - _a),
                "x_min": a - 6,
                "x_max": a - 0.01,   # tramo izquierdo: hasta antes de a
                "color": None,
                "discontinuity_type": "infinite",
                "asymptote_x": a,
            },
            {
                "func": lambda x, _a=a, _n=numerador: _n / (x - _a),
                "x_min": a + 0.01,   # tramo derecho: desde después de a
                "x_max": a + 6,
                "color": None,
                "discontinuity_type": None,
            },
        ]

        tipo = "infinita"
        explicacion = (
            f"d8 = {d8} deja residuo 2 al dividirse por 3. "
            f"Se genera f(x) = {numerador}/(x−{a}). "
            f"Al acercarse x→{a}, el denominador tiende a 0 y f(x) crece sin límite. "
            f"Existe asíntota vertical en x = {a}."
        )
        pasos.append("Residuo 2 → Discontinuidad Infinita.")
        pasos.append(
            f"Estructura: f(x) = (d5 + 1) / (x - a)"
        )
        pasos.append(
            f"Sustituyendo: f(x) = ({d5} + 1) / (x - {a}) = {numerador} / (x - {a})"
        )
        pasos.append(
            f"Cuando x → {a}⁻, (x - {a}) → 0⁻, por lo que f(x) → "
            f"{'−∞' if numerador > 0 else '+∞'}."
        )
        pasos.append(
            f"Cuando x → {a}⁺, (x - {a}) → 0⁺, por lo que f(x) → "
            f"{'+∞' if numerador > 0 else '−∞'}."
        )
        pasos.append(
            f"Asíntota vertical en x = {a}."
        )

    return {
        "funcion":             funcion,
        "funcion_tramos":      funcion_tramos,
        "a":                   a,
        "tipo_discontinuidad": tipo,
        "explicacion":         explicacion,
        "digitos":             digitos,
        "pasos_preliminares":  pasos,
        "expr_f1":             expr_f1,
        "expr_f2":             expr_f2,
    }