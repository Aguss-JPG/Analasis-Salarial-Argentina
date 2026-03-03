import pandas as pd
import numpy as np

dataframe_ipc = pd.read_csv(
    r"C:\Users\ferra\Downloads\serie_ipc_aperturas.csv",
    encoding="latin1",
    sep=";"
)
(dataframe_ipc.columns)
(dataframe_ipc.head())

# Nos quedamos solo con Nivel General
ipc = dataframe_ipc[
    dataframe_ipc["Descripcion_aperturas"] == "Nivel general"
].copy()

# Convertimos Periodo a fecha
dataframe_ipc["Periodo"] = pd.to_datetime(dataframe_ipc["Periodo"])
ipc["Periodo"] = pd.to_datetime(ipc["Periodo"].astype(str), format="%Y%m")

# Ordenamos
ipc = ipc.sort_values("Periodo")

# Recorte IPC (para usar en este proyecto)
ipc = ipc[
    (ipc["Periodo"] >= "2019-01-01") &
    (ipc["Periodo"] <= "2023-12-01")
]

ipc = ipc[["Periodo", "Indice_IPC"]]
ipc = ipc.rename(columns={"Periodo": "fecha"})

# Visualizar la evolución de la inflación (IPC) entre 2019 y 2023

import matplotlib.pyplot as plt

plt.figure()
plt.plot(ipc["fecha"], ipc["Indice_IPC"])
plt.title("Evolución del IPC (2019–2023)")
plt.xlabel("Fecha")
plt.ylabel("Índice de Precios (Base 2016 = 100)")
#plt.show()

print("Columnas dataframe_ipc:")
print(dataframe_ipc.columns)

print("\nColumnas ipc:")
print(ipc.columns)
print("Columnas dataframe_ipc:")
print(dataframe_ipc.columns)

df = dataframe_ipc.merge(
    ipc[["fecha", "Indice_IPC"]],
    left_on="Periodo",
    right_on="fecha",
    how="left"
)

ipc_base = ipc.loc[ipc["fecha"] == "2019-01-01", "Indice_IPC"].iloc[0]
