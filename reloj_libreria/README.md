# Reloj 1: librería propia (`mimath`)

Reloj analógico en ASCII hecho con Python y una librería matemática propia. Solo se importan módulos del propio proyecto (`mimath`, `nucleo`, `reloj_libreria`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `reloj_libreria` (esta) | La librería matemática propia: seno y coseno sin `math` |
| `reloj_terminal` | Interfaz de terminal con color y hora digital |
| `reloj_svg` | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mimath` y `nucleo` de la raíz del repositorio.

## Qué hace esta versión

- Usa la librería `mimath`: `PI`, reducción de ángulo, `seno` y `coseno` por serie de Taylor, geometría polar y ángulos de manecillas.
- `verificar_libreria()` compara la librería con valores conocidos (opción 5 del menú).
- Esfera analógica en ASCII con manecillas de hora (`H`), minuto (`M`) y segundo (`s`).
- Hora inicial pedida al usuario con `input()`.
- Cronómetro y alarma (lógica compartida en `nucleo`).

## Estructura

```
reloj_libreria/
  __main__.py   punto de entrada (llama a principal())
  menu.py       bucle del menú y ejecución de opciones
  entrada.py    lectura de hora, segundos, alarma y cronómetro
  estado.py     estado del reloj y avance del tiempo
  pantalla.py   textos de la pantalla y menú
  esfera.py     lienzo ASCII de la esfera (marcas, números, DDA)
```

## Cómo ejecutarlo

Desde la raíz del repositorio:

```
py -3 -m reloj_libreria
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.

Menú: `1` avanzar 1 s, `2` avanzar N s, `3` cronómetro, `4` alarma, `5` autotest, `0` salir.
