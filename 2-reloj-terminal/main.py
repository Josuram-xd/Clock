# Reloj de terminal: interfaz de texto con esfera analógica ASCII,
# hora digital en bloques y menú de teclas.
# Regla del taller: cero módulos externos. Solo funciones built-in.
# El avance del reloj es manual (teclas), no hay pausas reales.

# ---------------------------------------------------------------------------
# Constantes de presentación
# ---------------------------------------------------------------------------

ESC = "\033"
LIMPIAR_PANTALLA = ESC + "[2J" + ESC + "[H"
RESET = ESC + "[0m"
NEGRITA = ESC + "[1m"
ROJO = ESC + "[31m"
ROJO_PARPADEO = ESC + "[5;1;31m"
VERDE = ESC + "[32m"
AMARILLO = ESC + "[33m"
AZUL = ESC + "[34m"
CIAN = ESC + "[36m"
BLANCO = ESC + "[97m"

ANCHO_CAJA = 60
ANCHO_ESFERA = 25
ALTO_ESFERA = 13
CENTRO_COL = 12
CENTRO_FILA = 6
RADIO_COL = 12.0   # radio horizontal en columnas
RADIO_FILA = 6.0   # radio vertical en filas (la celda es ~2x alta: proporción 2:1)

LIMITE_AVANCE = 604800  # una semana en segundos

SEGUNDOS_DIA = 86400

# ---------------------------------------------------------------------------
# Matemáticas propias (sin módulos externos)
# ---------------------------------------------------------------------------

PI = 3.141592653589793
DOS_PI = 2 * PI


def reducir_angulo(x):
    """Lleva el ángulo en radianes al intervalo [-pi, pi]."""
    while x > PI:
        x -= DOS_PI
    while x < -PI:
        x += DOS_PI
    return x


def seno(x):
    """Seno por serie de Taylor, con reducción de ángulo."""
    x = reducir_angulo(x)
    termino = x
    suma = x
    n = 1
    while abs(termino) > 1e-12:
        termino = -termino * x * x / ((2 * n) * (2 * n + 1))
        suma += termino
        n += 1
    return suma


def coseno(x):
    """Coseno por serie de Taylor, con reducción de ángulo."""
    x = reducir_angulo(x)
    termino = 1.0
    suma = 1.0
    n = 1
    while abs(termino) > 1e-12:
        termino = -termino * x * x / ((2 * n - 1) * (2 * n))
        suma += termino
        n += 1
    return suma


# ---------------------------------------------------------------------------
# Lógica de tiempo
# ---------------------------------------------------------------------------

def a_segundos(horas, minutos, segundos):
    """Convierte hora, minuto y segundo en segundos desde medianoche."""
    return horas * 3600 + minutos * 60 + segundos


def desde_segundos(total):
    """Devuelve (horas, minutos, segundos) a partir de segundos desde medianoche."""
    return total // 3600, (total % 3600) // 60, total % 60


def dos(numero):
    """Escribe un número con al menos dos cifras."""
    if numero >= 10:
        return str(numero)
    return "0" + str(numero)


def formatear_hora(total):
    """Devuelve 'HH:MM:SS' en formato 24 horas."""
    h, m, s = desde_segundos(total)
    return dos(h) + ":" + dos(m) + ":" + dos(s)


def parsear_hora(texto):
    """Convierte 'HH:MM:SS' en segundos desde medianoche. Devuelve None si no es válido."""
    partes = texto.strip().split(":")
    if len(partes) != 3:
        return None
    try:
        horas, minutos, segundos = [int(p) for p in partes]
    except ValueError:
        return None
    if not (0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59):
        return None
    return a_segundos(horas, minutos, segundos)


def leer_entero(texto, minimo, maximo):
    """Convierte texto en entero dentro de [minimo, maximo]. Devuelve None si no es válido."""
    try:
        valor = int(texto)
    except ValueError:
        return None
    if valor < minimo or valor > maximo:
        return None
    return valor


