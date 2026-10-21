"""Generador del documento SVG completo a partir de la hora, alarma y cronómetro."""

from mimath import angulo_hora, angulo_minuto, angulo_segundo
from nucleo.hora import desde_segundos, formatear_hora
from reloj_svg.alarma_svg import aviso_alarma_svg, marca_alarma_svg
from reloj_svg.constantes import (
    ALTO_LIENZO,
    ANCHO_LIENZO,
    CENTRO_X,
    CENTRO_Y,
    COLOR_ALARMA_TEXTO,
    COLOR_FONDO,
    COLOR_MANECILLA,
    COLOR_SEGUNDERO,
    FUENTE_MONO,
    FUENTE_TEXTO,
)
from reloj_svg.cronometro_svg import cronometro_svg
from reloj_svg.elementos import bisel_svg, manecilla, marcas_svg, numeros_svg


def manecillas_svg(segundos_hora):
    """Manecillas que parten de la hora dada y dan vueltas de 12 h, 1 h y 60 s."""
    h, m, s = desde_segundos(segundos_hora)
    return [
        manecilla(CENTRO_X, CENTRO_Y, 90, 14, 7, COLOR_MANECILLA, angulo_hora(h, m, s), 43200),
        manecilla(CENTRO_X, CENTRO_Y, 136, 16, 4.5, COLOR_MANECILLA, angulo_minuto(m, s), 3600),
        manecilla(CENTRO_X, CENTRO_Y, 150, 36, 1.8, COLOR_SEGUNDERO, angulo_segundo(s), 60),
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="6" fill="{COLOR_SEGUNDERO}"/>',
    ]


def textos_digitales_svg(segundos_hora, segundos_alarma, x_digital):
    """Hora digital estática y, si hay alarma, su rótulo."""
    piezas = [
        f'<text x="{x_digital}" y="418" text-anchor="middle" font-family="{FUENTE_MONO}" '
        f'font-size="30" fill="{COLOR_MANECILLA}">{formatear_hora(segundos_hora)}</text>'
    ]
    if segundos_alarma is not None:
        piezas.append(
            f'<text x="{x_digital}" y="448" text-anchor="middle" font-size="14" '
            f'fill="{COLOR_ALARMA_TEXTO}">Alarma {formatear_hora(segundos_alarma)}</text>'
        )
    return piezas


def construir_svg(segundos_hora, segundos_alarma, segundos_crono):
    """Ensambla el documento SVG completo como texto."""
    # Con cronómetro, la hora digital se desplaza a la izquierda para dejar sitio al mini-dial.
    x_digital = 120 if segundos_crono is not None else CENTRO_X

    piezas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO_LIENZO} {ALTO_LIENZO}" '
        f'width="{ANCHO_LIENZO}" height="{ALTO_LIENZO}" font-family="{FUENTE_TEXTO}">',
        "  <title>Reloj SVG</title>",
        f'<rect x="0" y="0" width="{ANCHO_LIENZO}" height="{ALTO_LIENZO}" fill="{COLOR_FONDO}"/>',
        bisel_svg(),
        marcas_svg(),
        numeros_svg(),
    ]
    if segundos_alarma is not None:
        piezas.append(marca_alarma_svg(segundos_alarma))
    piezas.extend(manecillas_svg(segundos_hora))
    if segundos_alarma is not None:
        piezas.append(aviso_alarma_svg(segundos_hora, segundos_alarma))
    piezas.extend(textos_digitales_svg(segundos_hora, segundos_alarma, x_digital))
    if segundos_crono is not None:
        piezas.append(cronometro_svg(segundos_crono))

    piezas.append("</svg>")
    return "\n".join(piezas) + "\n"
