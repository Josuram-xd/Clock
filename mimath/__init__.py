"""Librería matemática propia: trigonometría, geometría polar y autotest."""

from mimath.geometria import (
    angulo_hora,
    angulo_manecilla,
    angulo_minuto,
    angulo_segundo,
    punto_polar,
)
from mimath.trigonometria import (
    PI,
    coseno,
    grados_a_radianes,
    reducir_angulo,
    seno,
)
from mimath.verificacion import verificar_libreria

__all__ = [
    "PI",
    "angulo_hora",
    "angulo_manecilla",
    "angulo_minuto",
    "angulo_segundo",
    "coseno",
    "grados_a_radianes",
    "punto_polar",
    "reducir_angulo",
    "seno",
    "verificar_libreria",
]
