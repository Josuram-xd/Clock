# Reloj SVG: genera reloj.svg con manecillas animadas, cronometro y alarma.
# Regla del taller: sin imports. El SVG se escribe como texto XML y el
# seno/coseno se calculan con series de Taylor propias.

PI = 3.141592653589793
DOS_PI = 2 * PI

NOMBRE_ARCHIVO = "reloj.svg"

# Geometria del lienzo (viewBox 0 0 400 480)
CENTRO_X = 200
CENTRO_Y = 200
CRONO_CX = 300
CRONO_CY = 412
CRONO_R = 36

# Paleta oscura y acentos
COLOR_FONDO = "#0f172a"
COLOR_BISEL_EXTERNO = "#334155"
COLOR_BISEL_INTERNO = "#1e293b"
COLOR_CARA = "#111827"
COLOR_CARATULA_CRONO = "#0b1222"
COLOR_MARCA_HORA = "#e2e8f0"
COLOR_MARCA_MINUTO = "#475569"
COLOR_NUMERO = "#cbd5e1"
COLOR_MANECILLA = "#e2e8f0"
COLOR_SEGUNDERO = "#f59e0b"
COLOR_ALARMA = "#ef4444"
COLOR_ALARMA_TEXTO = "#f87171"
COLOR_TEXTO_SECUNDARIO = "#94a3b8"

FUENTE_TEXTO = "'Helvetica Neue', Arial, sans-serif"
FUENTE_MONO = "'SF Mono', 'JetBrains Mono', Consolas, monospace"


# ---------------------------------------------------------------------------
# Trigonometria propia
# ---------------------------------------------------------------------------

def reducir_angulo(x):
    """Lleva un angulo en radianes al intervalo [-pi, pi]."""
    while x > PI:
        x -= DOS_PI
    while x < -PI:
        x += DOS_PI
    return x


def seno(x):
    """Seno por serie de Taylor, tras reducir el angulo."""
    x = reducir_angulo(x)
    termino = x
    suma = x
    for n in range(1, 12):
        termino = -termino * x * x / ((2 * n) * (2 * n + 1))
        suma += termino
    return suma


def coseno(x):
    """Coseno usando cos(x) = sen(x + pi/2)."""
    return seno(x + PI / 2)


def punto(cx, cy, radio, grados):
    """Punto a 'radio' del centro (cx, cy), medido en grados desde las 12 en sentido horario."""
    rad = grados * PI / 180
    return cx + radio * seno(rad), cy - radio * coseno(rad)


# ---------------------------------------------------------------------------
# Entrada de datos
# ---------------------------------------------------------------------------

def analizar_hora(texto):
    """Convierte 'HH:MM:SS' en (h, m, s). Devuelve None si el formato no es valido."""
    partes = texto.strip().split(":")
    if len(partes) != 3:
        return None
    for parte in partes:
        if not parte.isdecimal():
            return None
    h, m, s = int(partes[0]), int(partes[1]), int(partes[2])
    if h > 23 or m > 59 or s > 59:
        return None
    return h, m, s


