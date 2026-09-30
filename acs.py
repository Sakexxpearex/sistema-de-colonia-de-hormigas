"""ACS (Ant Colony System) aplicado al problema del vendedor viajero.

Uso:
    python acs.py <instancia> <hormigas> <iteraciones> <alfa> <beta> <q0> <semilla> <salida.csv>

Ejemplo:
    python acs.py datos/berlin52.txt 25 1000 0.1 2.0 0.9 1 resultados/resultados.csv
"""

import csv
import random
import sys
import time

import operadores

RHO = 0.1  # tasa de la actualizacion local de feromonas

if len(sys.argv) != 9:
    print(__doc__)
    sys.exit(1)

instancia = sys.argv[1]
hormigas = int(sys.argv[2])
iteraciones = int(sys.argv[3])
alfa = float(sys.argv[4])
beta = float(sys.argv[5])
q0 = float(sys.argv[6])
semilla = int(sys.argv[7])
salida = sys.argv[8]

# inicializar
random.seed(semilla)
ciudades = operadores.leer_ciudades(instancia)
n = len(ciudades)
distancias = operadores.calcular_distancias(ciudades)
visibilidad = operadores.calcular_visibilidad(distancias, beta)
greedy = operadores.ruta_vecino_mas_cercano(distancias)
tau0 = 1.0 / (n * operadores.costo_ruta(greedy, distancias))
feromonas = operadores.crear_feromonas(n, tau0)

mejor_ruta = None
mejor_costo = float("inf")
inicio = time.time()

archivo = open(salida, "w", newline="")
escritor = csv.writer(archivo)
escritor.writerow(["instancia", "semilla", "hormigas", "iteraciones", "alfa",
                   "beta", "q0", "iteracion", "costo", "tiempo", "ruta"])

for iteracion in range(1, iteraciones + 1):

    rutas = operadores.construir_soluciones(hormigas, feromonas, visibilidad, q0, RHO, tau0)

    costos = operadores.evaluar_soluciones(rutas, distancias)

    mejor_ruta, mejor_costo = operadores.actualizar_mejor_solucion(rutas, costos,
                                                                  mejor_ruta, mejor_costo)

    operadores.actualizar_feromonas(feromonas, mejor_ruta, mejor_costo, alfa)

    escritor.writerow([instancia, semilla, hormigas, iteraciones, alfa, beta, q0,
                       iteracion, mejor_costo, round(time.time() - inicio, 3),
                       " ".join(str(c) for c in mejor_ruta)])

archivo.close()

print("mejor costo:", mejor_costo)
print("ruta:", " ".join(str(c) for c in mejor_ruta))
print("resultados en:", salida)
