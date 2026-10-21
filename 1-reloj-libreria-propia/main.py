"""
Reloj analógico en ASCII con una librería trigonométrica propia.

Secciones:
  1. LIBRERÍA mimath: PI, reducción de ángulos, seno y coseno por Taylor,
     punto polar y autotest.
  2. FRONTEND: lienzo ASCII de la esfera y manecillas dibujadas con DDA.
  3. LÓGICA DEL RELOJ: hora, avance, cronómetro y alarma.
  4. MENÚ: interacción con el usuario.

Regla del taller: no se usan módulos externos; solo funciones built-in.
"""

# ============================================================
# 1. LIBRERÍA mimath
# ============================================================

PI = 3.141592653589793
TAU = 2 * PI
NUM_TERMINOS = 12  # Términos de la serie de Taylor (mínimo 10)
TOLERANCIA = 1e-6


def reducir_angulo(angulo):
    """Reduce un ángulo en radianes al intervalo [-PI, PI]."""
    vueltas = round(angulo / TAU)
    reducido = angulo - vueltas * TAU
    if reducido > PI:
        reducido -= TAU
    elif reducido < -PI:
        reducido += TAU
    return reducido


def seno(angulo):
    """Seno por serie de Taylor: x - x^3/3! + x^5/5! - ..."""
    x = reducir_angulo(angulo)
    termino = x
    suma = x
    for n in range(1, NUM_TERMINOS):
        termino = -termino * x * x / ((2 * n) * (2 * n + 1))
        suma += termino
    return suma


def coseno(angulo):
    """Coseno por serie de Taylor: 1 - x^2/2! + x^4/4! - ..."""
    x = reducir_angulo(angulo)
    termino = 1.0
    suma = 1.0
    for n in range(1, NUM_TERMINOS):
        termino = -termino * x * x / ((2 * n - 1) * (2 * n))
        suma += termino
    return suma


def grados_a_radianes(grados):
    """Convierte grados a radianes."""
    return grados * PI / 180


def angulo_manecilla(valor, maximo):
    """Ángulo en grados de una manecilla: 0 en las 12 y sentido horario."""
    return valor / maximo * 360


def punto_polar(cx, cy, radio, angulo_grados):
    """
    Devuelve (x, y) a 'radio' del centro (cx, cy).
    El ángulo se mide desde las 12 en sentido horario y el eje Y apunta hacia arriba.
    """
    radianes = grados_a_radianes(angulo_grados)
    x = cx + radio * seno(radianes)
    y = cy + radio * coseno(radianes)
    return x, y


# Valores conocidos: (grados, seno esperado, coseno esperado)
VALORES_CONOCIDOS = [
    (0, 0.0, 1.0),
    (30, 0.5, 0.8660254037844386),
    (45, 0.7071067811865476, 0.7071067811865476),
    (60, 0.8660254037844386, 0.5),
    (90, 1.0, 0.0),
    (180, 0.0, -1.0),
    (270, -1.0, 0.0),
    (360, 0.0, 1.0),
]


def comparar(nombre, obtenido, esperado):
    """Imprime OK o FALLÓ para un valor y devuelve True si pasa la prueba."""
    pasa = abs(obtenido - esperado) <= TOLERANCIA
    estado = "OK" if pasa else "FALLÓ"
    print(f"  {nombre}: obtenido={obtenido:.9f} esperado={esperado:.9f} -> {estado}")
    return pasa


def verificar_libreria():
    """Autotest: compara seno y coseno con valores conocidos."""
    print("AUTOTEST de la librería mimath (tolerancia 1e-6):")
    resultados = []
    for grados, seno_esperado, coseno_esperado in VALORES_CONOCIDOS:
        radianes = grados_a_radianes(grados)
        resultados.append(comparar(f"seno({grados} gr)", seno(radianes), seno_esperado))
        resultados.append(comparar(f"coseno({grados} gr)", coseno(radianes), coseno_esperado))
    if all(resultados):
        print("Resultado global: OK")
    else:
        print("Resultado global: FALLÓ")


# ============================================================
# 2. FRONTEND: esfera analógica en ASCII
# ============================================================

ANCHO = 41
ALTO = 21
CENTRO_COL = 20
CENTRO_FILA = 10
FACTOR_ASPECTO = 2  # Una celda es el doble de alta que de ancha: el eje X se escala x2
RADIO_ANILLO = 10
RADIO_NUMEROS = 9
LARGO_HORA = 5
LARGO_MINUTO = 7
LARGO_SEGUNDO = 8


def crear_lienzo():
    """Crea una matriz de espacios ANCHO x ALTO."""
    return [[" "] * ANCHO for _ in range(ALTO)]


