from tsp_utils import generar_tsp
import pandas as pd
import os

# Generar las matrices
tamaños = [10, 20, 50, 100, 200, 500]
semilla_base = 5000
matrices = {n: generar_tsp(n, seed=n + semilla_base) for n in tamaños}

# Nombre del archivo de salida
output_path = "matrices_distancias.txt"

with open(output_path, "w", encoding="utf-8") as f:
    for n, mat in matrices.items():
        f.write(f"Matriz de distancias {n}×{n}\n")
        # Creamos un DataFrame para que los números queden alineados
        df = pd.DataFrame(mat)
        # to_string con índices y cabeceras opcionales
        f.write(df.to_string(index=False, header=False))
        f.write("\n\n")  

print(f"✅ Tablas volcadas en '{output_path}'")
