"""Trigonometría propia: PI, reducción de ángulos, seno y coseno por Taylor."""

PI = 3.141592653589793
TAU = 2 * PI
NUM_TERMINOS = 12  # Términos de la serie de Taylor (mínimo 10)


def reducir_angulo(angulo):
    """Reduce un ángulo en radianes al intervalo [-PI, PI]."""
    vueltas = round(angulo / TAU)
    reducido = angulo - vueltas * TAU
    if reducido > PI:
        reducido -= TAU
    elif reducido < -PI:
        reducido += TAU
    return reducido


def seno(angulo):
    """Seno por serie de Taylor: x - x^3/3! + x^5/5! - ..."""
    x = reducir_angulo(angulo)
    termino = x
    suma = x
    for n in range(1, NUM_TERMINOS):
        termino = -termino * x * x / ((2 * n) * (2 * n + 1))
        suma += termino
    return suma


def coseno(angulo):
    """Coseno por serie de Taylor: 1 - x^2/2! + x^4/4! - ..."""
    x = reducir_angulo(angulo)
    termino = 1.0
    suma = 1.0
    for n in range(1, NUM_TERMINOS):
        termino = -termino * x * x / ((2 * n - 1) * (2 * n))
        suma += termino
    return suma


def grados_a_radianes(grados):
    """Convierte grados a radianes."""
    return grados * PI / 180
