"""Genera los graficos a partir de un archivo de resultados.

Uso:
    python graficar.py resultados/experimentos.csv
"""

import csv
import sys

import matplotlib.pyplot as plt

import operadores

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)

with open(sys.argv[1]) as f:
    filas = list(csv.DictReader(f))

# Grafico 1: costo de la mejor solucion por iteracion, promediando las semillas.
corridas = {}
for fila in filas:
    clave = "h=%s a=%s b=%s q0=%s" % (fila["hormigas"], fila["alfa"],
                                      fila["beta"], fila["q0"])
    corridas.setdefault(clave, {}).setdefault(int(fila["iteracion"]), []).append(float(fila["costo"]))

plt.figure(figsize=(8, 5))
for clave in sorted(corridas):
    iteraciones = sorted(corridas[clave])
    promedios = [sum(corridas[clave][i]) / len(corridas[clave][i]) for i in iteraciones]
    plt.plot(iteraciones, promedios, label=clave)
plt.xlabel("iteracion")
plt.ylabel("costo de la mejor solucion (promedio de semillas)")
plt.title("Convergencia de ACS")
plt.legend(fontsize=7)
plt.grid(alpha=0.3)
plt.savefig("graficos/convergencia.png")

# Grafico 2: la mejor ruta de todo el archivo.
mejor = min(filas, key=lambda f: float(f["costo"]))
ciudades = operadores.leer_ciudades(mejor["instancia"])
ruta = [int(c) for c in mejor["ruta"].split()]
x = [ciudades[c][0] for c in ruta] + [ciudades[ruta[0]][0]]
y = [ciudades[c][1] for c in ruta] + [ciudades[ruta[0]][1]]

plt.figure(figsize=(7, 6))
plt.plot(x, y, "-o", markersize=4)
plt.title("Mejor ruta encontrada (costo %.0f)" % float(mejor["costo"]))
plt.xlabel("x")
plt.ylabel("y")
plt.grid(alpha=0.3)
plt.savefig("graficos/mejor_ruta.png")

print("guardados: graficos/convergencia.png y graficos/mejor_ruta.png")
