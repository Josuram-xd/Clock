# Reloj 2: terminal

Reloj de terminal con color ANSI. Solo se importan módulos del propio proyecto (`mimath`, `nucleo`, `reloj_terminal`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `reloj_libreria` | La librería matemática propia: seno y coseno sin `math` |
| `reloj_terminal` (esta) | Interfaz de terminal con color y hora digital |
| `reloj_svg` | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mimath` y `nucleo` de la raíz del repositorio.

## Qué hace esta versión

- Pantalla con bordes unicode y colores ANSI escritos a mano.
- Esfera analógica ASCII con manecillas de colores y hora digital en bloques.
- `seno` y `coseno` de la librería propia `mimath` (serie de Taylor).
- Hora inicial pedida con `input()`; el reloj avanza con el teclado, no hay pausas reales.
- Cronómetro, alarma y formato 12 h / 24 h.

## Estructura

```
reloj_terminal/
  __main__.py    punto de entrada (llama a principal())
  aplicacion.py  bucle principal
  acciones.py    entrada del usuario y ejecución de teclas
  estado.py      estado del reloj y avance del tiempo
  pantalla.py    textos de estado y construcción de la pantalla
  esfera.py      esfera analógica ASCII en color
  digitos.py     hora digital con caracteres de bloque
  ansi.py        colores ANSI, centrado y cajas
```

## Cómo ejecutarlo

Requiere una terminal con soporte de colores ANSI y UTF-8 (Windows Terminal). Desde la raíz del repositorio:

```
py -3 -m reloj_terminal
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.

Teclas: `Enter` +1 s, `n` avanzar N s, `c` cronómetro (`i` iniciar, `p` parar, `r` reiniciar), `a` alarma (vacío la quita), `f` 12 h / 24 h, `q` salir.
