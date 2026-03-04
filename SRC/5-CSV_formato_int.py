
import pandas as pd
import numpy as np

# Leer el CSV correcto
dataframe = pd.read_csv(
    r"C:\Users\ferra\OneDrive\Documentos\Data Projects\Analisis media salarial 2019-2023\data\salarios_reales.csv"
)

# Verificar columnas (debug rápido)
print(dataframe.columns)

# Convertir de float a int
dataframe["salario_real"] = dataframe["salario_real"].round().astype(int)
dataframe["ipc_normalizado"] = dataframe["ipc_normalizado"].round().astype(int)

#Convertir fecha a formato datetime
dataframe['fecha'] = pd.to_datetime(
    dataframe['fecha'],
    format='%Y-%m-%d'
)
dataframe['anio'] = dataframe['fecha'].dt.year
dataframe['mes'] = dataframe['fecha'].dt.month

print(dataframe.dtypes)


dataframe = dataframe.sort_values(['fecha', 'clae2'])


# Guardar CSV actualizado (opción segura)
dataframe.to_csv(
    r"C:\Users\ferra\OneDrive\Documentos\Data Projects\Analisis media salarial 2019-2023\data/salarios_reales.csv",
    index=False
)
