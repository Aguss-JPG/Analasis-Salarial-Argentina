import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
IMG_DIR = BASE_DIR / "Graficos"

dataframe = pd.read_csv(
    r"C:\Users\ferra\OneDrive\Documentos\Data Projects\Analisis media salarial 2019-2023\Data\w_median_privado_mensual_por_clae2.csv"
)
print (dataframe.head())

#   Excluir salario total mediano "clae 999" 
# "clae 999" = conjunto de todos los sectores industriales
dataframe_total = dataframe[dataframe["clae2"]== 999]
dataframe = dataframe[dataframe["clae2"] != 999]

#Cambiar nombre de columna media salarial:
dataframe = dataframe.rename(columns={
    "w_median": "salario_median" 
})

# eliminar salarios inválidos
dataframe = dataframe[dataframe["salario_median"] > 0]
print("Salario minimo")
print(dataframe["salario_median"].min())

dataframe.to_csv(
    "Data/salarios_clae_clean.csv",
    index=False
)