def avanzar_un_segundo(estado):
    """Avanza el reloj un segundo y actualiza cronómetro y alarma."""
    estado["segundos"] = (estado["segundos"] + 1) % SEGUNDOS_DIA
    if estado["cronometro_activo"]:
        estado["cronometro"] += 1
    if estado["alarma"] is not None and estado["segundos"] == estado["alarma"]:
        estado["alarma_sonando"] = True


def avanzar(estado, cantidad):
    """Avanza el reloj la cantidad de segundos indicada."""
    for _ in range(cantidad):
        avanzar_un_segundo(estado)


def crear_estado(segundos_inicio):
    """Crea el diccionario con todo el estado de la aplicación."""
    return {
        "segundos": segundos_inicio,
        "formato_24h": True,
        "cronometro": 0,
        "cronometro_activo": False,
        "alarma": None,
        "alarma_sonando": False,
        "parpadeo": False,
        "mensaje": "",
    }


# ---------------------------------------------------------------------------
# Render: utilidades de texto y caja
# ---------------------------------------------------------------------------

def longitud_visible(texto):
    """Cuenta los caracteres visibles, ignorando las secuencias ANSI."""
    total = 0
    dentro_secuencia = False
    for caracter in texto:
        if caracter == ESC:
            dentro_secuencia = True
        elif dentro_secuencia:
            if caracter == "m":
                dentro_secuencia = False
        else:
            total += 1
    return total


def colorear(texto, color):
    """Envuelve el texto en un color ANSI y lo restablece al final."""
    return color + texto + RESET


def centrar(texto, ancho):
    """Centra un texto (con o sin color) dentro de un ancho dado."""
    relleno = (ancho - longitud_visible(texto)) // 2
    if relleno < 0:
        relleno = 0
    return " " * relleno + texto


def dibujar_caja(lineas, ancho):
    """Dibuja una caja con bordes unicode. Una línea None es un separador."""
    borde = colorear("║", AZUL)
    salida = [colorear("╔" + "═" * ancho + "╗", AZUL)]
    for linea in lineas:
        if linea is None:
            salida.append(colorear("╟" + "─" * ancho + "╢", AZUL))
            continue
        relleno = ancho - longitud_visible(linea)
        salida.append(borde + linea + " " * relleno + borde)
    salida.append(colorear("╚" + "═" * ancho + "╝", AZUL))
    return salida


# ---------------------------------------------------------------------------
# Render: esfera analógica
# ---------------------------------------------------------------------------

def poner_celda(rejilla, angulo, radio, caracter, color):
    """Coloca un carácter en la rejilla a una distancia radial y ángulo dados.

    El ángulo se mide en radianes desde las 12 en sentido horario.
    """
    columna = round(CENTRO_COL + radio * RADIO_COL * seno(angulo))
    fila = round(CENTRO_FILA - radio * RADIO_FILA * coseno(angulo))
    if 0 <= fila < ALTO_ESFERA and 0 <= columna < ANCHO_ESFERA:
        if color:
            rejilla[fila][columna] = colorear(caracter, color)
        else:
            rejilla[fila][columna] = caracter


def trazar_mano(rejilla, angulo, longitud, caracter, color):
    """Dibuja una manecilla desde el centro hasta la longitud indicada (0 a 1)."""
    paso = 0.0
    while paso <= longitud:
        poner_celda(rejilla, angulo, paso, caracter, color)
        paso += 0.02


def marcar_contorno(rejilla):
    """Dibuja el contorno elíptico de la esfera usando la ecuación de la elipse."""
    for fila in range(ALTO_ESFERA):
        for columna in range(ANCHO_ESFERA):
            dx = (columna - CENTRO_COL) / RADIO_COL
            dy = (fila - CENTRO_FILA) / RADIO_FILA
            distancia2 = dx * dx + dy * dy
            if abs(distancia2 - 1.0) < 0.12:
                rejilla[fila][columna] = "."


