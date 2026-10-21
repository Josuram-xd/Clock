# Reloj 3: SVG

Python escribe un archivo `reloj.svg` como texto, sin HTML ni CSS. Solo se importan módulos del propio proyecto (`mimath`, `nucleo`, `reloj_svg`); no se importa nada de la librería estándar ni de terceros.

## Por qué existen 3 carpetas

El taller pide un reloj en Python con frontend, sin HTML ni CSS. Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. Por eso se entregan tres versiones del mismo reloj, cada una con un enfoque distinto:

| Carpeta | Enfoque |
|---|---|
| `reloj_libreria` | La librería matemática propia: seno y coseno sin `math` |
| `reloj_terminal` | Interfaz de terminal con color y hora digital |
| `reloj_svg` (esta) | Frontend gráfico generado como texto SVG |

Cada versión se ejecuta y evalúa sola; las tres comparten los paquetes `mimath` y `nucleo` de la raíz del repositorio.

## Qué hace esta versión

- Pide la hora con `input()`, una alarma opcional y un cronómetro opcional.
- Genera `reloj.svg` con `open()` (función built-in): esfera, 60 marcas, números y manecillas, todo calculado con `seno` y `coseno` de `mimath`.
- Las manecillas giran solas con `<animateTransform>`, partiendo de la hora ingresada.
- Cronómetro como mini-dial animado.
- Alarma: marca roja en la esfera y aviso «¡ALARMA!» parpadeante al llegar la hora, con `<set>` y `<animate>`.
- Solo atributos de presentación SVG: no hay `<style>`, `style=` ni archivos `.html`.

## Estructura

```
reloj_svg/
  __main__.py       punto de entrada (llama a principal())
  aplicacion.py     flujo principal: pide datos y genera el archivo
  entrada.py        lectura de hora, alarma y cronómetro
  documento.py      ensamblado del documento SVG completo
  elementos.py      líneas, bisel, marcas, números y manecillas
  alarma_svg.py     marca y aviso de la alarma
  cronometro_svg.py mini-dial del cronómetro
  constantes.py     geometría, paleta y fuentes
  archivo.py        escritura del SVG en disco
  reloj.svg         ejemplo ya generado
```

## Cómo ejecutarlo

Desde la raíz del repositorio:

```
py -3 -m reloj_svg
```

No uses `-I`: ese modo quita el directorio actual de la ruta de módulos y Python no encontraría los paquetes del proyecto.

Luego abre `reloj.svg` (se guarda en la carpeta desde la que ejecutas el programa) en cualquier navegador.

Limitación: la hora digital del SVG es estática; actualizarla exigiría scripts.
