"""Autotest de la librería: compara seno y coseno con valores conocidos."""

from mimath.trigonometria import coseno, grados_a_radianes, seno

TOLERANCIA = 1e-6

# Valores conocidos: (grados, seno esperado, coseno esperado)
VALORES_CONOCIDOS = [
    (0, 0.0, 1.0),
    (30, 0.5, 0.8660254037844386),
    (45, 0.7071067811865476, 0.7071067811865476),
    (60, 0.8660254037844386, 0.5),
    (90, 1.0, 0.0),
    (180, 0.0, -1.0),
    (270, -1.0, 0.0),
    (360, 0.0, 1.0),
]


def comparar(nombre, obtenido, esperado):
    """Imprime OK o FALLÓ para un valor y devuelve True si pasa la prueba."""
    pasa = abs(obtenido - esperado) <= TOLERANCIA
    estado = "OK" if pasa else "FALLÓ"
    print(f"  {nombre}: obtenido={obtenido:.9f} esperado={esperado:.9f} -> {estado}")
    return pasa


def verificar_libreria():
    """Autotest: compara seno y coseno con valores conocidos."""
    print("AUTOTEST de la librería mimath (tolerancia 1e-6):")
    resultados = []
    for grados, seno_esperado, coseno_esperado in VALORES_CONOCIDOS:
        radianes = grados_a_radianes(grados)
        resultados.append(comparar(f"seno({grados} gr)", seno(radianes), seno_esperado))
        resultados.append(comparar(f"coseno({grados} gr)", coseno(radianes), coseno_esperado))
    if all(resultados):
        print("Resultado global: OK")
    else:
        print("Resultado global: FALLÓ")
