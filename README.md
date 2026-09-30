# Pre Proyecto 2 - Sistema de Colonia de Hormigas (ACS) para el TSP

Implementacion de Ant Colony System aplicada al problema del vendedor viajero,
usando la instancia **berlin52** (optimo conocido: **7542**).

Solo usa la libreria estandar de Python. `matplotlib` hace falta unicamente para los graficos.

## Archivos

```
acs.py            algoritmo principal (que hace el algoritmo)
operadores.py     biblioteca de operadores (como se hace cada operacion)
tests.py          pruebas de los operadores
experimentos.py   corre varias configuraciones y junta los resultados
graficar.py       graficos a partir de un CSV de resultados
datos/            instancia berlin52
resultados/       archivos CSV generados
graficos/         imagenes generadas
```

## Como ejecutar

```
python acs.py <instancia> <hormigas> <iteraciones> <alfa> <beta> <q0> <semilla> <salida.csv>
```

Ejemplo (esta corrida encuentra el optimo 7542):

```
python acs.py datos/berlin52.txt 25 1000 0.1 2.0 0.9 1 resultados/resultados.csv
```

Pruebas:

```
python -m unittest tests
```

Experimentos y graficos:

```
python experimentos.py
python graficar.py resultados/experimentos.csv
```

## Parametros

| Parametro | Que es | Valor tipico |
|---|---|---|
| `hormigas` | soluciones construidas por iteracion | 10 - 25 |
| `iteraciones` | repeticiones del ciclo principal | 500 - 1000 |
| `alfa` | evaporacion en la actualizacion global de feromonas | 0.1 |
| `beta` | peso de la distancia frente a la feromona | 2.0 |
| `q0` | probabilidad de elegir la mejor opcion en vez de sortear | 0.9 |
| `semilla` | semilla del generador aleatorio (para repetir corridas) | cualquiera |

La tasa de la actualizacion local de feromonas queda fija en 0.1 (`RHO` en `acs.py`),
que es el valor habitual en ACS.

## Salida

El CSV tiene una fila por iteracion con: instancia, semilla, parametros usados,
numero de iteracion, costo de la mejor solucion hasta ese momento, tiempo transcurrido
y la ruta.

## Como funciona

`acs.py` tiene el ciclo del algoritmo y `operadores.py` los detalles:

```
inicializar feromonas (tau0 = 1 / (n * costo del vecino mas cercano))
repetir:
    construir soluciones   cada hormiga arma una ruta; con probabilidad q0 elige
                           la ciudad que maximiza feromona * (1/distancia)^beta,
                           si no sortea proporcionalmente. Al pasar por una arista
                           le baja un poco la feromona (actualizacion local) para
                           que las demas hormigas exploren otros caminos.
    evaluar soluciones     largo de cada ruta
    actualizar mejor solucion
    actualizar feromonas   solo la mejor ruta global deposita feromona
```

## Experimentos

45 corridas: 9 configuraciones x 5 semillas, partiendo de
`hormigas=10, iteraciones=500, alfa=0.1, beta=2.0, q0=0.9` y cambiando un parametro por vez.

| hormigas | beta | q0 | mejor | promedio | tiempo (s) |
|---|---|---|---|---|---|
| 5 | 2.0 | 0.9 | 7542 | 7679.8 | 0.6 |
| 10 | 1.0 | 0.9 | 7619 | 7798.6 | 1.2 |
| 10 | 2.0 | 0.0 | 9781 | 10056.4 | 1.0 |
| 10 | 2.0 | 0.5 | 8025 | 8149.6 | 1.1 |
| 10 | 2.0 | 0.9 | 7657 | 7752.0 | 1.2 |
| 10 | 2.0 | 0.98 | 7547 | 7664.8 | 1.2 |
| 10 | 5.0 | 0.9 | 7542 | 7674.4 | 1.2 |
| 25 | 2.0 | 0.9 | 7542 | 7664.6 | 2.9 |
| 50 | 2.0 | 0.9 | 7657 | 7713.6 | 6.1 |

**Numero de hormigas.** Subir de 10 a 25 mejora un poco el resultado, pero con 50 ya no
mejora y el tiempo se multiplica por 5. Con pocas hormigas (5) el resultado tambien es
bueno porque en ACS la busqueda la guia la mejor ruta global, no la cantidad de hormigas.

**Numero de iteraciones.** En el grafico de convergencia se ve que casi toda la mejora
ocurre en las primeras 100 iteraciones. Despues la curva es casi plana, aunque de vez en
cuando aparece una mejora suelta. Para berlin52 alcanza con 500 iteraciones; 1000 ayudan
a encontrar el optimo exacto.

**beta.** Con `beta=1` la distancia pesa poco y el resultado empeora. Con `beta=2` o `beta=5`
los resultados son parecidos, asi que el algoritmo no es muy sensible en ese rango.

**q0.** Es el parametro mas influyente. Con `q0=0` (siempre sortear) el costo queda un 33%
por encima del optimo; con `q0=0.9` o `0.98` se llega cerca del optimo. Sin explotacion el
algoritmo explora demasiado y no aprovecha la feromona acumulada.

**Semillas.** Con los mismos parametros los resultados varian entre 7542 y ~7900 segun la
semilla (1-5% de diferencia). Por eso cada configuracion se corre con varias semillas y se
compara el promedio, no una corrida suelta.

**Calidad vs tiempo.** El tiempo crece de forma lineal con hormigas x iteraciones, pero la
calidad se estanca. Pasar de 10 a 50 hormigas cuesta 5 veces mas tiempo y no mejora nada.
Conviene invertir en mas iteraciones o en repetir con varias semillas antes que en mas hormigas.

## Transferencia a un problema mas complejo (PFSP)

En el PFSP una solucion es un orden de trabajos en las maquinas, y el costo es el makespan.

1. **Que se mantiene de `acs.py`:** todo el ciclo principal. Inicializar, construir soluciones,
   evaluar, actualizar feromonas y actualizar la mejor solucion son independientes del problema.
   Tambien se mantienen los parametros (hormigas, iteraciones, alfa, beta, q0) y el CSV de salida.

2. **Que cambia en `operadores.py`:** la lectura del problema (tiempos de proceso en vez de
   coordenadas), `calcular_distancias` y `calcular_visibilidad` (la heuristica deja de ser 1/distancia
   y pasa a ser algo como el tiempo de proceso del trabajo), `costo_ruta` (se reemplaza por el
   calculo del makespan) y `ruta_vecino_mas_cercano` (se usa una heuristica constructiva tipo NEH).

3. **Que informacion nueva hay que representar:** la matriz de tiempos de proceso trabajo x maquina,
   y la feromona deja de ser "arista i-j" para pasar a ser "trabajo j en la posicion i" de la secuencia.

4. **Que cambia la evaluacion:** en vez de sumar distancias hay que simular la linea de produccion,
   acumulando por maquina el maximo entre el fin del trabajo anterior en esa maquina y el fin del
   mismo trabajo en la maquina previa.

En resumen: el algoritmo general (`acs.py`) se reutiliza casi entero y lo que se reescribe son
los operadores especificos del problema.
