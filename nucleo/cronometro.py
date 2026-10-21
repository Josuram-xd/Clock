"""Cronómetro: estado y operaciones, sin interfaz."""


def crear_cronometro():
    """Cronómetro parado en 00:00."""
    return {"segundos": 0, "activo": False}


def iniciar_cronometro(cronometro):
    """Inicia o reanuda el cronómetro."""
    cronometro["activo"] = True


def parar_cronometro(cronometro):
    """Detiene el cronómetro conservando el tiempo."""
    cronometro["activo"] = False


def reiniciar_cronometro(cronometro):
    """Vuelve a 00:00 y deja el cronómetro parado."""
    cronometro["segundos"] = 0
    cronometro["activo"] = False


def avanzar_cronometro(cronometro, segundos=1):
    """Suma segundos solo si el cronómetro está en marcha."""
    if cronometro["activo"]:
        cronometro["segundos"] += segundos


def formatear_cronometro(segundos):
    """Segundos transcurridos -> 'MM:SS'."""
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


def descripcion_cronometro(cronometro):
    """'en marcha' o 'parado' según el estado."""
    return "en marcha" if cronometro["activo"] else "parado"
