# Reloj 2: terminal

Reloj de terminal que **corre solo**, con color ANSI. Solo se importan módulos del propio proyecto (`mymath`, `core`, `clock_terminal`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `clock_library` | Librerías propias: `mymath` y `minitk` (ventanas tipo tkinter) |
| `clock_terminal` (esta) | Interfaz de terminal con color y hora digital |
| `clock_svg` | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mymath` y `core` de la raíz del repositorio.

## Qué hace esta versión

- La pantalla se redibuja en el mismo sitio (sin parpadeo): esfera analógica dibujada con puntos braille (aro, una marca por hora, números, manecillas con cola y marca de la alarma), hora digital y cronómetro en dígitos grandes con los dos puntos parpadeando, y secciones con título (cronómetro, alarma y estado).
- Cronómetro y alarma avanzan con el reloj; la alarma suena con la campana de la terminal y parpadea en rojo unos 20 s.
- Formato 12 h / 24 h y 4 temas de color (clásico, neón, ámbar, hielo).
- `sine` y `cosine` de la librería propia `mymath` (serie de Taylor).
- Hora inicial pedida con `input()`; a partir de ahí el reloj corre por su cuenta. La hora se escribe como quieras: `14:30`, `14:30:15`, `2:30 pm`, `7am` o solo dígitos (`1430`, `230pm`, los `:` se ponen solos); los segundos son opcionales. Si escribes una hora de 1 a 12 sin am/pm, pregunta AM o PM (Enter la deja como 24 h).

## Cómo corre sin `time`

Sin `time` no se puede esperar un segundo, y sin librerías no se puede leer el teclado mientras el programa trabaja. Por eso:

- La espera es un bucle de trabajo fijo (`core/pacer.py`, con `sum(range(n))`), dividido en 10 cuadros por segundo.
- **Ctrl+C pausa el reloj** y abre el menú de comandos. `Enter` lo reanuda.
- Esa espera depende de la velocidad del computador. Si el reloj va rápido o lento: `Ctrl+C` → `k` (calibrar). Se deja correr el reloj mientras se cronometra con el celular, se para con `Ctrl+C` y se escriben los segundos reales; la velocidad se corrige sola. Conviene repetirlo una o dos veces.

## Menú de pausa (Ctrl+C)

Cada comando acepta su dato en la misma línea (`a 07:30:00`) o lo pregunta si se omite.

| Comando | Qué hace |
|---|---|
| `h [hora]` | Cambiar la hora (mismos formatos que arriba) |
| `n [N]` | Avanzar N segundos de golpe |
| `c [i\|p\|r]` | Cronómetro: iniciar, parar, reiniciar |
| `a [hora]` | Fijar la alarma (`a quitar` la borra). Con la hora en el comando no pregunta AM/PM: escribe `a 7:30 pm` |
| `f` | Alternar 12 h / 24 h |
| `t` | Cambiar de tema |
| `k` | Calibrar la velocidad |
| `q` | Salir |
| `Enter` | Seguir |

## Estructura

```
clock_terminal/
  __main__.py     punto de entrada (llama a main())
  application.py  alterna entre el reloj corriendo y el menú de pausa
  live.py         bucle en vivo: espera, avanza y redibuja hasta Ctrl+C
  commands.py     menú de pausa y sus comandos
  state.py        estado del reloj y avance del tiempo
  screen.py       panel lateral y construcción de la pantalla
  dial.py         esfera con puntos braille (core/braille.py) y colores por rol
  digits.py       hora digital con caracteres de bloque
  themes.py       temas de color
  ansi.py         códigos ANSI, cursor, longitud visible y cajas
```

## Cómo ejecutarlo

Requiere una terminal con colores ANSI de 24 bits, UTF-8 y fuente con caracteres braille (Windows Terminal con Cascadia lo trae) de al menos 80 columnas por 26 filas. Desde la raíz del repositorio:

```
py -3 -m clock_terminal
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.
