"""Estado del reloj 1 y avance del tiempo (hora, cronómetro y alarma)."""

from nucleo.alarma import alarma_coincide, crear_alarma, quitar_alarma
from nucleo.cronometro import avanzar_cronometro, crear_cronometro
from nucleo.hora import siguiente_segundo


def crear_estado(segundos_inicio):
    """Estado del reloj: hora, cronómetro y alarma."""
    return {
        "segundos": segundos_inicio,
        "cronometro": crear_cronometro(),
        "alarma": crear_alarma(),
    }


def avanzar_un_segundo(estado):
    """Avanza 1 s. Devuelve True si la alarma suena en ese segundo."""
    estado["segundos"] = siguiente_segundo(estado["segundos"])
    avanzar_cronometro(estado["cronometro"])
    if alarma_coincide(estado["alarma"], estado["segundos"]):
        quitar_alarma(estado["alarma"])
        return True
    return False


def avanzar(estado, cantidad):
    """Avanza 'cantidad' segundos. Devuelve la hora de la alarma si sonó, o None."""
    hora_alarma = estado["alarma"]["hora"]
    suena = False
    for _ in range(cantidad):
        if avanzar_un_segundo(estado):
            suena = True
    return hora_alarma if suena else None
