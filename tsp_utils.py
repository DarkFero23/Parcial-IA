# archivo: tsp_utils.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Funciones generales para TSP

def generar_tsp(n, seed=None):
    """
    Genera una matriz de distancias aleatoria de tamaño n×n.
    Distancias entre 10 y 499, con ceros en la diagonal.
    """
    if seed is not None:
        np.random.seed(seed)
    mat = np.random.randint(10, 500, size=(n, n))
    np.fill_diagonal(mat, 0)
    return mat


def fitness(sol, matriz):
    """
    Calcula la distancia total de la ruta `sol` sobre `matriz`.
    Incluye retorno al punto inicial.
    """
    distancia = 0
    for i in range(len(sol) - 1):
        distancia += matriz[sol[i], sol[i+1]]
    distancia += matriz[sol[-1], sol[0]]
    return distancia


def get_neighbors(sol):
    """
    Genera todos los vecinos de `sol` mediante swap de dos posiciones.
    """
    vecinos = []
    n = len(sol)
    for i in range(n-1):
        for j in range(i+1, n):
            vecino = sol.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos


def graficar_ruta_grafo_espacial(ruta, algoritmo, n, distancia, save_path=None, seed=None):
    """
    Dibuja la ruta sobre un grafo espacial con posiciones aleatorias fijas.
    """
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed(42)
    # Generar posiciones únicas por nodo
    coords = np.random.rand(n, 2)
    fig, ax = plt.subplots(figsize=(8, 6))
    # Dibujar aristas
    for i in range(len(ruta)):
        u = ruta[i]
        v = ruta[(i+1) % len(ruta)]
        xs = [coords[u,0], coords[v,0]]
        ys = [coords[u,1], coords[v,1]]
        ax.plot(xs, ys, '-', color='gray', lw=1, alpha=0.7)
    # Dibujar nodos y etiquetas
    ax.scatter(coords[:,0], coords[:,1], s=50, color='skyblue', edgecolor='black', zorder=3)
    for idx, (x, y) in enumerate(coords):
        ax.text(x, y+0.01, str(idx), fontsize=8, ha='center')
    ax.set_title(f"{algoritmo} | n={n} | Distancia={distancia}")
    ax.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()


def graficar_comparaciones(df, tipo="Distancia", logscale=False):
    """
    Grafica comparativa de `tipo` (e.g., Distancia o Tiempo) para cada algoritmo.
    Anota valores y permite escala logarítmica.
    """
    # Asegurar orden por n
    df_sorted = df.sort_values(by='n')
    fig, ax = plt.subplots(figsize=(10,6))
    # Agrupar por algoritmo y trazar
    for algo, grupo in df_sorted.groupby('Algoritmo'):
        ax.plot(grupo['n'], grupo[tipo], marker='o', label=algo)
        # Etiquetar cada punto
        for x, y in zip(grupo['n'], grupo[tipo]):
            ax.text(x, y, f"{int(y)}", fontsize=7, ha='center', va='bottom')
    ax.set_xlabel('Número de ciudades (n)')
    ax.set_ylabel(tipo)
    if logscale:
        ax.set_yscale('log')
    ax.set_title(f'Comparación de {tipo.lower()} por algoritmo')
    ax.legend(title='Algoritmo')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