def dibujar_esfera(segundos):
    """Devuelve las líneas ASCII de la esfera con las tres manecillas."""
    h, m, s = desde_segundos(segundos)
    rejilla = [[" "] * ANCHO_ESFERA for _ in range(ALTO_ESFERA)]
    marcar_contorno(rejilla)
    for marca in range(12):
        poner_celda(rejilla, marca * PI / 6, 0.9, "+", NEGRITA)

    angulo_hora = DOS_PI * ((h % 12) * 60 + m) / 720
    angulo_minuto = DOS_PI * (m * 60 + s) / 3600
    angulo_segundo = DOS_PI * s / 60

    trazar_mano(rejilla, angulo_hora, 0.5, "#", AMARILLO)
    trazar_mano(rejilla, angulo_minuto, 0.8, "=", VERDE)
    trazar_mano(rejilla, angulo_segundo, 0.9, "*", ROJO)
    rejilla[CENTRO_FILA][CENTRO_COL] = colorear("o", NEGRITA)

    return ["".join(fila) for fila in rejilla]


# ---------------------------------------------------------------------------
# Render: dígitos tipo 7 segmentos con caracteres de bloque (3 filas)
# ---------------------------------------------------------------------------

FUENTE_DIGITOS = {
    "0": ["█▀█", "█ █", "█▄█"],
    "1": [" ▄█", "  █", "  ▀"],
    "2": ["▀▀█", "█▀▀", "▀▀▀"],
    "3": ["▀▀█", " ▄█", "▀▀▀"],
    "4": ["█ █", "▀▀█", "  ▀"],
    "5": ["█▀▀", "▀▀█", "▀▀▀"],
    "6": ["█▀▀", "█▀█", "▀▀▀"],
    "7": ["▀▀█", "  █", "  ▀"],
    "8": ["█▀█", "█▀█", "▀▀▀"],
    "9": ["█▀█", "▀▀█", "▀▀▀"],
    ":": [" █ ", "   ", " █ "],
}


def dibujar_digital(texto):
    """Devuelve las 3 filas de un texto como 'HH:MM:SS' en bloques."""
    filas = ["", "", ""]
    for indice, caracter in enumerate(texto):
        glifo = FUENTE_DIGITOS[caracter]
        for fila in range(3):
            if indice > 0:
                filas[fila] += "  "
            filas[fila] += glifo[fila]
    return filas


# ---------------------------------------------------------------------------
# Render: textos de estado y pantalla completa
# ---------------------------------------------------------------------------

def texto_hora(estado):
    """Devuelve (texto de la hora, sufijo AM/PM) según el formato elegido."""
    if estado["formato_24h"]:
        return formatear_hora(estado["segundos"]), ""
    h, m, s = desde_segundos(estado["segundos"])
    sufijo = "AM" if h < 12 else "PM"
    h12 = h % 12
    if h12 == 0:
        h12 = 12
    return dos(h12) + ":" + dos(m) + ":" + dos(s), sufijo


