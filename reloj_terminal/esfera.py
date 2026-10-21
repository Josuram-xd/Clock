"""Esfera analógica ASCII en color: contorno elíptico, marcas y manecillas."""

from mimath import angulo_hora, angulo_minuto, angulo_segundo, coseno, grados_a_radianes, seno
from nucleo.hora import desde_segundos
from reloj_terminal.ansi import AMARILLO, NEGRITA, ROJO, VERDE, colorear

ANCHO_ESFERA = 25
ALTO_ESFERA = 13
CENTRO_COL = 12
CENTRO_FILA = 6
RADIO_COL = 12.0   # radio horizontal en columnas
RADIO_FILA = 6.0   # radio vertical en filas (la celda es ~2x alta: proporción 2:1)


def poner_celda(rejilla, grados, radio, caracter, color):
    """Coloca un carácter en la rejilla a una distancia radial y ángulo dados.

    El ángulo se mide en grados desde las 12 en sentido horario.
    """
    angulo = grados_a_radianes(grados)
    columna = round(CENTRO_COL + radio * RADIO_COL * seno(angulo))
    fila = round(CENTRO_FILA - radio * RADIO_FILA * coseno(angulo))
    if 0 <= fila < ALTO_ESFERA and 0 <= columna < ANCHO_ESFERA:
        if color:
            rejilla[fila][columna] = colorear(caracter, color)
        else:
            rejilla[fila][columna] = caracter


def trazar_mano(rejilla, grados, longitud, caracter, color):
    """Dibuja una manecilla desde el centro hasta la longitud indicada (0 a 1)."""
    paso = 0.0
    while paso <= longitud:
        poner_celda(rejilla, grados, paso, caracter, color)
        paso += 0.02


def marcar_contorno(rejilla):
    """Dibuja el contorno elíptico de la esfera usando la ecuación de la elipse."""
    for fila in range(ALTO_ESFERA):
        for columna in range(ANCHO_ESFERA):
            dx = (columna - CENTRO_COL) / RADIO_COL
            dy = (fila - CENTRO_FILA) / RADIO_FILA
            distancia2 = dx * dx + dy * dy
            if abs(distancia2 - 1.0) < 0.12:
                rejilla[fila][columna] = "."


def dibujar_esfera(segundos):
    """Devuelve las líneas ASCII de la esfera con las tres manecillas."""
    horas, minutos, segundos_reloj = desde_segundos(segundos)
    rejilla = [[" "] * ANCHO_ESFERA for _ in range(ALTO_ESFERA)]
    marcar_contorno(rejilla)
    for marca in range(12):
        poner_celda(rejilla, marca * 30, 0.9, "+", NEGRITA)

    # La manecilla de las horas avanza por minutos completos (sin contar segundos).
    trazar_mano(rejilla, angulo_hora(horas, minutos, 0), 0.5, "#", AMARILLO)
    trazar_mano(rejilla, angulo_minuto(minutos, segundos_reloj), 0.8, "=", VERDE)
    trazar_mano(rejilla, angulo_segundo(segundos_reloj), 0.9, "*", ROJO)
    rejilla[CENTRO_FILA][CENTRO_COL] = colorear("o", NEGRITA)

    return ["".join(fila) for fila in rejilla]
