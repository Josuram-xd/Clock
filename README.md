# Taller: Desarrollo de un Reloj con Python

Reloj analógico en Python, entregado en **3 versiones independientes**, una por paquete, que comparten una librería matemática propia (`mymath`) y la lógica común (`core`).

## Reglas del taller

- Solo Python.
- La app debe tener frontend.
- Aumentar una funcionalidad pertinente (aquí: **cronómetro y alarma**).
- No usar HTML ni CSS.

Regla de imports del proyecto: **solo se importan módulos del propio proyecto** (`mymath`, `core` y los paquetes `clock_*`). No se importa ningún módulo de la librería estándar ni de terceros: el seno y el coseno son propios (serie de Taylor) y, como no se importa `time`, **la hora se pide al usuario con `input()` al iniciar** y los relojes corren por su cuenta con una espera calibrable (`core/pacer.py`).

## Convenciones

- El código (identificadores, comentarios y docstrings) está en **inglés**.
- Los textos que ve el usuario (menús, avisos, pantallas y el propio `reloj.svg`) están en **español**.
- Solo se importan módulos del propio proyecto (`mymath`, `core`, `clock_library`, `clock_terminal`, `clock_svg`). Ningún módulo de la librería estándar.
- La hora se pide siempre con `input()`; no se lee el reloj del sistema.

## Por qué hay 3 versiones

Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. En vez de apostar por una sola interpretación, se entregan tres enfoques del mismo reloj. Cada uno se puede ejecutar y evaluar solo.

| Paquete | Enfoque | Frontend |
|---|---|---|
| [`clock_library`](clock_library) | Librerías propias: `mymath` (`sine`, `cosine`, geometría polar) y `minitk`, una mini-librería de ventanas tipo tkinter | Ventana de aplicación en la terminal (Canvas de píxeles, tarjetas, barras de progreso, `after`) |
| [`clock_terminal`](clock_terminal) | Aplicación de terminal con colores ANSI, hora digital en bloques, temas y formato 12 h / 24 h | Terminal |
| [`clock_svg`](clock_svg) | Programa que escribe `reloj.svg` como texto, con manecillas y hora digital animadas | Gráfico SVG en el navegador |

## Estructura del repositorio

```
.
├── mymath/                   librería matemática propia
│   ├── trigonometry.py       PI, reduce_angle, sine, cosine, degrees_to_radians
│   ├── geometry.py           polar_point y ángulos de las manecillas
│   ├── raster.py             líneas (Bresenham), elipses, polígonos y relleno por barrido
│   └── verification.py       autotest de la librería (verify_library)
├── core/                     lógica compartida, sin interfaz
│   ├── time_utils.py         validación HH:MM:SS, conversiones y formatos
│   ├── stopwatch.py          estado y operaciones del cronómetro
│   ├── alarm.py              estado y operaciones de la alarma
│   ├── time_input.py         pregunta una hora: segundos opcionales, am/pm y sin ':'
│   ├── braille.py            cuadrícula de puntos braille (2×4 por celda); la usa la versión de terminal
│   ├── bigfont.py            dígitos grandes de 5 filas con bloques completos
│   └── pacer.py              espera sin reloj del sistema y calibración
├── clock_library/            versión 1 (ventana con minitk, una mini-librería tipo tkinter)
├── clock_terminal/           versión 2 (terminal ANSI)
├── clock_svg/                versión 3 (SVG, con un reloj.svg de ejemplo)
└── README.md
```

Cada paquete `clock_*` tiene su propio `README.md`, un `__main__.py` mínimo y módulos por responsabilidad.

## Cómo ejecutar

Requiere Python 3. En Windows se usa el lanzador `py`. Los comandos se ejecutan **desde la raíz del repositorio**:

```
py -3 -m clock_library
py -3 -m clock_terminal
py -3 -m clock_svg
```

- No uses `-I` (modo aislado): quita el directorio actual de la ruta de módulos y los paquetes del proyecto no se encontrarían.
- La versión 2 necesita una terminal con ANSI y UTF-8 (Windows Terminal).
- La versión 3 genera `reloj.svg` en la carpeta desde la que se ejecuta; se abre en cualquier navegador.

## Funcionalidades comunes

- Hora inicial pedida con `input()` y validada. En las versiones 1 y 2 acepta `14:30`, `2:30 pm`, `1430`…: segundos opcionales, am/pm y sin escribir los `:`.
- El reloj corre solo (versiones 1 y 2 con la espera de `core/pacer.py`; la 3 con animaciones SVG).
- Cronómetro.
- Alarma, incluido el cruce de medianoche.

## Cómo corren solos los relojes sin `time`

Sin `time` no hay `sleep` ni lectura del reloj del sistema, y sin librerías no se puede leer una tecla mientras el programa trabaja. En las versiones 1 y 2:

- Cada segundo se "espera" quemando trabajo fijo (`sum(range(n))`, ver `core/pacer.py`), en 10 cuadros por segundo.
- **Ctrl+C pausa** el reloj y abre un menú; `Enter` lo reanuda.
- Como esa espera depende del computador, se **calibra**: se deja correr mientras se cronometra con el celular, se para con `Ctrl+C` y se escriben los segundos reales (`k` en la versión 2, `calibrar` en la 1). El pacer corrige la velocidad solo.

## Limitaciones conocidas

- La hora inicial se escribe a mano: el reloj es tan exacto como esa hora y la calibración.
- Las versiones 1 y 2 se manejan con Ctrl+C y un menú, no con teclas en vivo.
- En la versión 3 el SVG arranca desde la hora escrita cada vez que se abre.
- El profesor indicó que SVG, librería propia y terminal no son válidos como frontend. Estas tres versiones son las alternativas posibles bajo la regla de no importar módulos externos al proyecto.
