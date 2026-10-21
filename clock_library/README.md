# Reloj 1: librería propia (`mymath`)

Reloj analógico en ASCII hecho con Python y una librería matemática propia. Solo se importan módulos del propio proyecto (`mymath`, `core`, `clock_library`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `clock_library` (esta) | La librería matemática propia: seno y coseno sin `math` |
| `clock_terminal` | Interfaz de terminal con color y hora digital |
| `clock_svg` | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mymath` y `core` de la raíz del repositorio.

## Qué hace esta versión

- Usa la librería `mymath`: `PI`, reducción de ángulo, `sine` y `cosine` por serie de Taylor, geometría polar y ángulos de manecillas.
- `verify_library()` compara la librería con valores conocidos (opción 5 del menú).
- Esfera analógica en ASCII con manecillas de hora (`H`), minuto (`M`) y segundo (`s`).
- Hora inicial pedida al usuario con `input()`.
- Cronómetro y alarma (lógica compartida en `core`).

## Estructura

```
clock_library/
  __main__.py      punto de entrada (llama a main())
  menu.py          bucle del menú y ejecución de opciones
  input_reader.py  lectura de hora, segundos, alarma y cronómetro
  state.py         estado del reloj y avance del tiempo
  display.py       textos de la pantalla y del menú
  dial.py          lienzo ASCII de la esfera (marcas, números, DDA)
```

## Cómo ejecutarlo

Desde la raíz del repositorio:

```
py -3 -m clock_library
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.

Menú: `1` avanzar 1 s, `2` avanzar N s, `3` cronómetro, `4` alarma, `5` autotest, `0` salir.