def texto_cronometro(estado):
    """Devuelve el cronómetro en formato MM:SS con su estado."""
    total = estado["cronometro"]
    marcha = "en marcha" if estado["cronometro_activo"] else "parado"
    return dos(total // 60) + ":" + dos(total % 60) + " (" + marcha + ")"


def linea_alarma(estado):
    """Devuelve la línea de alarma; parpadea en rojo cuando está sonando."""
    if estado["alarma_sonando"]:
        if estado["parpadeo"]:
            return colorear("¡ALARMA!", ROJO_PARPADEO)
        return " " * len("¡ALARMA!")
    if estado["alarma"] is None:
        return "Alarma: ninguna"
    return "Alarma: " + formatear_hora(estado["alarma"])


def construir_pantalla(estado):
    """Construye el texto completo de la pantalla (sin limpiar)."""
    lineas = [centrar(colorear("RELOJ DE TERMINAL", NEGRITA + CIAN), ANCHO_CAJA), None]

    for fila in dibujar_esfera(estado["segundos"]):
        lineas.append(centrar(fila, ANCHO_CAJA))
    lineas.append(None)

    texto, sufijo = texto_hora(estado)
    for fila in dibujar_digital(texto):
        lineas.append(centrar(colorear(fila, BLANCO + NEGRITA), ANCHO_CAJA))
    lineas.append(centrar(sufijo, ANCHO_CAJA))
    lineas.append(None)

    formato = "24h" if estado["formato_24h"] else "12h"
    lineas.append(" Formato: " + formato + "   Cronómetro: " + texto_cronometro(estado))
    lineas.append(" " + linea_alarma(estado))

    salida = dibujar_caja(lineas, ANCHO_CAJA)
    salida.append("")
    salida.append(colorear(" [Enter] +1 s    [n] avanzar N s    [c] cronómetro", CIAN))
    salida.append(colorear(" [a] alarma (vacío = quitar)    [f] 12h/24h    [q] salir", CIAN))
    if estado["mensaje"]:
        salida.append(colorear(" " + estado["mensaje"], AMARILLO))
    return "\n".join(salida)


def mostrar(estado):
    """Limpia la pantalla y dibuja el reloj."""
    print(LIMPIAR_PANTALLA + construir_pantalla(estado))


# ---------------------------------------------------------------------------
# Entrada del usuario
# ---------------------------------------------------------------------------

def pedir_hora_inicial():
    """Pide la hora inicial y la repite hasta que sea válida."""
    while True:
        segundos = parsear_hora(input("Hora inicial (HH:MM:SS): "))
        if segundos is not None:
            return segundos
        print("Hora no válida. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def accion_avanzar_segundos(estado):
    """Pide cuántos segundos avanzar y los avanza."""
    cantidad = leer_entero(input("Segundos a avanzar (0-604800): "), 0, LIMITE_AVANCE)
    if cantidad is None:
        estado["mensaje"] = "Cantidad no válida."
        return
    avanzar(estado, cantidad)
    estado["mensaje"] = "Avanzados " + str(cantidad) + " s."


def accion_cronometro(estado):
    """Inicia, para o reinicia el cronómetro."""
    opcion = input("Cronómetro: [i] iniciar  [p] parar  [r] reiniciar: ").strip().lower()
    if opcion == "i":
        estado["cronometro_activo"] = True
        estado["mensaje"] = "Cronómetro en marcha."
    elif opcion == "p":
        estado["cronometro_activo"] = False
        estado["mensaje"] = "Cronómetro parado."
    elif opcion == "r":
        estado["cronometro"] = 0
        estado["cronometro_activo"] = False
        estado["mensaje"] = "Cronómetro reiniciado."
    else:
        estado["mensaje"] = "Opción de cronómetro no válida."


def accion_alarma(estado):
    """Fija la alarma, o la quita si se deja vacía."""
    texto = input("Alarma HH:MM:SS (vacío = quitar): ").strip()
    if texto == "":
        estado["alarma"] = None
        estado["alarma_sonando"] = False
        estado["mensaje"] = "Alarma quitada."
        return
    segundos = parsear_hora(texto)
    if segundos is None:
        estado["mensaje"] = "Hora de alarma no válida."
        return
    estado["alarma"] = segundos
    estado["alarma_sonando"] = segundos == estado["segundos"]
    estado["mensaje"] = "Alarma fijada a " + formatear_hora(segundos) + "."


def procesar_opcion(estado, opcion):
    """Ejecuta la acción de la tecla pulsada. Devuelve False si el usuario sale."""
    if opcion == "":
        avanzar(estado, 1)
    elif opcion == "n":
        accion_avanzar_segundos(estado)
    elif opcion == "c":
        accion_cronometro(estado)
    elif opcion == "a":
        accion_alarma(estado)
    elif opcion == "f":
        estado["formato_24h"] = not estado["formato_24h"]
    elif opcion == "q":
        return False
    else:
        estado["mensaje"] = "Opción no válida: " + opcion
    return True


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    """Bucle principal: pide la hora, dibuja y procesa teclas hasta salir."""
    print(LIMPIAR_PANTALLA + colorear("Bienvenido al reloj de terminal.", CIAN))
    estado = crear_estado(pedir_hora_inicial())
    continuar = True
    while continuar:
        estado["parpadeo"] = not estado["parpadeo"]
        mostrar(estado)
        estado["mensaje"] = ""
        opcion = input("Opción: ").strip().lower()
        continuar = procesar_opcion(estado, opcion)
    print("Hasta luego.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego.")
