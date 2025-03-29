import os
import random
import time
import matplotlib.pyplot as plt
from datetime import datetime

class EnjambreAbejas:
    def __init__(self, num_ciudades):
        self.num_ciudades = num_ciudades
        self.ciudades = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_ciudades)]
        self.mejor_ruta = list(range(num_ciudades))
        random.shuffle(self.mejor_ruta)
        self.mejor_distancia = self.calcular_distancia(self.mejor_ruta)

    def calcular_distancia(self, ruta):
        distancia = 0
        for i in range(len(ruta) - 1):
            x1, y1 = self.ciudades[ruta[i]]
            x2, y2 = self.ciudades[ruta[i + 1]]
            distancia += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distancia

    def optimizar(self, iteraciones=1000):
        for _ in range(iteraciones):
            nueva_ruta = self.mejor_ruta[:]
            random.shuffle(nueva_ruta)
            nueva_distancia = self.calcular_distancia(nueva_ruta)
            if nueva_distancia < self.mejor_distancia:
                self.mejor_ruta, self.mejor_distancia = nueva_ruta, nueva_distancia

def graficar_ruta(ciudades, ruta, carpeta, num_ciudades):
    plt.figure(figsize=(8, 6))
    x_vals, y_vals = [], []

    for i in ruta:
        x_vals.append(ciudades[i][0])
        y_vals.append(ciudades[i][1])

    plt.plot(x_vals, y_vals, 'bo-', label="Ruta óptima")
    plt.scatter(x_vals[0], y_vals[0], color='green', s=100, label="Inicio (Ciudad 0)")
    plt.scatter(x_vals[-1], y_vals[-1], color='red', s=100, label="Fin (Última ciudad)")

    for i, (x, y) in enumerate(ciudades):
        plt.text(x, y, str(i), color='black', fontsize=10, fontweight='bold')

    # **Etiquetas descriptivas para los ejes**
    plt.xlabel("Coordenada X (Posición en el mapa)")
    plt.ylabel("Coordenada Y (Posición en el mapa)")
    plt.title(f"Ruta óptima para {num_ciudades} ciudades")
    plt.legend()
    plt.grid()

    img_path = os.path.join(carpeta, f"ruta_optima_{num_ciudades}.png")
    plt.savefig(img_path)
    plt.close()
    return img_path

def generar_reporte(carpeta, resultados):
    md_path = os.path.join(carpeta, "resultados.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 📌 Informe de Ejecución\n\n")
        f.write(f"📅 **Fecha de ejecución:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 📊 Resultados\n\n")

        for res in resultados:
            f.write(f"### 🔹 {res['num_ciudades']} ciudades\n")
            f.write(f"- 🚀 **Mejor ruta encontrada:** {res['mejor_ruta']}\n")
            f.write(f"- 📏 **Distancia total:** {res['mejor_distancia']:.2f}\n")
            f.write(f"- ⏳ **Tiempo de ejecución:** {res['tiempo']} segundos\n")
            f.write(f"![Ruta óptima para {res['num_ciudades']} ciudades](ruta_optima_{res['num_ciudades']}.png)\n\n")

def ejecutar_experimentos():
    num_ciudades_lista = [20, 50, 100]
    resultados = []

    # Crear carpeta con timestamp único
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    carpeta = os.path.join("resultados", timestamp)
    os.makedirs(carpeta, exist_ok=True)

    for num_ciudades in num_ciudades_lista:
        print(f"\nEjecutando con {num_ciudades} ciudades...")
        inicio = time.perf_counter()

        enjambre = EnjambreAbejas(num_ciudades)
        enjambre.optimizar(iteraciones=1000)

        fin = time.perf_counter()
        tiempo_total = round(fin - inicio, 6)  # Mayor precisión en segundos

        print(f"Mejor ruta encontrada: {enjambre.mejor_ruta}")
        print(f"Distancia total: {enjambre.mejor_distancia:.2f}")
        print(f"Tiempo de ejecución: {tiempo_total} segundos")

        # Generar gráfico
        img_path = graficar_ruta(enjambre.ciudades, enjambre.mejor_ruta, carpeta, num_ciudades)

        # Guardar resultados
        resultados.append({
            "num_ciudades": num_ciudades,
            "mejor_ruta": enjambre.mejor_ruta,
            "mejor_distancia": enjambre.mejor_distancia,
            "tiempo": tiempo_total,
            "img_path": img_path
        })

    # Generar informe en Markdown
    generar_reporte(carpeta, resultados)

if __name__ == "__main__":
    ejecutar_experimentos()
