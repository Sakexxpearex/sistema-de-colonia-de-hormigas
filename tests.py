"""Pruebas de los operadores principales."""

import random
import unittest

import operadores

# Cuadrado de lado 10: la ruta optima recorre el borde y mide 40.
CIUDADES = [(0, 0), (10, 0), (10, 10), (0, 10)]


class PruebasOperadores(unittest.TestCase):

    def setUp(self):
        self.distancias = operadores.calcular_distancias(CIUDADES)

    def test_lectura_de_datos(self):
        ciudades = operadores.leer_ciudades("datos/berlin52.txt")
        self.assertEqual(len(ciudades), 52)
        self.assertEqual(ciudades[0], (565.0, 575.0))
        self.assertEqual(ciudades[-1], (1740.0, 245.0))

    def test_matriz_de_distancias(self):
        self.assertEqual(self.distancias[0][1], 10)
        self.assertEqual(self.distancias[0][2], 14)  # sqrt(200) redondeado
        self.assertEqual(self.distancias[0][0], 0)
        self.assertEqual(self.distancias[1][3], self.distancias[3][1])

    def test_costo_de_ruta(self):
        self.assertEqual(operadores.costo_ruta([0, 1, 2, 3], self.distancias), 40)
        self.assertEqual(operadores.costo_ruta([3, 2, 1, 0], self.distancias), 40)

    def test_ruta_valida(self):
        random.seed(1)
        visibilidad = operadores.calcular_visibilidad(self.distancias, 2.0)
        feromonas = operadores.crear_feromonas(4, 0.5)
        ruta = operadores.construir_ruta(feromonas, visibilidad, 0.9, 0.1, 0.5)
        self.assertEqual(sorted(ruta), [0, 1, 2, 3])  # cada ciudad una sola vez

    def test_feromonas_iniciales(self):
        feromonas = operadores.crear_feromonas(4, 0.5)
        for fila in feromonas:
            self.assertEqual(fila, [0.5, 0.5, 0.5, 0.5])

    def test_actualizacion_local_baja_la_feromona(self):
        feromonas = operadores.crear_feromonas(4, 1.0)
        operadores.actualizar_feromona_local(feromonas, 0, 1, 0.1, 0.0)
        self.assertAlmostEqual(feromonas[0][1], 0.9)
        self.assertAlmostEqual(feromonas[1][0], 0.9)

    def test_actualizacion_global_premia_la_mejor_ruta(self):
        feromonas = operadores.crear_feromonas(4, 0.001)
        operadores.actualizar_feromonas(feromonas, [0, 1, 2, 3], 40, 0.1)
        # las aristas de la mejor ruta suben, las que no estan quedan igual
        self.assertGreater(feromonas[0][1], feromonas[0][2])
        self.assertEqual(feromonas[0][2], 0.001)

    def test_la_mejor_solucion_nunca_empeora(self):
        rutas = [[0, 1, 2, 3], [0, 2, 1, 3]]
        costos = [40, 60]
        ruta, costo = operadores.actualizar_mejor_solucion(rutas, costos, None, float("inf"))
        self.assertEqual(costo, 40)
        ruta, costo = operadores.actualizar_mejor_solucion([[0, 2, 1, 3]], [60], ruta, costo)
        self.assertEqual(costo, 40)

    def test_vecino_mas_cercano(self):
        ruta = operadores.ruta_vecino_mas_cercano(self.distancias)
        self.assertEqual(sorted(ruta), [0, 1, 2, 3])
        self.assertEqual(operadores.costo_ruta(ruta, self.distancias), 40)


if __name__ == "__main__":
    unittest.main()
