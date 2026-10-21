"""Elementos SVG de la alarma: marca roja en la esfera y aviso parpadeante."""

from mimath import angulo_hora
from nucleo.alarma import segundos_hasta_alarma
from nucleo.hora import desde_segundos
from reloj_svg.constantes import CENTRO_X, CENTRO_Y, COLOR_ALARMA
from reloj_svg.elementos import linea_svg


def marca_alarma_svg(segundos_alarma):
    """Marca roja sobre las horas en el ángulo de la alarma."""
    horas, minutos, segundos = desde_segundos(segundos_alarma)
    return linea_svg(CENTRO_X, CENTRO_Y, 136, 152, angulo_hora(horas, minutos, segundos),
                     COLOR_ALARMA, 5)


def aviso_alarma_svg(segundos_hora, segundos_alarma):
    """Texto '¡ALARMA!' oculto que aparece y parpadea cuando la animación llega a la alarma."""
    inicio = segundos_hasta_alarma(segundos_hora, segundos_alarma)
    return "\n".join([
        f'<text x="{CENTRO_X}" y="275" text-anchor="middle" font-size="26" font-weight="bold" '
        f'fill="{COLOR_ALARMA}" visibility="hidden">&#161;ALARMA!',
        f'  <set attributeName="visibility" to="visible" begin="{inicio}s"/>',
        f'  <animate attributeName="opacity" values="1;0;1" dur="1s" begin="{inicio}s" '
        f'repeatCount="indefinite"/>',
        "</text>",
    ])
