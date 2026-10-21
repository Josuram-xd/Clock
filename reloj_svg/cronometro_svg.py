"""Elementos SVG del cronómetro: mini-dial con su manecilla y etiqueta."""

from mimath import angulo_segundo
from reloj_svg.constantes import (
    COLOR_BISEL_EXTERNO,
    COLOR_CARATULA_CRONO,
    COLOR_MARCA_MINUTO,
    COLOR_SEGUNDERO,
    COLOR_TEXTO_SECUNDARIO,
    CRONO_CX,
    CRONO_CY,
    CRONO_R,
)
from reloj_svg.elementos import linea_svg, manecilla


def cronometro_svg(segundos):
    """Mini-dial de cronómetro con su etiqueta; la manecilla gira cada 60 s."""
    piezas = [
        f'<circle cx="{CRONO_CX}" cy="{CRONO_CY}" r="{CRONO_R}" fill="{COLOR_CARATULA_CRONO}" '
        f'stroke="{COLOR_BISEL_EXTERNO}" stroke-width="2"/>'
    ]
    for i in range(12):
        piezas.append(linea_svg(CRONO_CX, CRONO_CY, 28, 33, i * 30, COLOR_MARCA_MINUTO, 1.5))
    piezas.append(manecilla(CRONO_CX, CRONO_CY, 30, 5, 1.5, COLOR_SEGUNDERO,
                            angulo_segundo(segundos % 60), 60))
    piezas.append(f'<circle cx="{CRONO_CX}" cy="{CRONO_CY}" r="2.5" fill="{COLOR_SEGUNDERO}"/>')
    minutos, seg = segundos // 60, segundos % 60
    piezas.append(
        f'<text x="{CRONO_CX}" y="470" text-anchor="middle" font-size="12" '
        f'letter-spacing="2" fill="{COLOR_TEXTO_SECUNDARIO}">CRONO {minutos}:{seg:02d}</text>'
    )
    return "\n".join(piezas)
