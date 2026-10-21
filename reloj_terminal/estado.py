"""Estado del reloj 2 y avance del tiempo (hora, cronómetro y alarma)."""

from nucleo.alarma import alarma_coincide, crear_alarma
from nucleo.cronometro import avanzar_cronometro, crear_cronometro
from nucleo.hora import siguiente_segundo


def crear_estado(segundos_inicio):
    """Crea el diccionario con todo el estado de la aplicación."""
    return {
        "segundos": segundos_inicio,
        "formato_24h": True,
        "cronometro": crear_cronometro(),
        "alarma": crear_alarma(),
        "parpadeo": False,
        "mensaje": "",
    }


def avanzar_un_segundo(estado):
    """Avanza el reloj un segundo y actualiza cronómetro y alarma."""
    estado["segundos"] = siguiente_segundo(estado["segundos"])
    avanzar_cronometro(estado["cronometro"])
    if alarma_coincide(estado["alarma"], estado["segundos"]):
        estado["alarma"]["sonando"] = True


def avanzar(estado, cantidad):
    """Avanza el reloj la cantidad de segundos indicada."""
    for _ in range(cantidad):
        avanzar_un_segundo(estado)
