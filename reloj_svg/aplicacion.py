"""Programa principal del reloj 3: pide los datos y genera reloj.svg."""

from nucleo.alarma import segundos_hasta_alarma
from reloj_svg.archivo import escribir_archivo
from reloj_svg.constantes import NOMBRE_ARCHIVO
from reloj_svg.documento import construir_svg
from reloj_svg.entrada import pedir_cronometro, pedir_hora


def generar_reloj():
    """Pregunta hora, alarma y cronómetro; escribe el SVG y avisa al usuario."""
    print("=== Generador de reloj SVG ===")
    hora = pedir_hora("Hora inicial HH:MM:SS: ")
    alarma = pedir_hora("Hora de alarma HH:MM:SS (Enter para omitir): ", opcional=True)
    segundos_crono = pedir_cronometro()

    escribir_archivo(NOMBRE_ARCHIVO, construir_svg(hora, alarma, segundos_crono))

    if alarma is not None:
        print(f"La alarma sonara en el SVG dentro de {segundos_hasta_alarma(hora, alarma)} s de animacion.")
    print(f"Archivo generado: {NOMBRE_ARCHIVO} (en el directorio desde el que ejecutaste el programa).")
    print("Abrelo en tu navegador (doble clic, o arrastralo a una pestana abierta).")


def principal():
    """Ejecuta el generador y sale con elegancia si se cierra la entrada."""
    try:
        generar_reloj()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada terminada. No se genero el archivo.")
