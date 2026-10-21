"""Esfera analógica en ASCII: lienzo, marcas, números y manecillas con DDA."""

from mimath import angulo_hora, angulo_manecilla, angulo_minuto, angulo_segundo, punto_polar
from nucleo.hora import desde_segundos

ANCHO = 41
ALTO = 21
CENTRO_COL = 20
CENTRO_FILA = 10
FACTOR_ASPECTO = 2  # Una celda es el doble de alta que de ancha: el eje X se escala x2
RADIO_ANILLO = 10
RADIO_NUMEROS = 9
LARGO_HORA = 5
LARGO_MINUTO = 7
LARGO_SEGUNDO = 8


def crear_lienzo():
    """Crea una matriz de espacios ANCHO x ALTO."""
    return [[" "] * ANCHO for _ in range(ALTO)]


def poner_caracter(lienzo, columna, fila, caracter):
    """Escribe un carácter si la posición cae dentro del lienzo."""
    if 0 <= columna < ANCHO and 0 <= fila < ALTO:
        lienzo[fila][columna] = caracter


def a_celda(x, y):
    """Convierte coordenadas ideales (Y hacia arriba) en (columna, fila)."""
    columna = CENTRO_COL + round(x * FACTOR_ASPECTO)
    fila = CENTRO_FILA - round(y)
    return columna, fila


def punto_en_celda(radio, angulo_grados):
    """Celda del lienzo a 'radio' del centro, con el ángulo dado."""
    x, y = punto_polar(0, 0, radio, angulo_grados)
    return a_celda(x, y)


def linea_dda(col0, fila0, col1, fila1):
    """Celdas de la línea entre dos puntos, con el algoritmo DDA."""
    delta_col = col1 - col0
    delta_fila = fila1 - fila0
    pasos = max(abs(delta_col), abs(delta_fila))
    if pasos == 0:
        return [(col0, fila0)]
    celdas = []
    for paso in range(pasos + 1):
        columna = round(col0 + delta_col * paso / pasos)
        fila = round(fila0 + delta_fila * paso / pasos)
        celdas.append((columna, fila))
    return celdas


def dibujar_marcas(lienzo):
    """Marcas en el anillo: '.' para minutos y '+' para cada hora."""
    for minuto in range(60):
        columna, fila = punto_en_celda(RADIO_ANILLO, angulo_manecilla(minuto, 60))
        caracter = "+" if minuto % 5 == 0 else "."
        poner_caracter(lienzo, columna, fila, caracter)


def dibujar_numeros(lienzo):
    """Escribe los números 1 a 12 alrededor de la esfera."""
    for hora in range(1, 13):
        columna, fila = punto_en_celda(RADIO_NUMEROS, angulo_manecilla(hora, 12))
        texto = str(hora)
        inicio = columna - len(texto) // 2
        for indice, caracter in enumerate(texto):
            poner_caracter(lienzo, inicio + indice, fila, caracter)


def dibujar_manecilla(lienzo, angulo_grados, largo, caracter):
    """Dibuja una manecilla desde el centro hasta su punta."""
    columna_fin, fila_fin = punto_en_celda(largo, angulo_grados)
    for columna, fila in linea_dda(CENTRO_COL, CENTRO_FILA, columna_fin, fila_fin):
        poner_caracter(lienzo, columna, fila, caracter)


def construir_esfera(total_segundos):
    """Compone el lienzo completo: marcas, números y manecillas."""
    horas, minutos, segundos = desde_segundos(total_segundos)
    lienzo = crear_lienzo()
    dibujar_marcas(lienzo)
    dibujar_numeros(lienzo)
    dibujar_manecilla(lienzo, angulo_segundo(segundos), LARGO_SEGUNDO, "s")
    dibujar_manecilla(lienzo, angulo_minuto(minutos, segundos), LARGO_MINUTO, "M")
    # La manecilla de las horas avanza por minutos completos (sin contar segundos).
    dibujar_manecilla(lienzo, angulo_hora(horas, minutos, 0), LARGO_HORA, "H")
    poner_caracter(lienzo, CENTRO_COL, CENTRO_FILA, "O")
    return lienzo


def mostrar_esfera(total_segundos):
    """Imprime la esfera en la consola."""
    for fila in construir_esfera(total_segundos):
        print("".join(fila).rstrip())
