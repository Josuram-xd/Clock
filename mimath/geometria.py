"""Geometría del reloj: puntos polares y ángulos de las manecillas."""

from mimath.trigonometria import coseno, grados_a_radianes, seno


def angulo_manecilla(valor, maximo):
    """Ángulo en grados de una manecilla: 0 en las 12 y sentido horario."""
    return valor / maximo * 360


def punto_polar(cx, cy, radio, angulo_grados):
    """
    Devuelve (x, y) a 'radio' del centro (cx, cy).
    El ángulo se mide desde las 12 en sentido horario y el eje Y apunta hacia arriba.
    """
    radianes = grados_a_radianes(angulo_grados)
    x = cx + radio * seno(radianes)
    y = cy + radio * coseno(radianes)
    return x, y


def angulo_segundo(segundos):
    """Ángulo en grados de la manecilla de los segundos."""
    return segundos * 6.0


def angulo_minuto(minutos, segundos):
    """Ángulo en grados de la manecilla de los minutos."""
    return (minutos * 60 + segundos) * 0.1


def angulo_hora(horas, minutos, segundos):
    """Ángulo en grados de la manecilla de las horas (esfera de 12 h)."""
    return (horas % 12) * 30 + minutos * 0.5 + segundos / 120
