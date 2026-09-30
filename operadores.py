"""Operadores usados por el algoritmo ACS para el TSP."""

import math
import random


def leer_ciudades(archivo):
    """Lee las coordenadas del archivo de instancia (formato: id x y)."""
    ciudades = []
    with open(archivo) as f:
        for linea in f:
            partes = linea.split()
            if len(partes) == 3:
                try:
                    ciudades.append((float(partes[1]), float(partes[2])))
                except ValueError:
                    continue  # linea de cabecera, se ignora
    return ciudades


def calcular_distancias(ciudades):
    """Matriz de distancias euclidianas redondeadas (EUC_2D de TSPLIB)."""
    n = len(ciudades)
    distancias = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = ciudades[i][0] - ciudades[j][0]
            dy = ciudades[i][1] - ciudades[j][1]
            d = round(math.sqrt(dx * dx + dy * dy))
            distancias[i][j] = d
            distancias[j][i] = d
    return distancias


def calcular_visibilidad(distancias, beta):
    """Matriz (1/distancia)^beta, para no recalcularla en cada paso."""
    n = len(distancias)
    visibilidad = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                visibilidad[i][j] = (1.0 / distancias[i][j]) ** beta
    return visibilidad


def costo_ruta(ruta, distancias):
    """Largo total de la ruta, incluyendo el regreso a la ciudad inicial."""
    total = 0.0
    for i in range(len(ruta)):
        total += distancias[ruta[i - 1]][ruta[i]]
    return total


def ruta_vecino_mas_cercano(distancias):
    """Ruta greedy: desde cada ciudad se salta a la mas cercana sin visitar."""
    ruta = [0]
    faltan = set(range(1, len(distancias)))
    while faltan:
        actual = ruta[-1]
        siguiente = min(faltan, key=lambda c: distancias[actual][c])
        ruta.append(siguiente)
        faltan.remove(siguiente)
    return ruta


def crear_feromonas(n, valor_inicial):
    """Matriz de feromonas con el mismo valor en todas las aristas."""
    return [[valor_inicial] * n for _ in range(n)]


def elegir_ciudad(actual, candidatas, feromonas, visibilidad, q0):
    """Regla de transicion de ACS: explotacion con probabilidad q0, si no ruleta."""
    pesos = [feromonas[actual][c] * visibilidad[actual][c] for c in candidatas]

    if random.random() < q0:
        mejor = max(range(len(candidatas)), key=lambda k: pesos[k])
        return candidatas[mejor]

    corte = random.random() * sum(pesos)
    acumulado = 0.0
    for i, peso in enumerate(pesos):
        acumulado += peso
        if acumulado >= corte:
            return candidatas[i]
    return candidatas[-1]


def actualizar_feromona_local(feromonas, i, j, rho, tau0):
    """Evapora un poco la arista recien usada para que otras hormigas la eviten."""
    nuevo = (1 - rho) * feromonas[i][j] + rho * tau0
    feromonas[i][j] = nuevo
    feromonas[j][i] = nuevo


def construir_ruta(feromonas, visibilidad, q0, rho, tau0):
    """Una hormiga arma una ruta completa aplicando la actualizacion local."""
    n = len(feromonas)
    actual = random.randrange(n)
    ruta = [actual]
    candidatas = [c for c in range(n) if c != actual]

    while candidatas:
        siguiente = elegir_ciudad(actual, candidatas, feromonas, visibilidad, q0)
        candidatas.remove(siguiente)
        actualizar_feromona_local(feromonas, actual, siguiente, rho, tau0)
        ruta.append(siguiente)
        actual = siguiente

    actualizar_feromona_local(feromonas, actual, ruta[0], rho, tau0)
    return ruta


def construir_soluciones(hormigas, feromonas, visibilidad, q0, rho, tau0):
    """Todas las hormigas de la iteracion construyen su ruta."""
    return [construir_ruta(feromonas, visibilidad, q0, rho, tau0)
            for _ in range(hormigas)]


def evaluar_soluciones(rutas, distancias):
    """Costo de cada ruta."""
    return [costo_ruta(ruta, distancias) for ruta in rutas]


def actualizar_feromonas(feromonas, mejor_ruta, mejor_costo, alfa):
    """Actualizacion global: solo la mejor ruta encontrada deposita feromona."""
    deposito = alfa / mejor_costo
    for i in range(len(mejor_ruta)):
        a = mejor_ruta[i - 1]
        b = mejor_ruta[i]
        nuevo = (1 - alfa) * feromonas[a][b] + deposito
        feromonas[a][b] = nuevo
        feromonas[b][a] = nuevo


def actualizar_mejor_solucion(rutas, costos, mejor_ruta, mejor_costo):
    """Se queda con la mejor ruta entre la actual y las de esta iteracion."""
    i = min(range(len(costos)), key=lambda k: costos[k])
    if mejor_ruta is None or costos[i] < mejor_costo:
        return list(rutas[i]), costos[i]
    return mejor_ruta, mejor_costo
