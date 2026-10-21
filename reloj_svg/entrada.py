"""Entrada del usuario del reloj 3: hora, alarma opcional y cronómetro opcional."""

from nucleo.hora import convertir_hora


def pedir_hora(mensaje, opcional=False):
    """Pide una hora (en segundos del día) hasta que sea válida. Si es opcional, Enter da None."""
    while True:
        texto = input(mensaje)
        if opcional and texto.strip() == "":
            return None
        valor = convertir_hora(texto, dos_cifras=False)
        if valor is not None:
            return valor
        print("Formato no valido. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def pedir_si_o_no(mensaje):
    """Pregunta hasta recibir 's' o 'n'. Devuelve True para 's'."""
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Responde s o n.")


def pedir_segundos_crono():
    """Pide los segundos de arranque del cronómetro (entero de 0 o más)."""
    while True:
        texto = input("Duracion de arranque del cronometro en segundos: ").strip()
        if texto.isdecimal():
            return int(texto)
        print("Escribe un numero entero de segundos (0 o mas).")


def pedir_cronometro():
    """Devuelve None si no quiere cronómetro; si lo quiere, sus segundos de arranque."""
    if not pedir_si_o_no("Quieres cronometro? (s/n): "):
        return None
    return pedir_segundos_crono()
