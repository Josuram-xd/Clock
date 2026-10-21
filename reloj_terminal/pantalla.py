"""Pantalla del reloj 2: textos de estado y construcción de la imagen completa."""

from nucleo.cronometro import descripcion_cronometro, formatear_cronometro
from nucleo.hora import formatear_hora, formatear_hora_12h
from reloj_terminal.ansi import (
    AMARILLO,
    BLANCO,
    CIAN,
    LIMPIAR_PANTALLA,
    NEGRITA,
    ROJO_PARPADEO,
    centrar,
    colorear,
    dibujar_caja,
)
from reloj_terminal.digitos import dibujar_digital
from reloj_terminal.esfera import dibujar_esfera

ANCHO_CAJA = 60


def texto_hora(estado):
    """Devuelve (texto de la hora, sufijo AM/PM) según el formato elegido."""
    if estado["formato_24h"]:
        return formatear_hora(estado["segundos"]), ""
    return formatear_hora_12h(estado["segundos"])


def texto_cronometro(estado):
    """Devuelve el cronómetro en formato MM:SS con su estado."""
    cronometro = estado["cronometro"]
    return (formatear_cronometro(cronometro["segundos"])
            + " (" + descripcion_cronometro(cronometro) + ")")


def linea_alarma(estado):
    """Devuelve la línea de alarma; parpadea en rojo cuando está sonando."""
    alarma = estado["alarma"]
    if alarma["sonando"]:
        if estado["parpadeo"]:
            return colorear("¡ALARMA!", ROJO_PARPADEO)
        return " " * len("¡ALARMA!")
    if alarma["hora"] is None:
        return "Alarma: ninguna"
    return "Alarma: " + formatear_hora(alarma["hora"])


def lineas_caja(estado):
    """Contenido de la caja: título, esfera, hora digital y estado."""
    lineas = [centrar(colorear("RELOJ DE TERMINAL", NEGRITA + CIAN), ANCHO_CAJA), None]

    for fila in dibujar_esfera(estado["segundos"]):
        lineas.append(centrar(fila, ANCHO_CAJA))
    lineas.append(None)

    texto, sufijo = texto_hora(estado)
    for fila in dibujar_digital(texto):
        lineas.append(centrar(colorear(fila, BLANCO + NEGRITA), ANCHO_CAJA))
    lineas.append(centrar(sufijo, ANCHO_CAJA))
    lineas.append(None)

    formato = "24h" if estado["formato_24h"] else "12h"
    lineas.append(" Formato: " + formato + "   Cronómetro: " + texto_cronometro(estado))
    lineas.append(" " + linea_alarma(estado))
    return lineas


def construir_pantalla(estado):
    """Construye el texto completo de la pantalla (sin limpiar)."""
    salida = dibujar_caja(lineas_caja(estado), ANCHO_CAJA)
    salida.append(colorear(" [Enter] +1 s    [n] avanzar N s    [c] cronómetro", CIAN))
    salida.append(colorear(" [a] alarma (vacío = quitar)    [f] 12h/24h    [q] salir", CIAN))
    if estado["mensaje"]:
        salida.append(colorear(" " + estado["mensaje"], AMARILLO))
    return "\n".join(salida)


def mostrar(estado):
    """Limpia la pantalla y dibuja el reloj."""
    print(LIMPIAR_PANTALLA + construir_pantalla(estado))
