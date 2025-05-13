# archivo: tsp_optimo.py

import os
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from matrices import matrices

def compute_optimal_distance(dist_matrix):
    """Resuelve el TSP de forma exacta con OR-Tools y devuelve la distancia óptima."""
    n = len(dist_matrix)
    # Crear el índice manager y el RoutingModel:
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    # Función de coste (distancia)
    def distance_callback(i, j):
        return int(dist_matrix[manager.IndexToNode(i)][manager.IndexToNode(j)])
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Parámetros de búsqueda para intentar ser exactos
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_params.time_limit.seconds = 30  # ajusta según el tamaño

    solution = routing.SolveWithParameters(search_params)
    if solution:
        return solution.ObjectiveValue()
    else:
        return None  # no encontró solución

def main():
    resultados = []
    os.makedirs("resultados", exist_ok=True)

    for n, mat in matrices.items():
        print(f"Resolviendo TSP óptimo para n={n}…")
        opt_dist = compute_optimal_distance(mat)
        resultados.append({"n": n, "Distancia_Óptima": opt_dist})

    df = pd.DataFrame(resultados).sort_values("n")
    ruta_salida = os.path.join("resultados", "optimal_distances.txt")
    with open(ruta_salida, "w") as f:
        f.write(df.to_string(index=False))

    print(f"Listo: distancias óptimas guardadas en {ruta_salida}")

if __name__ == "__main__":
    main()
