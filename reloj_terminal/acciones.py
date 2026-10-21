"""Entrada del usuario del reloj 2: pide datos y ejecuta la tecla pulsada."""

from nucleo.alarma import alarma_coincide, fijar_alarma, quitar_alarma
from nucleo.cronometro import iniciar_cronometro, parar_cronometro, reiniciar_cronometro
from nucleo.hora import convertir_hora, formatear_hora
from reloj_terminal.estado import avanzar

LIMITE_AVANCE = 604800  # una semana en segundos


def leer_entero(texto, minimo, maximo):
    """Convierte texto en entero dentro de [minimo, maximo]. Devuelve None si no es válido."""
    try:
        valor = int(texto)
    except ValueError:
        return None
    if valor < minimo or valor > maximo:
        return None
    return valor


def pedir_hora_inicial():
    """Pide la hora inicial y la repite hasta que sea válida."""
    while True:
        segundos = convertir_hora(input("Hora inicial (HH:MM:SS): "), dos_cifras=False)
        if segundos is not None:
            return segundos
        print("Hora no válida. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def accion_avanzar_segundos(estado):
    """Pide cuántos segundos avanzar y los avanza."""
    cantidad = leer_entero(input("Segundos a avanzar (0-604800): "), 0, LIMITE_AVANCE)
    if cantidad is None:
        estado["mensaje"] = "Cantidad no válida."
        return
    avanzar(estado, cantidad)
    estado["mensaje"] = "Avanzados " + str(cantidad) + " s."


def accion_cronometro(estado):
    """Inicia, para o reinicia el cronómetro."""
    opcion = input("Cronómetro: [i] iniciar  [p] parar  [r] reiniciar: ").strip().lower()
    cronometro = estado["cronometro"]
    if opcion == "i":
        iniciar_cronometro(cronometro)
        estado["mensaje"] = "Cronómetro en marcha."
    elif opcion == "p":
        parar_cronometro(cronometro)
        estado["mensaje"] = "Cronómetro parado."
    elif opcion == "r":
        reiniciar_cronometro(cronometro)
        estado["mensaje"] = "Cronómetro reiniciado."
    else:
        estado["mensaje"] = "Opción de cronómetro no válida."


def accion_alarma(estado):
    """Fija la alarma, o la quita si se deja vacía."""
    alarma = estado["alarma"]
    texto = input("Alarma HH:MM:SS (vacío = quitar): ").strip()
    if texto == "":
        quitar_alarma(alarma)
        estado["mensaje"] = "Alarma quitada."
        return
    segundos = convertir_hora(texto, dos_cifras=False)
    if segundos is None:
        estado["mensaje"] = "Hora de alarma no válida."
        return
    fijar_alarma(alarma, segundos)
    alarma["sonando"] = alarma_coincide(alarma, estado["segundos"])
    estado["mensaje"] = "Alarma fijada a " + formatear_hora(segundos) + "."


def procesar_opcion(estado, opcion):
    """Ejecuta la acción de la tecla pulsada. Devuelve False si el usuario sale."""
    if opcion == "":
        avanzar(estado, 1)
    elif opcion == "n":
        accion_avanzar_segundos(estado)
    elif opcion == "c":
        accion_cronometro(estado)
    elif opcion == "a":
        accion_alarma(estado)
    elif opcion == "f":
        estado["formato_24h"] = not estado["formato_24h"]
    elif opcion == "q":
        return False
    else:
        estado["mensaje"] = "Opción no válida: " + opcion
    return True
