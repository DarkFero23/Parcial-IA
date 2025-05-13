# archivo: compare_algorithms.py
import re
import pandas as pd
from tsp_utils import graficar_comparaciones

# Función robusta para leer resultados y crear DataFrame
def leer_resultados(path, algoritmo_label):
    data = []
    pattern_n = re.compile(r"n=(\d+)")
    pattern_time = re.compile(r"Tiempo:\s*([0-9]*\.?[0-9]+)")
    pattern_dist = re.compile(r"Distancia:\s*(\d+)")
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '[' not in line or 'Distancia' not in line:
                continue
            # Extraer valores con regex
            m_n = pattern_n.search(line)
            m_t = pattern_time.search(line)
            m_d = pattern_dist.search(line)
            if not (m_n and m_t and m_d):
                continue
            n = int(m_n.group(1))
            tiempo = float(m_t.group(1))
            distancia = int(m_d.group(1))
            data.append({
                'Algoritmo': algoritmo_label,
                'n': n,
                'Tiempo (s)': tiempo,
                'Distancia': distancia
            })
    return pd.DataFrame(data)

# Leer resultados de cada archivo (asegúrate de los nombres exactos)
df_cuckoo = leer_resultados('resultados_cuckoo.txt', 'Cuckoo puro')
df_hybrid = leer_resultados('resultados_cuckoo_hc.txt', 'Cuckoo+HC')

# Concatenar y ordenar
if df_cuckoo.empty and df_hybrid.empty :
    raise RuntimeError("No se encontraron líneas de resultados en los archivos.")
df_all = pd.concat([df_cuckoo,  df_hybrid], ignore_index=True)

df_all = df_all.sort_values(['Algoritmo','n']).reset_index(drop=True)

# Graficar comparaciones de Distancia y Tiempo
graficar_comparaciones(df_all, tipo='Distancia', logscale=False)
graficar_comparaciones(df_all, tipo='Tiempo (s)', logscale=True)
