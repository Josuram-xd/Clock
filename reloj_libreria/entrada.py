"""Entrada del usuario del reloj 1: hora, segundos, alarma y cronómetro."""

from nucleo.alarma import fijar_alarma, quitar_alarma
from nucleo.cronometro import iniciar_cronometro, parar_cronometro, reiniciar_cronometro
from nucleo.hora import convertir_hora, formatear_hora


def pedir_hora_inicial():
    """Pide la hora hasta que sea válida."""
    while True:
        segundos = convertir_hora(input("Hora inicial (HH:MM:SS): "))
        if segundos is not None:
            return segundos
        print("Hora inválida. Use HH:MM:SS con HH de 00 a 23 y MM/SS de 00 a 59.")


def pedir_cantidad_segundos():
    """Pide un entero positivo de segundos."""
    while True:
        texto = input("Segundos a avanzar: ").strip()
        if texto.isdecimal() and int(texto) > 0:
            return int(texto)
        print("Escriba un número entero mayor que 0.")


def configurar_alarma(estado):
    """Pide la hora de la alarma. Vacío cancela la alarma actual."""
    texto = input("Hora de la alarma (HH:MM:SS, vacío para cancelar): ").strip()
    if texto == "":
        quitar_alarma(estado["alarma"])
        print("Alarma cancelada.")
        return
    segundos = convertir_hora(texto)
    if segundos is None:
        print("Hora inválida. Use el formato HH:MM:SS.")
        return
    fijar_alarma(estado["alarma"], segundos)
    print(f"Alarma fijada a las {formatear_hora(segundos)}.")


def menu_cronometro(estado):
    """Iniciar/reanudar, parar o reiniciar el cronómetro."""
    print("  [1] iniciar/reanudar  [2] parar  [3] reiniciar (00:00)  [0] volver")
    opcion = input("Cronómetro> ").strip()
    cronometro = estado["cronometro"]
    if opcion == "1":
        iniciar_cronometro(cronometro)
    elif opcion == "2":
        parar_cronometro(cronometro)
    elif opcion == "3":
        reiniciar_cronometro(cronometro)
    elif opcion != "0":
        print("Opción de cronómetro inválida.")
