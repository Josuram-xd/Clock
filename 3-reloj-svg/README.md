# Reloj 3: SVG

Python escribe un archivo `reloj.svg` como texto, sin `import` y sin HTML ni CSS.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `1-reloj-libreria-propia` | La librería matemática propia: seno y coseno sin `math` |
| `2-reloj-terminal` | Interfaz de terminal con color y hora digital |
| `3-reloj-svg` (esta) | Frontend gráfico generado como texto SVG |

Cada carpeta es independiente: se puede ejecutar y evaluar sola.

## Qué hace esta versión

- Pide la hora con `input()`, una alarma opcional y un cronómetro opcional.
- Genera `reloj.svg` con `open()` (función built-in): esfera, 60 marcas, números y manecillas, todo calculado con `seno` y `coseno` propios.
- Las manecillas giran solas con `<animateTransform>`, partiendo de la hora ingresada.
- Cronómetro como mini-dial animado.
- Alarma: marca roja en la esfera y aviso «¡ALARMA!» parpadeante al llegar la hora, con `<set>` y `<animate>`.
- Solo atributos de presentación SVG: no hay `<style>`, `style=` ni archivos `.html`.

## Cómo ejecutarlo

```
py -3 main.py
```

Luego abre `reloj.svg` (se guarda en la carpeta desde la que ejecutas el programa) en cualquier navegador.

Limitación: la hora digital del SVG es estática; actualizarla exigiría scripts.
