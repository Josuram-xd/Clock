"""Elementos SVG de la esfera: líneas, bisel, marcas, números y manecillas."""

from mimath import punto_polar
from reloj_svg.constantes import (
    CENTRO_X,
    CENTRO_Y,
    COLOR_BISEL_EXTERNO,
    COLOR_BISEL_INTERNO,
    COLOR_CARA,
    COLOR_MARCA_HORA,
    COLOR_MARCA_MINUTO,
    COLOR_NUMERO,
)


def punto_svg(cx, cy, radio, grados):
    """Punto a 'radio' del centro (cx, cy), en grados desde las 12 en sentido horario.

    El eje Y del SVG apunta hacia abajo, por eso se resta el desplazamiento vertical.
    """
    dx, dy = punto_polar(0, 0, radio, grados)
    return cx + dx, cy - dy


def linea_svg(cx, cy, radio_interno, radio_externo, grados, color, grosor):
    """Segmento radial entre dos radios, en un ángulo dado."""
    x1, y1 = punto_svg(cx, cy, radio_interno, grados)
    x2, y2 = punto_svg(cx, cy, radio_externo, grados)
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{grosor}" stroke-linecap="round"/>')


def bisel_svg():
    """Tres círculos concéntricos que dan el efecto de bisel de la esfera."""
    return "\n".join([
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="170" fill="{COLOR_BISEL_EXTERNO}"/>',
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="164" fill="{COLOR_BISEL_INTERNO}"/>',
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="158" fill="{COLOR_CARA}"/>',
    ])


def marcas_svg():
    """60 marcas; las de cada hora (cada 5) son más gruesas y largas."""
    piezas = []
    for i in range(60):
        grados = i * 6
        if i % 5 == 0:
            piezas.append(linea_svg(CENTRO_X, CENTRO_Y, 136, 152, grados, COLOR_MARCA_HORA, 4))
        else:
            piezas.append(linea_svg(CENTRO_X, CENTRO_Y, 146, 152, grados, COLOR_MARCA_MINUTO, 1.5))
    return "\n".join(piezas)


def numeros_svg():
    """Números del 1 al 12 colocados con las funciones trigonométricas propias."""
    piezas = []
    for hora in range(1, 13):
        x, y = punto_svg(CENTRO_X, CENTRO_Y, 118, hora * 30)
        piezas.append(
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="22" fill="{COLOR_NUMERO}">{hora}</text>'
        )
    return "\n".join(piezas)


def manecilla(cx, cy, longitud_arriba, longitud_abajo, grosor, color, angulo, duracion):
    """Manecilla en un grupo que gira alrededor de (cx, cy).

    La animación parte del ángulo actual (from) y da una vuelta completa
    en 'duracion' segundos, en bucle infinito.
    """
    inicio = f"{angulo:.3f} {cx} {cy}"
    fin = f"{angulo + 360:.3f} {cx} {cy}"
    return "\n".join([
        "<g>",
        f'  <line x1="{cx}" y1="{cy + longitud_abajo}" x2="{cx}" y2="{cy - longitud_arriba}" '
        f'stroke="{color}" stroke-width="{grosor}" stroke-linecap="round"/>',
        f'  <animateTransform attributeName="transform" type="rotate" '
        f'from="{inicio}" to="{fin}" dur="{duracion}s" repeatCount="indefinite"/>',
        "</g>",
    ])
