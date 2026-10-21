"""Colores ANSI y utilidades de texto: longitud visible, centrado y cajas."""

ESC = "\033"
LIMPIAR_PANTALLA = ESC + "[2J" + ESC + "[H"
RESET = ESC + "[0m"
NEGRITA = ESC + "[1m"
ROJO = ESC + "[31m"
ROJO_PARPADEO = ESC + "[5;1;31m"
VERDE = ESC + "[32m"
AMARILLO = ESC + "[33m"
AZUL = ESC + "[34m"
CIAN = ESC + "[36m"
BLANCO = ESC + "[97m"


def longitud_visible(texto):
    """Cuenta los caracteres visibles, ignorando las secuencias ANSI."""
    total = 0
    dentro_secuencia = False
    for caracter in texto:
        if caracter == ESC:
            dentro_secuencia = True
        elif dentro_secuencia:
            if caracter == "m":
                dentro_secuencia = False
        else:
            total += 1
    return total


def colorear(texto, color):
    """Envuelve el texto en un color ANSI y lo restablece al final."""
    return color + texto + RESET


def centrar(texto, ancho):
    """Centra un texto (con o sin color) dentro de un ancho dado."""
    relleno = (ancho - longitud_visible(texto)) // 2
    if relleno < 0:
        relleno = 0
    return " " * relleno + texto


def dibujar_caja(lineas, ancho):
    """Dibuja una caja con bordes unicode. Una línea None es un separador."""
    borde = colorear("║", AZUL)
    salida = [colorear("╔" + "═" * ancho + "╗", AZUL)]
    for linea in lineas:
        if linea is None:
            salida.append(colorear("╟" + "─" * ancho + "╢", AZUL))
            continue
        relleno = ancho - longitud_visible(linea)
        salida.append(borde + linea + " " * relleno + borde)
    salida.append(colorear("╚" + "═" * ancho + "╝", AZUL))
    return salida
