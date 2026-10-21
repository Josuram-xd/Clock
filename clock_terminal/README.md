# Reloj 2: terminal

Reloj de terminal con color ANSI. Solo se importan módulos del propio proyecto (`mymath`, `core`, `clock_terminal`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `clock_library` | La librería matemática propia: seno y coseno sin `math` |
| `clock_terminal` (esta) | Interfaz de terminal con color y hora digital |
| `clock_svg` | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mymath` y `core` de la raíz del repositorio.

## Qué hace esta versión

- Pantalla con bordes unicode y colores ANSI escritos a mano.
- Esfera analógica ASCII con manecillas de colores y hora digital en bloques.
- `sine` y `cosine` de la librería propia `mymath` (serie de Taylor).
- Hora inicial pedida con `input()`; el reloj avanza con el teclado, no hay pausas reales.
- Cronómetro, alarma y formato 12 h / 24 h.

## Estructura

```
clock_terminal/
  __main__.py    punto de entrada (llama a main())
  application.py bucle principal de pantalla y teclas
  actions.py     entrada del usuario y ejecución de teclas
  state.py       estado del reloj y avance del tiempo
  screen.py      textos de estado y construcción de la pantalla
  dial.py        esfera analógica ASCII en color
  digits.py      hora digital con caracteres de bloque
  ansi.py        colores ANSI, longitud visible, centrado y cajas
```

## Cómo ejecutarlo

Requiere una terminal con soporte de colores ANSI y UTF-8 (Windows Terminal). Desde la raíz del repositorio:

```
py -3 -m clock_terminal
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.

Teclas: `Enter` +1 s, `n` avanzar N s, `c` cronómetro (`i` iniciar, `p` parar, `r` reiniciar), `a` alarma (vacío la quita), `f` 12 h / 24 h, `q` salir.
