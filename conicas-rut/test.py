from core.rut_validator import validate_rut
from core.coef_builder import build_coefficients


def imprimir_separador(titulo: str):
    linea = "═" * 50
    print(f"\n{linea}")
    print(f"  {titulo}")
    print(linea)


def imprimir_pasos(pasos: list):
    for paso in pasos:
        print(paso)


# ─────────────────────────────────────────────
#  ENTRADA
# ─────────────────────────────────────────────
rut = input("Ingrese RUT: ")

# ─────────────────────────────────────────────
#  VALIDACIÓN
# ─────────────────────────────────────────────
imprimir_separador("VALIDACIÓN DEL RUT")

validation = validate_rut(rut)

imprimir_pasos(validation.get("steps", []))

if not validation["valid"]:
    print(f"\n RUT inválido: {validation.get('error', 'DV incorrecto')}")
    exit()

print(f"\n RUT válido")
print(f"  RUT limpio  : {validation['clean_rut']}")
print(f"  Cuerpo      : {validation['body']}")
print(f"  DV ingresado: {validation['dv_input']}")
print(f"  DV esperado : {validation['dv_expected']}")
print(f"  Variable v  : {validation['v']}")
print(f"  Dígitos     : {validation['named_digits']}")

# ─────────────────────────────────────────────
#  CONSTRUCCIÓN DE COEFICIENTES
# ─────────────────────────────────────────────
imprimir_separador("CONSTRUCCIÓN DE COEFICIENTES")

# Se pasa el dict completo de validate_rut, no solo los dígitos
coefficients = build_coefficients(validation)

imprimir_pasos(coefficients["steps"])

if not coefficients["valid"]:
    print(f"\n Error: {coefficients['error']}")
    exit()

print(f"\n✓ Coeficientes construidos")
print(f"  A = {coefficients['A']:.6f}  (fracción: {coefficients['A_frac']})")
print(f"  B = {coefficients['B']:.6f}  (fracción: {coefficients['B_frac']})")
print(f"  C = {coefficients['C']}")
print(f"  D = {coefficients['D']}")
print(f"  E = {coefficients['E']}")
print(f"\n  Ecuación: {coefficients['equation_str']}")

if coefficients["adjustments"]:
    print(f"\n  Ajustes aplicados:")
    for adj in coefficients["adjustments"]:
        print(f"    • {adj}")
else:
    print(f"\n  Sin ajustes especiales")