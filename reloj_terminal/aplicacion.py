"""Programa principal del reloj 2: bucle de pantalla y teclas."""

from reloj_terminal.acciones import pedir_hora_inicial, procesar_opcion
from reloj_terminal.ansi import CIAN, LIMPIAR_PANTALLA, colorear
from reloj_terminal.estado import crear_estado
from reloj_terminal.pantalla import mostrar


def bucle_principal():
    """Pide la hora, dibuja y procesa teclas hasta salir."""
    print(LIMPIAR_PANTALLA + colorear("Bienvenido al reloj de terminal.", CIAN))
    estado = crear_estado(pedir_hora_inicial())
    continuar = True
    while continuar:
        estado["parpadeo"] = not estado["parpadeo"]
        mostrar(estado)
        estado["mensaje"] = ""
        opcion = input("Opción: ").strip().lower()
        continuar = procesar_opcion(estado, opcion)
    print("Hasta luego.")


def principal():
    """Ejecuta el reloj y sale con elegancia si se cierra la entrada."""
    try:
        bucle_principal()
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego.")
