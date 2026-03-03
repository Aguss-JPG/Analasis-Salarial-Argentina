
import pandas as pd
import numpy as np

salarios = pd.read_csv(
    r"C:\Users\ferra\OneDrive\Documentos\Data Projects\Analisis media salarial 2019-2023\data\salarios_limpios.csv",
    parse_dates=["fecha"]
)

ipc = pd.read_csv(
    r"C:\Users\ferra\Downloads\serie_ipc_aperturas.csv",
    sep=";",
    encoding="latin1"
)

# Datos que vamos a usar
ipc = ipc[
    (ipc["Descripcion_aperturas"] == "Nivel general") &
    (ipc["Region"] == "Pampeana")
]

# Crear columna fecha
ipc["fecha"] = pd.to_datetime(
    ipc["Periodo"].astype(str),
    format="%Y%m"
)

ipc = ipc[
    (ipc["fecha"] >= "2019-01-01") &
    (ipc["fecha"] <= "2023-11-01")
]

ipc = ipc[["fecha", "Indice_IPC"]]

print(ipc.head())

# Convertir valor a tipo float
ipc["Indice_IPC"] = (
    ipc["Indice_IPC"]
    .str.replace(",", ".", regex=False)
    .astype(float)
)

# Calcular base
ipc_base = ipc[ipc["fecha"] == "2019-01-01"]["Indice_IPC"].iloc[0]

# Crear IPC normalizado
ipc["ipc_normalizado"] = ipc["Indice_IPC"] / ipc_base * 100

# Grafico de control
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(ipc["fecha"], ipc["ipc_normalizado"])
plt.title("IPC normalizado (base 100)")
plt.xlabel("Fecha")
plt.ylabel("Índice")
plt.grid(True)
plt.show()

# Objetivo: medir cómo evolucionó el poder adquisitivo de los salarios,
#  descontando inflación.


salarios[["fecha", "salario_median"]]

# Asegurarse que los datasets esten en Datetime
ipc["fecha"] = pd.to_datetime(ipc["fecha"])
salarios["fecha"] = pd.to_datetime(salarios["fecha"])

print(ipc.dtypes)
print(salarios.dtypes)

# Unir salarios con IPC
dataframe = salarios.merge(
    ipc[["fecha", "ipc_normalizado"]],
    on="fecha",
    how="left"
)
print(dataframe.isna().sum())


# Calcular salario real
dataframe["salario_real"] = (
    dataframe["salario_median"] / dataframe["ipc_normalizado"] * 100
)

# Visualizacion
plt.figure(figsize=(10,5))
plt.plot(dataframe["fecha"], dataframe["salario_median"], label="Salario nominal")
plt.plot(dataframe["fecha"], dataframe["salario_real"], label="Salario real")
plt.legend()
plt.title("Evolución del salario nominal vs salario real")
plt.xlabel("Fecha")
plt.ylabel("Pesos")
plt.grid(True)
plt.savefig("nominal_vs_real.")
plt.show()

"""
Si bien el salario nominal muestra una tendencia creciente durante todo el período analizado,
el salario real ajustado por inflación se mantiene relativamente estable, 
evidenciando que los aumentos salariales no implicaron una mejora sostenida del poder adquisitivo.
"""

salarios = salarios.merge(
    ipc[["fecha", "ipc_normalizado"]],
    on="fecha",
    how="left"
)
print(salarios[["fecha", "ipc_normalizado"]].head())

# Ranking por salario ajustado a inflacion
# Responde a ¿Que sectores terminaron el periodo con mayor poder adquisitivo

# Calcular salario real
salarios["salario_real"] = (
    salarios["salario_median"] / salarios["ipc_normalizado"] * 100
)
# Dataframe ranking
ranking_real = (
    salarios
    .groupby("clae2", as_index=False)
    ["salario_real"]
    .mean()
)

# Ordenar y crear ranking
ranking_real = ranking_real.sort_values(
    "salario_real",
    ascending=False
)

ranking_real["ranking"] = range(1, len(ranking_real) + 1)

# Percentil
ranking_real["percentil"] = (
    ranking_real["salario_real"]
    .rank(pct=True) * 100
)
print("Top claes ")
print(ranking_real.head(10))

print(ranking_real.tail(5))

plt.figure(figsize=(10,5))
plt.bar(
    ranking_real["clae2"].astype(str),
    ranking_real["salario_real"]
)
plt.xticks(rotation=90)
plt.title("Ranking de salario real promedio por actividad (CLAE)")
plt.tight_layout()
#plt.savefig("ranking_salario_real.png")
#plt.show()


# 1. Ranking por salario real (ajustado por inflación)
ranking = (
    salarios
    .groupby("clae2", as_index=False)["salario_normalizado"]
    .mean()
    .sort_values("salario_normalizado", ascending=False)
    .head(10)
)

# 2. Gráfico de barras horizontal
plt.figure(figsize=(10, 6))
plt.barh(
    ranking["clae2"].astype(str),
    ranking["salario_normalizado"]
)

plt.xlabel("Salario real promedio (ajustado por IPC)")
plt.ylabel("Sector económico (CLAE)")
plt.title("Top 10 sectores por salario real promedio")

plt.gca().invert_yaxis()  # el mayor arriba
plt.tight_layout()
plt.show()


"""
Aunque el sector CLAE 64 lideraba el ranking de salarios nominales,
 al ajustar por inflación se observa una caída relativa en su posición.
Esto indica que los aumentos salariales del sector no compensaron completamente la inflación acumulada del período,
provocando una mayor pérdida de poder adquisitivo en comparación con otros sectores que, si bien tenían salarios 
nominales menores, lograron sostener mejor su salario real.
"""

"""
Conclusión:
El ranking por salario real revela diferencias estructurales entre sectores
 que no son visibles al analizar únicamente salarios nominales, evidenciando cuáles sectores 
 lograron proteger mejor el poder adquisitivo de sus trabajadores frente a la inflación.
"""
salarios.to_csv(
    "salarios_reales.csv",
    index=False
)
