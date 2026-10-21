# Reloj 2: terminal

Reloj de terminal con color ANSI, hecho solo con Python y **cero `import`**.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `1-reloj-libreria-propia` | La librería matemática propia: seno y coseno sin `math` |
| `2-reloj-terminal` (esta) | Interfaz de terminal con color y hora digital |
| `3-reloj-svg` | Frontend gráfico generado como texto SVG |

Cada carpeta es independiente: se puede ejecutar y evaluar sola.

## Qué hace esta versión

- Pantalla con bordes unicode y colores ANSI escritos a mano.
- Esfera analógica ASCII con manecillas de colores y hora digital en bloques.
- `seno` y `coseno` propios por serie de Taylor.
- Hora inicial pedida con `input()`; sin `import` no hay acceso al reloj del sistema ni pausas reales, así que el reloj avanza con el teclado.
- Cronómetro, alarma y formato 12 h / 24 h.

## Cómo ejecutarlo

Requiere una terminal con soporte de colores ANSI y UTF-8 (Windows Terminal).

```
py -3 main.py
```

Teclas: `Enter` +1 s, `n` avanzar N s, `c` cronómetro (`i` iniciar, `p` parar, `r` reiniciar), `a` alarma (vacío la quita), `f` 12 h / 24 h, `q` salir.
