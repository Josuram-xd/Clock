"""Pantalla del reloj 1: esfera y datos digitales."""

from nucleo.cronometro import descripcion_cronometro, formatear_cronometro
from nucleo.hora import formatear_hora
from reloj_libreria.esfera import ANCHO, mostrar_esfera

MENU = """
[1] Avanzar 1 segundo
[2] Avanzar N segundos
[3] Cronómetro
[4] Fijar alarma
[5] Autotest de la librería
[0] Salir"""


def texto_alarma(alarma):
    """Hora de la alarma o 'ninguna'."""
    return "ninguna" if alarma["hora"] is None else formatear_hora(alarma["hora"])


def dibujar_pantalla(estado):
    """Redibuja la esfera y los datos digitales."""
    cronometro = estado["cronometro"]
    print("=" * ANCHO)
    mostrar_esfera(estado["segundos"])
    print("=" * ANCHO)
    print(f"Hora digital: {formatear_hora(estado['segundos'])}")
    print(f"Cronómetro: {formatear_cronometro(cronometro['segundos'])} "
          f"({descripcion_cronometro(cronometro)})")
    print(f"Alarma: {texto_alarma(estado['alarma'])}")
