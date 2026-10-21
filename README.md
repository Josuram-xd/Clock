# Taller: Desarrollo de un Reloj con Python

Reloj analógico en Python, entregado en **3 versiones independientes**, una por paquete, que comparten una librería matemática propia (`mimath`) y la lógica común (`nucleo`).

## Reglas del taller

- Solo Python.
- La app debe tener frontend.
- Aumentar una funcionalidad pertinente (aquí: **cronómetro y alarma**).
- No usar HTML ni CSS.

Regla de imports del proyecto: **solo se importan módulos del propio proyecto** (`mimath`, `nucleo` y los paquetes `reloj_*`). No se importa ningún módulo de la librería estándar ni de terceros: el seno y el coseno son propios (serie de Taylor) y, como no se importa `time`, **la hora se pide al usuario con `input()` al iniciar**.

## Por qué hay 3 versiones

Las reglas dejan dudas sobre qué cuenta como frontend sin usar librerías. En vez de apostar por una sola interpretación, se entregan tres enfoques del mismo reloj. Cada uno se puede ejecutar y evaluar solo.

| Paquete | Enfoque | Frontend |
|---|---|---|
| [`reloj_libreria`](reloj_libreria) | Librería matemática propia (`mimath`): `seno`, `coseno`, geometría polar y autotest | Esfera ASCII |
| [`reloj_terminal`](reloj_terminal) | Aplicación de terminal con colores ANSI, hora digital en bloques y formato 12 h / 24 h | Terminal |
| [`reloj_svg`](reloj_svg) | Programa que escribe `reloj.svg` como texto, con manecillas animadas | Gráfico SVG en el navegador |

## Estructura del repositorio

```
.
├── mimath/               librería matemática propia
│   ├── trigonometria.py  PI, reducir_angulo, seno, coseno, grados_a_radianes
│   ├── geometria.py      punto_polar y ángulos de las manecillas
│   └── verificacion.py   autotest de la librería
├── nucleo/               lógica compartida, sin interfaz
│   ├── hora.py           validación HH:MM:SS, conversiones y formatos
│   ├── cronometro.py     estado y operaciones del cronómetro
│   └── alarma.py         estado y operaciones de la alarma
├── reloj_libreria/       versión 1 (ASCII)
├── reloj_terminal/       versión 2 (terminal ANSI)
├── reloj_svg/            versión 3 (SVG, con un reloj.svg de ejemplo)
└── README.md
```

Cada paquete `reloj_*` tiene su propio `README.md`, un `__main__.py` mínimo y módulos por responsabilidad.

## Cómo ejecutar

Requiere Python 3. En Windows se usa el lanzador `py`. Los comandos se ejecutan **desde la raíz del repositorio**:

```
py -3 -m reloj_libreria
py -3 -m reloj_terminal
py -3 -m reloj_svg
```

- No uses `-I` (modo aislado): quita el directorio actual de la ruta de módulos y los paquetes del proyecto no se encontrarían.
- La versión 2 necesita una terminal con ANSI y UTF-8 (Windows Terminal).
- La versión 3 genera `reloj.svg` en la carpeta desde la que se ejecuta; se abre en cualquier navegador.

## Funcionalidades comunes

- Hora inicial pedida con `input()` y validada (`HH:MM:SS`).
- Cronómetro.
- Alarma, incluido el cruce de medianoche.

## Limitaciones conocidas

- Sin acceso al reloj del sistema ni pausas reales: en las versiones 1 y 2 el reloj avanza con el teclado.
- En la versión 3 la hora digital del SVG es estática; las manecillas sí giran solas.
- El profesor indicó que SVG, librería propia y terminal no son válidos como frontend. Estas tres versiones son las alternativas posibles bajo la regla de no importar módulos externos al proyecto.

## Cómo se construyó

Cada versión la construyó un agente con un modelo económico, la revisó un agente con un modelo intermedio y una revisión final independiente probó las tres de punta a punta. Después se reestructuró en paquetes sin cambiar el comportamiento.