def poner_caracter(lienzo, columna, fila, caracter):
    """Escribe un carácter si la posición cae dentro del lienzo."""
    if 0 <= columna < ANCHO and 0 <= fila < ALTO:
        lienzo[fila][columna] = caracter


def a_celda(x, y):
    """Convierte coordenadas ideales (Y hacia arriba) en (columna, fila)."""
    columna = CENTRO_COL + round(x * FACTOR_ASPECTO)
    fila = CENTRO_FILA - round(y)
    return columna, fila


def punto_en_celda(radio, angulo_grados):
    """Celda del lienzo a 'radio' del centro, con el ángulo dado."""
    x, y = punto_polar(0, 0, radio, angulo_grados)
    return a_celda(x, y)


def linea_dda(col0, fila0, col1, fila1):
    """Celdas de la línea entre dos puntos, con el algoritmo DDA."""
    delta_col = col1 - col0
    delta_fila = fila1 - fila0
    pasos = max(abs(delta_col), abs(delta_fila))
    if pasos == 0:
        return [(col0, fila0)]
    celdas = []
    for paso in range(pasos + 1):
        columna = round(col0 + delta_col * paso / pasos)
        fila = round(fila0 + delta_fila * paso / pasos)
        celdas.append((columna, fila))
    return celdas


def dibujar_marcas(lienzo):
    """Marcas en el anillo: '.' para minutos y '+' para cada hora."""
    for minuto in range(60):
        columna, fila = punto_en_celda(RADIO_ANILLO, angulo_manecilla(minuto, 60))
        caracter = "+" if minuto % 5 == 0 else "."
        poner_caracter(lienzo, columna, fila, caracter)


def dibujar_numeros(lienzo):
    """Escribe los números 1 a 12 alrededor de la esfera."""
    for hora in range(1, 13):
        columna, fila = punto_en_celda(RADIO_NUMEROS, angulo_manecilla(hora, 12))
        texto = str(hora)
        inicio = columna - len(texto) // 2
        for indice, caracter in enumerate(texto):
            poner_caracter(lienzo, inicio + indice, fila, caracter)


def dibujar_manecilla(lienzo, angulo_grados, largo, caracter):
    """Dibuja una manecilla desde el centro hasta su punta."""
    columna_fin, fila_fin = punto_en_celda(largo, angulo_grados)
    for columna, fila in linea_dda(CENTRO_COL, CENTRO_FILA, columna_fin, fila_fin):
        poner_caracter(lienzo, columna, fila, caracter)


