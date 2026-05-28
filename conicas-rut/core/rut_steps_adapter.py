# conicas-rut/core/rut_steps_adapter.py

import re


def parse_rut_steps(result: dict) -> list[dict]:
    if not result.get("valid"):
        return []

    raw: list[str] = result.get("steps", [])
    data: dict = result.get("data", {})
    structured = []

    for line in raw:

        # "RUT limpio: 123456789"
        if line.startswith("RUT limpio:"):
            clean = line.split(":", 1)[-1].strip()
            structured.append({
                "title": "Limpieza del RUT",
                "explanation": (
                    "Se eliminan puntos, guiones y espacios. El dígito verificador se convierte a mayúscula."
                ),
                "equation": f"RUT limpio → {clean}",
            })

        # "Proceso módulo 11:"
        elif line.startswith("Proceso módulo 11"):
            structured.append({
                "title": "Algoritmo módulo 11",
                "explanation": (
                    "Se recorre el cuerpo del RUT de derecha a izquierda, multiplicando cada dígito por el ciclo [2, 3, 4, 5, 6, 7]."
                ),
            })

        # "d × m = p"  ej: "3 × 2 = 6"
        elif re.fullmatch(r"\d+ × \d+ = \d+", line):
            d, m, p = re.findall(r"\d+", line)
            structured.append({
                "title": f"Dígito {d}",
                "explanation": None,
                "equation": f"{d} × {m} = {p}",
                "result": p,
            })

        # "Suma total = N"
        elif line.startswith("Suma total"):
            total = line.split("=")[-1].strip()
            structured.append({
                "title": "Suma total de productos",
                "explanation": "Suma acumulada de todos los productos anteriores.",
                "equation": line,
                "result": total,
            })

        # "N % 11 = R"
        elif "% 11" in line:
            remainder = line.split("=")[-1].strip()
            structured.append({
                "title": "Resto módulo 11",
                "explanation": "Se calcula el resto de dividir la suma entre 11.",
                "equation": line,
                "result": remainder,
            })

        # "11 - R = resultado"
        elif line.startswith("11 -"):
            result_val = line.split("=")[-1].strip()
            obs = None
            if result_val == "11":
                obs = "Resultado 11 → DV = 0"
            elif result_val == "10":
                obs = "Resultado 10 → DV = K"
            structured.append({
                "title": "Cálculo del DV esperado",
                "explanation": "Se resta el resto de 11 para obtener el dígito verificador.",
                "equation": line,
                "result": result_val,
                "observation": obs,
            })

        # "DV esperado = X"
        elif line.startswith("DV esperado"):
            dv = line.split("=")[-1].strip()
            structured.append({
                "title": "DV esperado",
                "explanation": None,
                "result": dv,
            })

        # "DV ingresado = X"
        elif line.startswith("DV ingresado"):
            dv_in = line.split("=")[-1].strip()
            dv_exp = data.get("dv_expected", "?")
            v = data.get("v", "?")
            structured.append({
                "title": "Verificación del DV",
                "explanation": "Se compara el DV ingresado con el calculado.",
                "equation": f"ingresado '{dv_in}'  =  esperado '{dv_exp}'",
                "result": " Coinciden RUT válido",
                "observation": f"Variable auxiliar  v = {v}",
            })

    return structured