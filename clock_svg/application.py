"""Main program of clock 3: asks for the data and generates reloj.svg."""

from core.alarm import seconds_until_alarm
from clock_svg.file_writer import write_file
from clock_svg.constants import FILE_NAME
from clock_svg.document import build_svg
from clock_svg.input_reader import ask_stopwatch, ask_time, ask_yes_no


def generate_clock():
    """Ask for the time, the alarm and the stopwatch; write the SVG and tell the user."""
    print("=== Generador de reloj SVG ===")
    start_time = ask_time("Hora inicial HH:MM:SS: ")
    alarm = ask_time("Hora de alarma HH:MM:SS (Enter para omitir): ", optional=True)
    stopwatch_seconds = ask_stopwatch()
    twelve_hour = ask_yes_no("¿Mostrar la hora en formato de 12 h con AM/PM? (s/n): ")

    write_file(FILE_NAME, build_svg(start_time, alarm, stopwatch_seconds, twelve_hour))

    if alarm is not None:
        remaining = seconds_until_alarm(start_time, alarm)
        print(f"La alarma sonará en el SVG dentro de {remaining} s de animación.")
    print("Las manecillas, la hora digital y el cronómetro avanzan solos desde la hora que escribiste.")
    print(f"Archivo generado: {FILE_NAME} (en el directorio desde el que ejecutaste el programa).")
    print("Ábrelo en tu navegador (doble clic, o arrástralo a una pestaña abierta).")


def main():
    """Run the generator and exit gracefully if the input is closed."""
    try:
        generate_clock()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada terminada. No se generó el archivo.")
