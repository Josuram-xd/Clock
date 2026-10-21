"""Alarma: estado y operaciones, incluido el cruce de medianoche."""

from nucleo.hora import SEGUNDOS_DIA


def crear_alarma():
    """Alarma sin hora fijada y sin sonar."""
    return {"hora": None, "sonando": False}


def fijar_alarma(alarma, segundos):
    """Fija la hora de la alarma (segundos del día)."""
    alarma["hora"] = segundos


def quitar_alarma(alarma):
    """Quita la hora fijada y apaga la alarma si sonaba."""
    alarma["hora"] = None
    alarma["sonando"] = False


def alarma_coincide(alarma, segundos):
    """True si hay alarma fijada y es la hora indicada."""
    return alarma["hora"] is not None and alarma["hora"] == segundos


def segundos_hasta_alarma(segundos_actuales, hora_alarma):
    """Segundos que faltan (1 a 86400) hasta la alarma, cruzando la medianoche."""
    faltan = (hora_alarma - segundos_actuales) % SEGUNDOS_DIA
    return faltan if faltan > 0 else SEGUNDOS_DIA
