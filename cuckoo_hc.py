# archivo: cuckoo_main.py
import os
import time
import numpy as np
import pandas as pd
from scipy.special import gamma
from tsp_utils import fitness, graficar_ruta_grafo_espacial
from matrices import matrices
from hill_climbing_main import hill_climbing  # importar HC para intensificación final

# Función Levy Flight para paso de mutación
def levy_flight(Lambda):
    sigma = (gamma(1 + Lambda) * np.sin(np.pi * Lambda / 2) /
             (gamma((1 + Lambda) / 2) * Lambda * 2 ** ((Lambda - 1) / 2))) ** (1 / Lambda)
    u = np.random.randn() * sigma
    v = np.random.randn()
    step = u / abs(v) ** (1 / Lambda)
    return step

# Mutación basada en Levy: k swaps en la ruta
def levy_mutation(route, step, n_cities):
    k = max(1, int(abs(step)))
    new_route = route.copy()
    for _ in range(k):
        i, j = np.random.randint(0, n_cities, size=2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

# Algoritmo Cuckoo Search con intensificación final (Hill Climbing)
def cuckoo_search_tsp(matriz_distancia, n_nests, max_iter, pa, alpha, Lambda):
    n_cities = len(matriz_distancia)
    nests = [np.random.permutation(n_cities) for _ in range(n_nests)]
    best_nest = nests[0].copy()
    best_fitness = fitness(best_nest, matriz_distancia)

    for t in range(1, max_iter + 1):
        new_nests = []
        for nest in nests:
            step = levy_flight(Lambda) * alpha
            new = levy_mutation(nest, step, n_cities)
            new_nests.append(new)

        for i, new in enumerate(new_nests):
            new_fit = fitness(new, matriz_distancia)
            old_fit = fitness(nests[i], matriz_distancia)
            if new_fit < old_fit:
                nests[i] = new
                if new_fit < best_fitness:
                    best_nest = new.copy()
                    best_fitness = new_fit

        # Abandonar y elitismo
        abandon_idx = np.random.rand(n_nests) < pa
        for i in range(n_nests):
            if abandon_idx[i]:
                nests[i] = np.random.permutation(n_cities)
        fits = [fitness(n, matriz_distancia) for n in nests]
        worst = int(np.argmax(fits))
        nests[worst] = best_nest.copy()

    # Intensificación final con Hill Climbing
    local_nest, local_fitness = hill_climbing(matriz_distancia)
    if local_fitness < best_fitness:
        best_nest, best_fitness = local_nest, local_fitness

    return best_nest, best_fitness

# Parámetros optimizados por tamaño
best_params = {
    10: dict(n_nests=50, max_iter=500, pa=0.6, alpha=1.5, Lambda=1.5),
    20: dict(n_nests=50, max_iter=200, pa=0.6, alpha=1.0, Lambda=2.0),
    50: dict(n_nests=25, max_iter=500, pa=0.25, alpha=2.0, Lambda=1.5),
    100: dict(n_nests=50, max_iter=500, pa=0.6, alpha=1.0, Lambda=1.5),
    200: dict(n_nests=50, max_iter=200, pa=0.6, alpha=1.5, Lambda=1.5),
    500: dict(n_nests=50, max_iter=200, pa=0.25, alpha=0.5, Lambda=1.0)
}

# Ejecución dinámica
tamaños = sorted(best_params.keys())
output_file = "resultados_cuckoo_hc.txt"
resultados = []
with open(output_file, "w", encoding="utf-8") as file:
    for n in tamaños:
        params = best_params[n]
        tsp = matrices[n]
        start = time.time()
        ruta, dist_total = cuckoo_search_tsp(
            tsp,
            params['n_nests'], params['max_iter'], params['pa'],
            params['alpha'], params['Lambda']
        )
        duracion = time.time() - start
        encabezado = (f"Cuckoo+HC | nests={params['n_nests']}, iter={params['max_iter']}, "
                     f"pa={params['pa']}, alpha={params['alpha']}, lambda={params['Lambda']}")
        linea = (f"[Cuckoo+HC] n={n} | {encabezado} | Tiempo: {duracion:.4f}s | Distancia: {dist_total}")
        print(linea)
        file.write(linea + "\n")
        resultados.append({"n": n, "Ruta": ruta, "Distancia": dist_total, "Tiempo (s)": duracion, **params})

# Mostrar y guardar resultados finales
import pandas as pd

df = pd.DataFrame(resultados)
mejores = df.loc[df.groupby("n")["Distancia"].idxmin()]
print("\n📊 Mejor resultado por cada tamaño:")
print(mejores)
with open(output_file, "a", encoding="utf-8") as file:
    file.write("\n📊 Mejor resultado por cada tamaño:\n" + mejores.to_string(index=False))

# Graficar rutas óptimas
os.makedirs("mejores_rutas_cuckoo_hc", exist_ok=True)
for _, r in mejores.iterrows():
    graficar_ruta_grafo_espacial(list(r['Ruta']), f"Cuckoo+HC n={int(r['n'])}", int(r['n']),
                                 int(r['Distancia']), save_path=os.path.join("mejores_rutas_cuckoo", f"cuckoo_hc_n{int(r['n'])}.png"),
                                 seed=int(r['n'] + 2000))
