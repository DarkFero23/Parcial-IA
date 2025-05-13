# archivo: hill_climbing_main.py
import os
import time
import numpy as np
import pandas as pd
from tsp_utils import generar_tsp, fitness, get_neighbors, graficar_ruta_grafo_espacial
from matrices import matrices

def hill_climbing(tsp):
    current_solution = list(range(len(tsp)))
    np.random.shuffle(current_solution)
    while True:
        neighbors = get_neighbors(current_solution)
        best_neighbor = min(neighbors, key=lambda x: fitness(x, tsp))
        if fitness(best_neighbor, tsp) >= fitness(current_solution, tsp):
            break
        current_solution = best_neighbor
    return current_solution, fitness(current_solution, tsp)

if __name__ == "__main__":
    # Configuración
    tamaños = [10, 20, 50, 100, 200, 500]
    resultados = []

    with open("resultados_hill_climbing.txt", "w", encoding="utf-8") as file:
        for n in tamaños:
            tsp = matrices[n]
            start = time.time()
            ruta, dist_total = hill_climbing(tsp)
            duracion = time.time() - start

            linea = f"[Hill Climbing] n={n} | Tiempo: {duracion:.4f}s | Distancia: {dist_total}"
            print(linea)
            file.write(linea + "\n")

            resultados.append({
                "Algoritmo": "Hill Climbing",
                "n": n,
                "Ruta": ruta,
                "Distancia": dist_total,
                "Tiempo (s)": duracion,
                "Temp Inicial": "-",
                "Cooling Rate": "-",
                "T_min": "-"
            })

    # Crear DataFrame
    df_hc = pd.DataFrame(resultados)

    mejores = df_hc.sort_values(by="Distancia").head()
    mejores_por_n = df_hc.loc[df_hc.groupby("n")["Distancia"].idxmin()]

    print("\nMejores rutas encontradas (menor distancia):")
    print(mejores)

    print("\nMejor resultado por cada tamaño:")
    print(mejores_por_n[["n", "Distancia", "Tiempo (s)"]])

    with open("resultados_hill_climbing.txt", "a", encoding="utf-8") as file:
        file.write("\nMejores rutas encontradas (menor distancia):\n")
        file.write(mejores.to_string(index=False) + "\n")
        file.write("\nMejor resultado por cada tamaño:\n")
        file.write(mejores_por_n[["n", "Distancia", "Tiempo (s)"]].to_string(index=False) + "\n")

    # Crear carpeta para guardar gráficos
    carpeta = "mejores_rutas_hc"
    os.makedirs(carpeta, exist_ok=True)

    # Graficar las mejores rutas con una semilla distinta por n
    for _, fila in mejores_por_n.iterrows():
        nombre_archivo = os.path.join(carpeta, f"hc_n{fila['n']}.png")
        graficar_ruta_grafo_espacial(
            fila["Ruta"],
            fila["Algoritmo"],
            fila["n"],
            fila["Distancia"],
            save_path=nombre_archivo,
            seed=int(fila["n"] + 3000)  # Semilla única para diferenciación visual
        )
