# Reloj 1: librería propia (`minitk` + `mymath`)

Reloj analógico que **corre solo**, hecho con dos librerías escritas desde cero: `mymath` (seno y coseno por serie de Taylor) y **`minitk`**, una mini-librería de ventanas al estilo de `tkinter` que dibuja en la terminal. Solo se importan módulos del propio proyecto; no se importa nada de la librería estándar ni de terceros (ni siquiera `tkinter`).

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `clock_library` (esta) | Librerías propias: `mymath` y `minitk` (ventanas tipo tkinter) |
| `clock_terminal` | Interfaz de terminal con color y hora digital |
| `clock_svg` | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mymath` y `core` de la raíz del repositorio.

## Cómo se ve y cómo se usa

La hora se escribe como quieras: `14:30`, `2:30 pm`, `7am` o solo dígitos (`1430`, `230pm`); los segundos son opcionales y, si escribes una hora de 1 a 12 sin am/pm, pregunta AM o PM (Enter la deja como 24 h).

Ventana con la esfera analógica (dibujada con un `Canvas`), paneles con título para la hora, el cronómetro y la alarma (con dígitos grandes) y dos filas de botones de colores. El reloj avanza por su cuenta: no hay que pulsar nada para que se mueva.

Sin `time` ni lectura de teclado no se puede esperar un segundo ni detectar una tecla mientras corre el programa, así que:

- **Ctrl+C pausa la ventana** y abre un menú de teclas: escribe la tecla de un botón (por ejemplo `a` para la alarma) y se dispara como si lo pulsaras. `Enter` vuelve al reloj.
- La espera es un bucle de trabajo fijo (`core/pacer.py`). Su duración depende del computador: si el reloj va rápido o lento, `Ctrl+C` → `calibrar`, se cronometra con el celular y se corrige sola la velocidad.

| Tecla | Botón |
|---|---|
| `c` | Cronómetro (iniciar / parar) |
| `r` | Reiniciar el cronómetro |
| `a` | Fijar la alarma |
| `x` | Quitar la alarma |
| `h` | Cambiar la hora |
| `n` | Avanzar N segundos |
| `f` | 12 h / 24 h |
| `v` | Autotest de `mymath` |
| `q` | Salir |

## `minitk`: la mini-librería tipo tkinter

Se usa igual que tkinter: widgets que se colocan con `pack()`, temporizadores con `after()`, teclas con `bind()` y un `mainloop()`.

```python
from clock_library import minitk as tk

root = tk.Tk("Hola")
canvas = tk.Canvas(root, width=20, height=6, bg="navy")
canvas.pack()
canvas.create_oval(1, 1, 18, 10, outline="cyan")
label = tk.Label(root, text="0", fg="yellow")
label.pack()

count = [0]
def tick():
    root.after(1000, tick)            # se reprograma primero
    count[0] += 1
    label["text"] = str(count[0])

tk.Button(root, text="Salir", key="q", command=root.quit).pack()
root.after(1000, tick)
root.mainloop()
```

| Módulo | Qué hace |
|---|---|
| `window.py` | `Tk`: ventana, bucle de eventos, `after`, `bind`, menú de Ctrl+C y calibración |
| `widgets.py` | `Widget`, `Frame` (organiza con `pack`), `Label` (texto o fuente grande) y `Button` |
| `canvas.py` | `Canvas` con `create_line`, `create_oval`, `create_rectangle`, `create_text`, `coords`, `itemconfigure`, `delete`; dibuja con puntos braille |
| `surface.py` | Cuadrícula de celdas (carácter, color, fondo) que se imprime con códigos ANSI |
| `colors.py` | Nombres de color y `#rrggbb` a RGB de 24 bits |
| `fonts.py` | Dígitos grandes de 3 filas con caracteres de bloque |
| `dialogs.py` | `askstring`, `askinteger` y `showinfo` |

Cada celda de la terminal es una cuadrícula de 2×4 puntos braille (`core/braille.py`), así el `Canvas` tiene 4 veces más resolución que la cuadrícula de caracteres y sus píxeles son cuadrados (una esfera de 40×20 celdas son 80×80 píxeles). Las líneas, óvalos y rectángulos los calcula `mymath/raster.py` (Bresenham y elipses con el seno y coseno propios).

## Estructura

```
clock_library/
  __main__.py     punto de entrada
  application.py  pide la hora, arma la ventana y programa el tic de 1 s con after()
  interface.py    widgets de la ventana (esfera, textos y botones)
  dial.py         esfera y manecillas sobre el Canvas (usa mymath)
  actions.py      qué hace cada botón
  state.py        estado del reloj y avance del tiempo
  minitk/         la mini-librería de ventanas
```

## Cómo ejecutarlo

Desde la raíz del repositorio, en una terminal con colores de 24 bits, UTF-8 y fuente con caracteres braille (Windows Terminal con Cascadia lo trae) de al menos 80 columnas por 26 filas:

```
py -3 -m clock_library
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.
