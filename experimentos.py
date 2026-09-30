"""Corre varias configuraciones de ACS y junta todo en un solo CSV.

Uso:
    python experimentos.py
"""

import os
import subprocess
import sys

INSTANCIA = "datos/berlin52.txt"
SALIDA = "resultados/experimentos.csv"
TEMPORAL = "resultados/_una_corrida.csv"
SEMILLAS = [1, 2, 3, 4, 5]

# hormigas, iteraciones, alfa, beta, q0
CONFIGURACIONES = [
    (5,  500, 0.1, 2.0, 0.9),    # variando la cantidad de hormigas
    (10, 500, 0.1, 2.0, 0.9),
    (25, 500, 0.1, 2.0, 0.9),
    (50, 500, 0.1, 2.0, 0.9),
    (10, 500, 0.1, 1.0, 0.9),    # variando beta
    (10, 500, 0.1, 5.0, 0.9),
    (10, 500, 0.1, 2.0, 0.0),    # variando q0
    (10, 500, 0.1, 2.0, 0.5),
    (10, 500, 0.1, 2.0, 0.98),
]

lineas = []

for i, config in enumerate(CONFIGURACIONES, 1):
    for semilla in SEMILLAS:
        print("corrida %d/%d  %s  semilla %d" % (i, len(CONFIGURACIONES), config, semilla))
        subprocess.run([sys.executable, "acs.py", INSTANCIA] +
                       [str(v) for v in config] + [str(semilla), TEMPORAL],
                       check=True, stdout=subprocess.DEVNULL)
        with open(TEMPORAL) as f:
            cabecera = f.readline()
            lineas.extend(f.readlines())  # se saltea la cabecera repetida

with open(SALIDA, "w", newline="") as f:
    f.write(cabecera)
    f.writelines(lineas)

os.remove(TEMPORAL)
print("resultados en:", SALIDA)
