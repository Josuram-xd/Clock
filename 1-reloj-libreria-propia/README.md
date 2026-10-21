# Reloj 1: librería propia (`mimath`)

Reloj analógico en ASCII hecho solo con Python y **cero `import`**.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `1-reloj-libreria-propia` (esta) | La librería matemática propia: seno y coseno sin `math` |
| `2-reloj-terminal` | Interfaz de terminal con color y hora digital |
| `3-reloj-svg` | Frontend gráfico generado como texto SVG |

Cada carpeta es independiente: se puede ejecutar y evaluar sola.

## Qué hace esta versión

- Librería `mimath` dentro del mismo `main.py`: `PI`, reducción de ángulo, `seno` y `coseno` por serie de Taylor, geometría polar y ángulos de manecillas.
- `verificar_libreria()` compara la librería con valores conocidos (opción 5 del menú).
- Esfera analógica en ASCII con manecillas de hora (`H`), minuto (`M`) y segundo (`s`).
- Hora inicial pedida al usuario con `input()`, porque sin `import` Python no puede leer el reloj del sistema.
- Cronómetro y alarma.

## Cómo ejecutarlo

```
py -3 main.py
```

Menú: `1` avanzar 1 s, `2` avanzar N s, `3` cronómetro, `4` alarma, `5` autotest, `0` salir.
