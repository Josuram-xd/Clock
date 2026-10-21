"""Menú principal del reloj 1: bucle de opciones."""

from mimath import verificar_libreria
from nucleo.hora import formatear_hora
from reloj_libreria.entrada import (
    configurar_alarma,
    menu_cronometro,
    pedir_cantidad_segundos,
    pedir_hora_inicial,
)
from reloj_libreria.estado import avanzar, crear_estado
from reloj_libreria.pantalla import MENU, dibujar_pantalla


def avanzar_y_avisar(estado, cantidad):
    """Avanza el reloj y avisa si la alarma sonó."""
    hora_alarma = avanzar(estado, cantidad)
    if hora_alarma is not None:
        print(f"¡ALARMA! Son las {formatear_hora(hora_alarma)}")


def ejecutar_opcion(opcion, estado):
    """Ejecuta la acción elegida en el menú."""
    if opcion == "1":
        avanzar_y_avisar(estado, 1)
    elif opcion == "2":
        avanzar_y_avisar(estado, pedir_cantidad_segundos())
    elif opcion == "3":
        menu_cronometro(estado)
    elif opcion == "4":
        configurar_alarma(estado)
    elif opcion == "5":
        verificar_libreria()
    else:
        print("Opción inválida.")


def principal():
    """Bucle principal: dibuja, lee la opción y ejecuta la acción."""
    try:
        estado = crear_estado(pedir_hora_inicial())
        while True:
            dibujar_pantalla(estado)
            print(MENU)
            opcion = input("Opción: ").strip()
            if opcion == "0":
                break
            ejecutar_opcion(opcion, estado)
        print("Reloj apagado. ¡Hasta luego!")
    except EOFError:
        print("\nNo hay más entrada. Saliendo.")
