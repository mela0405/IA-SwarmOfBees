import numpy as np
import random
import matplotlib.pyplot as plt

# Definimos la clase para el problema del agente viajero
def calcular_distancia(ruta, matriz_distancias):
    """Calcula la distancia total de una ruta dada."""
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += matriz_distancias[ruta[i]][ruta[i + 1]]
    distancia_total += matriz_distancias[ruta[-1]][ruta[0]]  # Retorno al punto de inicio
    return distancia_total

class EnjambreAbejas:
    def __init__(self, num_ciudades, num_abejas, num_exploradoras, iteraciones):
        self.num_ciudades = num_ciudades
        self.num_abejas = num_abejas
        self.num_exploradoras = num_exploradoras
        self.iteraciones = iteraciones
        self.matriz_distancias = self.generar_matriz_distancias()
        self.mejor_ruta = None
        self.mejor_distancia = float('inf')
    
    def generar_matriz_distancias(self):
        """Genera una matriz de distancias aleatorias entre ciudades."""
        matriz = np.random.randint(10, 100, size=(self.num_ciudades, self.num_ciudades))
        np.fill_diagonal(matriz, 0)
        return (matriz + matriz.T) // 2  # Asegurar simetría
    
    def generar_ruta_inicial(self):
        """Genera una ruta inicial aleatoria."""
        ruta = list(range(self.num_ciudades))
        random.shuffle(ruta)
        return ruta
    
    def buscar_solucion(self):
        """Implementa el algoritmo de enjambre de abejas para el TSP."""
        for _ in range(self.iteraciones):
            abejas = [self.generar_ruta_inicial() for _ in range(self.num_abejas)]
            distancias = [calcular_distancia(ruta, self.matriz_distancias) for ruta in abejas]
            
            # Seleccionamos las mejores rutas
            mejores_indices = np.argsort(distancias)[:self.num_exploradoras]
            mejores_rutas = [abejas[i] for i in mejores_indices]
            
            for ruta in mejores_rutas:
                nueva_ruta = self.variar_ruta(ruta)
                nueva_distancia = calcular_distancia(nueva_ruta, self.matriz_distancias)
                
                if nueva_distancia < calcular_distancia(ruta, self.matriz_distancias):
                    ruta[:] = nueva_ruta
            
            mejor_iteracion = min(zip(abejas, distancias), key=lambda x: x[1])
            if mejor_iteracion[1] < self.mejor_distancia:
                self.mejor_ruta, self.mejor_distancia = mejor_iteracion
    
    def variar_ruta(self, ruta):
        """Realiza un intercambio aleatorio de dos ciudades para explorar nuevas soluciones."""
        nueva_ruta = ruta[:]
        i, j = random.sample(range(len(ruta)), 2)
        nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
        return nueva_ruta
    
    def mostrar_resultados(self):
        """Muestra la mejor ruta encontrada y su distancia total."""
        print(f"Mejor ruta encontrada: {self.mejor_ruta}")
        print(f"Distancia total: {self.mejor_distancia}")

# Pruebas con 20, 50 y 100 ciudades
for num_ciudades in [20, 50, 100]:
    print(f"\nEjecutando con {num_ciudades} ciudades...")
    enjambre = EnjambreAbejas(num_ciudades=num_ciudades, num_abejas=30, num_exploradoras=10, iteraciones=100)
    enjambre.buscar_solucion()
    enjambre.mostrar_resultados()
