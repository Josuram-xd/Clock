"""Escritura del SVG en disco."""


def escribir_archivo(ruta, contenido):
    """Guarda el contenido en UTF-8 en la ruta indicada."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
