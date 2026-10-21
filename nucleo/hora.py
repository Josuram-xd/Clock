"""Hora del día: validación de HH:MM:SS, conversión a segundos y formatos."""

SEGUNDOS_DIA = 86400


def a_segundos(horas, minutos, segundos):
    """Convierte hora, minuto y segundo en segundos desde medianoche."""
    return horas * 3600 + minutos * 60 + segundos


def desde_segundos(total):
    """Devuelve (horas, minutos, segundos) a partir de segundos desde medianoche."""
    return total // 3600, (total % 3600) // 60, total % 60


def convertir_hora(texto, dos_cifras=True):
    """Segundos del día para 'HH:MM:SS', o None si el texto no es válido.

    Con dos_cifras=True cada parte debe tener exactamente dos dígitos ('07:05:09');
    con False se aceptan también partes cortas ('7:5:9').
    """
    partes = texto.strip().split(":")
    if len(partes) != 3:
        return None
    for parte in partes:
        solo_ascii = parte != "" and all("0" <= c <= "9" for c in parte)
        if not solo_ascii or (dos_cifras and len(parte) != 2):
            return None
    horas, minutos, segundos = (int(parte) for parte in partes)
    if horas > 23 or minutos > 59 or segundos > 59:
        return None
    return a_segundos(horas, minutos, segundos)


def siguiente_segundo(total):
    """Segundos del día un segundo después (vuelve a 0 tras la medianoche)."""
    return (total + 1) % SEGUNDOS_DIA


def formatear_hora(total):
    """Segundos del día -> 'HH:MM:SS' en formato 24 horas."""
    horas, minutos, segundos = desde_segundos(total)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def formatear_hora_12h(total):
    """Segundos del día -> ('HH:MM:SS' en formato 12 horas, 'AM' o 'PM')."""
    horas, minutos, segundos = desde_segundos(total)
    sufijo = "AM" if horas < 12 else "PM"
    horas_12 = horas % 12 or 12
    return f"{horas_12:02d}:{minutos:02d}:{segundos:02d}", sufijo
