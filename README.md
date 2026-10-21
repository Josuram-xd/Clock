# Taller: Desarrollo de un Reloj con Python

Reloj analógico en Python, entregado en **3 versiones independientes**, una por carpeta.

## Reglas del taller

- Solo Python.
- La app debe tener frontend.
- Aumentar una funcionalidad pertinente (aquí: **cronómetro y alarma**).
- No usar HTML ni CSS.

Además, el código no usa ningún `import`: el seno y el coseno son propios (serie de Taylor), y como Python no puede leer la hora del sistema sin importar `time`, **la hora se pide al usuario al iniciar**.

## Por qué hay 3 carpetas

Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. En vez de apostar por una sola interpretación, se entregan tres enfoques del mismo reloj. Cada carpeta se puede ejecutar y evaluar sola.

| Carpeta | Enfoque | Frontend |
|---|---|---|
| [`1-reloj-libreria-propia`](1-reloj-libreria-propia) | Librería matemática propia (`mimath`): `seno`, `coseno`, geometría polar y autotest | Esfera ASCII |
| [`2-reloj-terminal`](2-reloj-terminal) | Aplicación de terminal con colores ANSI, hora digital en bloques y formato 12 h / 24 h | Terminal |
| [`3-reloj-svg`](3-reloj-svg) | Programa que escribe `reloj.svg` como texto, con manecillas animadas | Gráfico SVG en el navegador |

## Cómo ejecutar

Requiere Python 3. En Windows se usa el lanzador `py`:

```
py -3 1-reloj-libreria-propia/main.py
py -3 2-reloj-terminal/main.py
py -3 3-reloj-svg/main.py
```

- La versión 2 necesita una terminal con ANSI y UTF-8 (Windows Terminal).
- La versión 3 genera `reloj.svg` en la carpeta desde la que se ejecuta; se abre en cualquier navegador.

## Funcionalidades comunes

- Hora inicial pedida con `input()` y validada (`HH:MM:SS`).
- Cronómetro.
- Alarma, incluido el cruce de medianoche.

## Limitaciones conocidas

- Sin `import` no hay pausas ni tiempo real: en las versiones 1 y 2 el reloj avanza con el teclado.
- En la versión 3 la hora digital del SVG es estática; las manecillas sí giran solas.
- El profesor indicó que SVG, librería propia y terminal no son válidos como frontend. Estas tres versiones son las alternativas posibles bajo la regla de no usar `import`.

## Cómo se construyó

Cada versión la construyó un agente con un modelo económico, la revisó un agente con un modelo intermedio y una revisión final independiente probó las tres de punta a punta.
