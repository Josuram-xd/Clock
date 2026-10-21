"""Dígitos tipo 7 segmentos con caracteres de bloque (3 filas)."""

FUENTE_DIGITOS = {
    "0": ["█▀█", "█ █", "█▄█"],
    "1": [" ▄█", "  █", "  ▀"],
    "2": ["▀▀█", "█▀▀", "▀▀▀"],
    "3": ["▀▀█", " ▄█", "▀▀▀"],
    "4": ["█ █", "▀▀█", "  ▀"],
    "5": ["█▀▀", "▀▀█", "▀▀▀"],
    "6": ["█▀▀", "█▀█", "▀▀▀"],
    "7": ["▀▀█", "  █", "  ▀"],
    "8": ["█▀█", "█▀█", "▀▀▀"],
    "9": ["█▀█", "▀▀█", "▀▀▀"],
    ":": [" █ ", "   ", " █ "],
}


def dibujar_digital(texto):
    """Devuelve las 3 filas de un texto como 'HH:MM:SS' en bloques."""
    filas = ["", "", ""]
    for indice, caracter in enumerate(texto):
        glifo = FUENTE_DIGITOS[caracter]
        for fila in range(3):
            if indice > 0:
                filas[fila] += "  "
            filas[fila] += glifo[fila]
    return filas