def calcular_angulos(total_segundos):
    """Ángulos (hora, minuto, segundo) en grados para los segundos del día."""
    horas = (total_segundos // 3600) % 12
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    angulo_hora = angulo_manecilla(horas + minutos / 60, 12)
    angulo_minuto = angulo_manecilla(minutos + segundos / 60, 60)
    angulo_segundo = angulo_manecilla(segundos, 60)
    return angulo_hora, angulo_minuto, angulo_segundo


def construir_esfera(total_segundos):
    """Compone el lienzo completo: marcas, números y manecillas."""
    lienzo = crear_lienzo()
    dibujar_marcas(lienzo)
    dibujar_numeros(lienzo)
    angulo_hora, angulo_minuto, angulo_segundo = calcular_angulos(total_segundos)
    dibujar_manecilla(lienzo, angulo_segundo, LARGO_SEGUNDO, "s")
    dibujar_manecilla(lienzo, angulo_minuto, LARGO_MINUTO, "M")
    dibujar_manecilla(lienzo, angulo_hora, LARGO_HORA, "H")
    poner_caracter(lienzo, CENTRO_COL, CENTRO_FILA, "O")
    return lienzo


def mostrar_esfera(total_segundos):
    """Imprime la esfera en la consola."""
    for fila in construir_esfera(total_segundos):
        print("".join(fila).rstrip())


# ============================================================
# 3. LÓGICA DEL RELOJ
# ============================================================

SEGUNDOS_DIA = 86400


def formatear_hora(total):
    """Segundos del día -> 'HH:MM:SS'."""
    horas = total // 3600
    minutos = (total % 3600) // 60
    segundos = total % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def formatear_cronometro(segundos):
    """Segundos transcurridos -> 'MM:SS'."""
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


def convertir_hora(texto):
    """Segundos del día para 'HH:MM:SS', o None si el texto no es válido."""
    partes = texto.strip().split(":")
    if len(partes) != 3:
        return None
    for parte in partes:
        if len(parte) != 2 or not parte.isdecimal():
            return None
    horas, minutos, segundos = (int(parte) for parte in partes)
    if horas > 23 or minutos > 59 or segundos > 59:
        return None
    return horas * 3600 + minutos * 60 + segundos


def crear_estado(segundos_inicio):
    """Estado del reloj: hora, cronómetro y alarma."""
    return {
        "segundos": segundos_inicio,
        "cronometro": 0,
        "cronometro_activo": False,
        "alarma": None,
    }


def avanzar_un_segundo(estado):
    """Avanza 1 s. Devuelve True si la alarma suena en ese segundo."""
    estado["segundos"] = (estado["segundos"] + 1) % SEGUNDOS_DIA
    if estado["cronometro_activo"]:
        estado["cronometro"] += 1
    if estado["alarma"] is not None and estado["alarma"] == estado["segundos"]:
        estado["alarma"] = None
        return True
    return False


def avanzar(estado, cantidad):
    """Avanza el reloj 'cantidad' segundos y avisa si la alarma suena."""
    hora_alarma = estado["alarma"]
    suena = False
    for _ in range(cantidad):
        if avanzar_un_segundo(estado):
            suena = True
    if suena:
        print(f"¡ALARMA! Son las {formatear_hora(hora_alarma)}")


def configurar_alarma(estado):
    """Pide la hora de la alarma. Vacío cancela la alarma actual."""
    texto = input("Hora de la alarma (HH:MM:SS, vacío para cancelar): ").strip()
    if texto == "":
        estado["alarma"] = None
        print("Alarma cancelada.")
        return
    segundos = convertir_hora(texto)
    if segundos is None:
        print("Hora inválida. Use el formato HH:MM:SS.")
        return
    estado["alarma"] = segundos
    print(f"Alarma fijada a las {formatear_hora(segundos)}.")


def menu_cronometro(estado):
    """Iniciar/reanudar, parar o reiniciar el cronómetro."""
    print("  [1] iniciar/reanudar  [2] parar  [3] reiniciar (00:00)  [0] volver")
    opcion = input("Cronómetro> ").strip()
    if opcion == "1":
        estado["cronometro_activo"] = True
    elif opcion == "2":
        estado["cronometro_activo"] = False
    elif opcion == "3":
        estado["cronometro"] = 0
        estado["cronometro_activo"] = False
    elif opcion != "0":
        print("Opción de cronómetro inválida.")


# ============================================================
# 4. MENÚ E INTERACCIÓN
# ============================================================

MENU = """
[1] Avanzar 1 segundo
[2] Avanzar N segundos
[3] Cronómetro
[4] Fijar alarma
[5] Autotest de la librería
[0] Salir"""


def pedir_hora_inicial():
    """Pide la hora hasta que sea válida."""
    while True:
        segundos = convertir_hora(input("Hora inicial (HH:MM:SS): "))
        if segundos is not None:
            return segundos
        print("Hora inválida. Use HH:MM:SS con HH de 00 a 23 y MM/SS de 00 a 59.")


def pedir_cantidad_segundos():
    """Pide un entero positivo de segundos."""
    while True:
        texto = input("Segundos a avanzar: ").strip()
        if texto.isdecimal() and int(texto) > 0:
            return int(texto)
        print("Escriba un número entero mayor que 0.")


def dibujar_pantalla(estado):
    """Redibuja la esfera y los datos digitales."""
    print("=" * ANCHO)
    mostrar_esfera(estado["segundos"])
    print("=" * ANCHO)
    print(f"Hora digital: {formatear_hora(estado['segundos'])}")
    situacion = "en marcha" if estado["cronometro_activo"] else "parado"
    print(f"Cronómetro: {formatear_cronometro(estado['cronometro'])} ({situacion})")
    alarma = "ninguna" if estado["alarma"] is None else formatear_hora(estado["alarma"])
    print(f"Alarma: {alarma}")


def ejecutar_opcion(opcion, estado):
    """Ejecuta la acción elegida en el menú."""
    if opcion == "1":
        avanzar(estado, 1)
    elif opcion == "2":
        avanzar(estado, pedir_cantidad_segundos())
    elif opcion == "3":
        menu_cronometro(estado)
    elif opcion == "4":
        configurar_alarma(estado)
    elif opcion == "5":
        verificar_libreria()
    else:
        print("Opción inválida.")


def main():
    """Bucle principal: dibuja, lee la opción y ejecuta la acción."""
    try:
        estado = crear_estado(pedir_hora_inicial())
        while True:
            dibujar_pantalla(estado)
            print(MENU)
            opcion = input("Opción: ").strip()
            if opcion == "0":
                break
            ejecutar_opcion(opcion, estado)
        print("Reloj apagado. ¡Hasta luego!")
    except EOFError:
        print("\nNo hay más entrada. Saliendo.")


if __name__ == "__main__":
    main()
