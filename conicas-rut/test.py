from core.rut_validator import validate_rut
from core.coef_builder import build_coefficients

from core.conic_classifier import classify_conic

from core.transforms.canonical_transform import (
    transform_conic
)


# ─────────────────────────────────────────────
# Utilidades de impresión
# ─────────────────────────────────────────────

def imprimir_separador(titulo: str):

    linea = "═" * 60

    print(f"\n{linea}")
    print(f"  {titulo}")
    print(linea)


def imprimir_pasos(pasos: list):

    for paso in pasos:
        print(paso)


def imprimir_error(resultado: dict):

    print(f"\n✗ Error:")
    print(f"  {resultado.get('error')}")


# ─────────────────────────────────────────────
# ENTRADA
# ─────────────────────────────────────────────

rut = input("Ingrese RUT: ")


# ─────────────────────────────────────────────
# VALIDACIÓN DEL RUT
# ─────────────────────────────────────────────

imprimir_separador("VALIDACIÓN DEL RUT")

validation = validate_rut(rut)

imprimir_pasos(
    validation.get("steps", [])
)

if not validation["valid"]:

    imprimir_error(validation)
    exit()

validation_data = validation["data"]

print(f"\n✓ RUT válido")
print(f"  RUT limpio  : {validation_data['clean_rut']}")
print(f"  Cuerpo      : {validation_data['body']}")
print(f"  DV ingresado: {validation_data['dv_input']}")
print(f"  DV esperado : {validation_data['dv_expected']}")
print(f"  Variable v  : {validation_data['v']}")
print(f"  Dígitos     : {validation_data['named_digits']}")


# ─────────────────────────────────────────────
# CONSTRUCCIÓN DE COEFICIENTES
# ─────────────────────────────────────────────

imprimir_separador(
    "CONSTRUCCIÓN DE COEFICIENTES"
)

coefficients = build_coefficients(
    validation
)

imprimir_pasos(
    coefficients.get("steps", [])
)

if not coefficients["valid"]:

    imprimir_error(coefficients)
    exit()

coef_data = coefficients["data"]

print(f"\n✓ Coeficientes construidos")

print(
    f"  A = {coef_data['A']:.6f} "
    f"(fracción: {coef_data['A_frac']})"
)

print(
    f"  B = {coef_data['B']:.6f} "
    f"(fracción: {coef_data['B_frac']})"
)

print(f"  C = {coef_data['C']}")
print(f"  D = {coef_data['D']}")
print(f"  E = {coef_data['E']}")

print(
    f"\n  Ecuación:"
)

print(
    f"  {coef_data['equation_str']}"
)

if coef_data["adjustments"]:

    print(f"\n  Ajustes aplicados:")

    for adj in coef_data["adjustments"]:

        print(f"    • {adj}")

else:

    print(f"\n  Sin ajustes especiales")


# ─────────────────────────────────────────────
# CLASIFICACIÓN DE CÓNICA
# ─────────────────────────────────────────────

imprimir_separador(
    "CLASIFICACIÓN DE CÓNICA"
)

classification = classify_conic(
    coefficients
)

imprimir_pasos(
    classification.get("steps", [])
)

if not classification["valid"]:

    imprimir_error(classification)
    exit()

class_data = classification["data"]

print(f"\n✓ Cónica clasificada")

print(
    f"  Tipo:"
    f" {class_data['conic_name_es']}"
)

print(
    f"  Tipo interno:"
    f" {classification['conic_type']}"
)

print(
    f"\n  Explicación:"
)

print(
    f"  {classification['explanation']}"
)


# ─────────────────────────────────────────────
# TRANSFORMACIÓN CANÓNICA
# ─────────────────────────────────────────────

imprimir_separador(
    "TRANSFORMACIÓN CANÓNICA"
)

transform = transform_conic(

    classification["conic_type"],

    coef_data["A"],
    coef_data["B"],
    coef_data["C"],
    coef_data["D"],
    coef_data["E"],
)

imprimir_pasos(
    transform.get("steps", [])
)

if not transform["valid"]:

    imprimir_error(transform)
    exit()

transform_data = transform["data"]

print(f"\n✓ Transformación completada")

print(
    f"\n  Forma canónica:"
)

print(
    f"  {transform_data['canonical_form']}"
)

# ─────────────────────────────────────────────
# Datos según tipo de cónica
# ─────────────────────────────────────────────

conic_type = transform["conic_type"]

if "center" in transform_data:

    print(
        f"\n  Centro:"
        f" {transform_data['center']}"
    )

if conic_type == "circle":

    print(
        f"  Radio:"
        f" {transform_data['radius']:.6f}"
    )

elif conic_type == "ellipse":

    print(
        f"  Semieje mayor (a):"
        f" {transform_data['a']:.6f}"
    )

    print(
        f"  Semieje menor (b):"
        f" {transform_data['b']:.6f}"
    )

    print(
        f"  Distancia focal (c):"
        f" {transform_data['c']:.6f}"
    )

elif conic_type == "hyperbola":

    print(
        f"  Orientación:"
        f" {transform_data['orientation']}"
    )

    print(
        f"  a = {transform_data['a']:.6f}"
    )

    print(
        f"  b = {transform_data['b']:.6f}"
    )

    print(
        f"  c = {transform_data['c']:.6f}"
    )

elif conic_type == "parabola":

    print(
        f"  Vértice:"
        f" {transform_data['vertex']}"
    )

    print(
        f"  Orientación:"
        f" {transform_data['orientation']}"
    )

    print(
        f"  Parámetro p:"
        f" {transform_data['p']:.6f}"
    )


# ─────────────────────────────────────────────
# FIN
# ─────────────────────────────────────────────

imprimir_separador(
    "PROCESO COMPLETADO"
)

print(
    "\n✓ Todas las etapas fueron ejecutadas correctamente."
)