def pedir_hora(mensaje, opcional=False):
    """Pide una hora hasta que sea valida. Si es opcional, Enter devuelve None."""
    while True:
        texto = input(mensaje)
        if opcional and texto.strip() == "":
            return None
        valor = analizar_hora(texto)
        if valor is not None:
            return valor
        print("Formato no valido. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def pedir_cronometro():
    """Devuelve None si no quiere cronometro; si lo quiere, sus segundos de arranque."""
    while True:
        respuesta = input("Quieres cronometro? (s/n): ").strip().lower()
        if respuesta == "n":
            return None
        if respuesta == "s":
            break
        print("Responde s o n.")
    while True:
        texto = input("Duracion de arranque del cronometro en segundos: ").strip()
        if texto.isdecimal():
            return int(texto)
        print("Escribe un numero entero de segundos (0 o mas).")


# ---------------------------------------------------------------------------
# Angulos de las manecillas (grados desde las 12, sentido horario)
# ---------------------------------------------------------------------------

def angulo_segundos(segundos):
    return segundos * 6.0


def angulo_minutos(minutos, segundos):
    return (minutos * 60 + segundos) * 0.1


def angulo_horas(horas, minutos, segundos):
    return (horas % 12) * 30 + minutos * 0.5 + segundos / 120


# ---------------------------------------------------------------------------
# Piezas SVG
# ---------------------------------------------------------------------------

def linea_svg(cx, cy, radio_interno, radio_externo, grados, color, grosor):
    """Segmento radial entre dos radios, en un angulo dado."""
    x1, y1 = punto(cx, cy, radio_interno, grados)
    x2, y2 = punto(cx, cy, radio_externo, grados)
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{grosor}" stroke-linecap="round"/>')


def bisel_svg():
    """Tres circulos concentricos que dan el efecto de bisel de la esfera."""
    return "\n".join([
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="170" fill="{COLOR_BISEL_EXTERNO}"/>',
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="164" fill="{COLOR_BISEL_INTERNO}"/>',
        f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="158" fill="{COLOR_CARA}"/>',
    ])


def marcas_svg():
    """60 marcas; las de cada hora (cada 5) son mas gruesas y largas."""
    piezas = []
    for i in range(60):
        grados = i * 6
        if i % 5 == 0:
            piezas.append(linea_svg(CENTRO_X, CENTRO_Y, 136, 152, grados, COLOR_MARCA_HORA, 4))
        else:
            piezas.append(linea_svg(CENTRO_X, CENTRO_Y, 146, 152, grados, COLOR_MARCA_MINUTO, 1.5))
    return "\n".join(piezas)


def numeros_svg():
    """Numeros del 1 al 12 colocados con las funciones trigonometricas propias."""
    piezas = []
    for hora in range(1, 13):
        x, y = punto(CENTRO_X, CENTRO_Y, 118, hora * 30)
        piezas.append(
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="22" fill="{COLOR_NUMERO}">{hora}</text>'
        )
    return "\n".join(piezas)


def marca_alarma_svg(alarma):
    """Marca roja sobre las horas en el angulo de la alarma."""
    ah, am, as_ = alarma
    return linea_svg(CENTRO_X, CENTRO_Y, 136, 152, angulo_horas(ah, am, as_), COLOR_ALARMA, 5)


def segundos_hasta_alarma(hora, alarma):
    """Segundos que faltan (1 a 86400) desde la hora inicial hasta la alarma."""
    h, m, s = hora
    ah, am, as_ = alarma
    faltan = ((ah - h) * 3600 + (am - m) * 60 + (as_ - s)) % 86400
    return faltan if faltan > 0 else 86400


def aviso_alarma_svg(hora, alarma):
    """Texto '¡ALARMA!' oculto que aparece y parpadea cuando la animacion llega a la alarma."""
    inicio = segundos_hasta_alarma(hora, alarma)
    return "\n".join([
        f'<text x="{CENTRO_X}" y="275" text-anchor="middle" font-size="26" font-weight="bold" '
        f'fill="{COLOR_ALARMA}" visibility="hidden">&#161;ALARMA!',
        f'  <set attributeName="visibility" to="visible" begin="{inicio}s"/>',
        f'  <animate attributeName="opacity" values="1;0;1" dur="1s" begin="{inicio}s" '
        f'repeatCount="indefinite"/>',
        "</text>",
    ])


def manecilla(cx, cy, longitud_arriba, longitud_abajo, grosor, color, angulo, duracion):
    """Manecilla en un grupo que gira alrededor de (cx, cy).

    La animacion parte del angulo actual (from) y da una vuelta completa
    en 'duracion' segundos, en bucle infinito.
    """
    inicio = f"{angulo:.3f} {cx} {cy}"
    fin = f"{angulo + 360:.3f} {cx} {cy}"
    return "\n".join([
        "<g>",
        f'  <line x1="{cx}" y1="{cy + longitud_abajo}" x2="{cx}" y2="{cy - longitud_arriba}" '
        f'stroke="{color}" stroke-width="{grosor}" stroke-linecap="round"/>',
        f'  <animateTransform attributeName="transform" type="rotate" '
        f'from="{inicio}" to="{fin}" dur="{duracion}s" repeatCount="indefinite"/>',
        "</g>",
    ])


def cronometro_svg(segundos):
    """Mini-dial de cronometro con su etiqueta; la manecilla gira cada 60 s."""
    piezas = [
        f'<circle cx="{CRONO_CX}" cy="{CRONO_CY}" r="{CRONO_R}" fill="{COLOR_CARATULA_CRONO}" '
        f'stroke="{COLOR_BISEL_EXTERNO}" stroke-width="2"/>'
    ]
    for i in range(12):
        piezas.append(linea_svg(CRONO_CX, CRONO_CY, 28, 33, i * 30, COLOR_MARCA_MINUTO, 1.5))
    piezas.append(manecilla(CRONO_CX, CRONO_CY, 30, 5, 1.5, COLOR_SEGUNDERO,
                            angulo_segundos(segundos % 60), 60))
    piezas.append(f'<circle cx="{CRONO_CX}" cy="{CRONO_CY}" r="2.5" fill="{COLOR_SEGUNDERO}"/>')
    minutos, seg = segundos // 60, segundos % 60
    piezas.append(
        f'<text x="{CRONO_CX}" y="470" text-anchor="middle" font-size="12" '
        f'letter-spacing="2" fill="{COLOR_TEXTO_SECUNDARIO}">CRONO {minutos}:{seg:02d}</text>'
    )
    return "\n".join(piezas)


def construir_svg(hora, alarma, segundos_crono):
    """Ensambla el documento SVG completo como texto."""
    h, m, s = hora
    # Con cronometro, la hora digital se desplaza a la izquierda para dejar sitio al mini-dial.
    x_digital = 120 if segundos_crono is not None else CENTRO_X

    piezas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480" width="400" height="480" '
        f'font-family="{FUENTE_TEXTO}">',
        "  <title>Reloj SVG</title>",
        f'<rect x="0" y="0" width="400" height="480" fill="{COLOR_FONDO}"/>',
        bisel_svg(),
        marcas_svg(),
        numeros_svg(),
    ]
    if alarma is not None:
        piezas.append(marca_alarma_svg(alarma))

    # Las manecillas parten de la hora dada y dan vueltas de 12 h, 1 h y 60 s.
    piezas.append(manecilla(CENTRO_X, CENTRO_Y, 90, 14, 7, COLOR_MANECILLA,
                            angulo_horas(h, m, s), 43200))
    piezas.append(manecilla(CENTRO_X, CENTRO_Y, 136, 16, 4.5, COLOR_MANECILLA,
                            angulo_minutos(m, s), 3600))
    piezas.append(manecilla(CENTRO_X, CENTRO_Y, 150, 36, 1.8, COLOR_SEGUNDERO,
                            angulo_segundos(s), 60))
    piezas.append(f'<circle cx="{CENTRO_X}" cy="{CENTRO_Y}" r="6" fill="{COLOR_SEGUNDERO}"/>')
    if alarma is not None:
        piezas.append(aviso_alarma_svg(hora, alarma))

    piezas.append(
        f'<text x="{x_digital}" y="418" text-anchor="middle" font-family="{FUENTE_MONO}" '
        f'font-size="30" fill="{COLOR_MANECILLA}">{h:02d}:{m:02d}:{s:02d}</text>'
    )
    if alarma is not None:
        ah, am, as_ = alarma
        piezas.append(
            f'<text x="{x_digital}" y="448" text-anchor="middle" font-size="14" '
            f'fill="{COLOR_ALARMA_TEXTO}">Alarma {ah:02d}:{am:02d}:{as_:02d}</text>'
        )
    if segundos_crono is not None:
        piezas.append(cronometro_svg(segundos_crono))

    piezas.append("</svg>")
    return "\n".join(piezas) + "\n"


def escribir_archivo(ruta, contenido):
    """Guarda el contenido en UTF-8 en la ruta indicada."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    print("=== Generador de reloj SVG ===")
    hora = pedir_hora("Hora inicial HH:MM:SS: ")
    alarma = pedir_hora("Hora de alarma HH:MM:SS (Enter para omitir): ", opcional=True)
    segundos_crono = pedir_cronometro()

    contenido = construir_svg(hora, alarma, segundos_crono)
    escribir_archivo(NOMBRE_ARCHIVO, contenido)

    if alarma is not None:
        print(f"La alarma sonara en el SVG dentro de {segundos_hasta_alarma(hora, alarma)} s de animacion.")
    print(f"Archivo generado: {NOMBRE_ARCHIVO} (en el directorio desde el que ejecutaste el programa).")
    print("Abrelo en tu navegador (doble clic, o arrastralo a una pestana abierta).")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada terminada. No se genero el archivo.")
