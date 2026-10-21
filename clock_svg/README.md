# Reloj 3: SVG

Python escribe un archivo `reloj.svg` como texto, sin HTML ni CSS. Solo se importan módulos del propio proyecto (`mymath`, `core`, `clock_svg`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `clock_library` | La librería matemática propia: seno y coseno sin `math` |
| `clock_terminal` | Interfaz de terminal con color y hora digital |
| `clock_svg` (esta) | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mymath` y `core` de la raíz del repositorio.

## Qué hace esta versión

- Pide la hora con `input()`, una alarma opcional y un cronómetro opcional.
- Genera `reloj.svg` con `open()` (función built-in): esfera, 60 marcas, números y manecillas, todo calculado con `sine` y `cosine` de `mymath`.
- Las manecillas giran solas con `<animateTransform>`, partiendo de la hora ingresada.
- Cronómetro como mini-dial animado.
- Alarma: marca roja en la esfera y aviso «¡ALARMA!» parpadeante al llegar la hora, con `<set>` y `<animate>`.
- Solo atributos de presentación SVG: no hay `<style>`, `style=` ni archivos `.html`.

## Estructura

```
clock_svg/
  __main__.py       punto de entrada (llama a main())
  application.py    flujo principal: pide datos y genera el archivo
  input_reader.py   lectura de hora, alarma y cronómetro
  document.py       ensamblado del documento SVG completo
  elements.py       líneas, bisel, marcas, números y manecillas
  alarm_svg.py      marca y aviso de la alarma
  stopwatch_svg.py  mini-dial del cronómetro
  constants.py      geometría, paleta y fuentes
  file_writer.py    escritura del SVG en disco
  reloj.svg         ejemplo ya generado
```

## Cómo ejecutarlo

Desde la raíz del repositorio:

```
py -3 -m clock_svg
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.

Luego abre `reloj.svg` (se guarda en la carpeta desde la que ejecutas el programa) en cualquier navegador.

Limitación: la hora digital del SVG es estática; actualizarla exigiría scripts.
