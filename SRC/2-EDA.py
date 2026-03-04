#   EDA
#   ¿Como evoluciono el salario por industria entre el 2019 y el 2023?

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataframe = pd.read_csv(
    "Data/salarios_clae_clean.csv",
    parse_dates=["fecha"]
)

print(dataframe.info())
print(dataframe.describe())

#       Histograma distribucion de salarios
plt.figure()
plt.hist(dataframe["salario_median"], bins=50)
plt.xlabel("Salario mediano")
plt.ylabel("Frecuencia")
plt.title("Distribucion de salario mediano")
plt.savefig("Graficos/Dist_salario_med.png")
#plt.show()

#Histograma distibucion sin outliers
plt.figure()
plt.hist(
    dataframe[dataframe["salario_median"] < 500000]["salario_median"],
    bins=50
)
plt.xlabel("Salario mediano (< 500k)")
plt.ylabel("Frecuencia")
plt.title("Distribución del salario mediano (sin outliers extremos)")
plt.savefig("Graficos/Dist_salario_med_Sin_Outliers_extremos.png")
#plt.show()


#       Boxplot para detectar Outliers
plt.figure()
plt.boxplot(dataframe["salario_median"], vert=False)
plt.xlabel("Salario mediano")
plt.ylabel("Boxplot del salario mediano")
plt.savefig("Graficos/Boxplot_sal_med.png")
#plt.show()

#       Media vs Mediana
print("Salario promedio")
print(dataframe["salario_median"].mean()) # = 141000
print("Salario medio")
print(dataframe["salario_median"].median()) # = 86000
#   Media influenciada por sueldos altos
#   La mediana representa mejor salarios más tipicos
#   55000 de diferencia con el promedio = Desigualdad entre industrias

print("__________________________________________________________________")


#       Bloque 2 EDA        

salario_por_fecha = dataframe.groupby("fecha")["salario_median"].median()

plt.figure()
plt.plot(salario_por_fecha.index, salario_por_fecha.values)
plt.xlabel("Fecha")
plt.ylabel("Salario mediano")
plt.title("Evolucion del salario mediano (2019 - 2023)")
plt.savefig(
    "Graficos/Evolución_del_salario_mediano.png",
    dpi=300)

#plt.show()

"""""
El crecimiento del salario mediano presenta una tendencia ascendente con picos recurrentes.
  Estos picos no se distribuyen de forma aleatoria, sino que se concentran en actividades económicas 
 específicas con niveles salariales significativamente superiores al promedio, lo que genera distorsiones
   temporales en la serie agregada.
"""

#   Identificar las actividades con salarios mas altos #edit

top_claes = (
    dataframe
    .groupby("clae2", as_index=False)
    ["salario_median"]
    .mean()
    .sort_values("salario_median", ascending=False)
    .head(5)
)
print(top_claes.head(5))

#   Visualizar la evolucion temporal de esas actividades

top_clae_ids = top_claes["clae2"].tolist()

plt.figure(figsize=(12, 6))

for clae in top_clae_ids:
    datos = dataframe[dataframe["clae2"] == clae]
    plt.plot(
        datos["fecha"],
        datos["salario_median"],
        label=f"CLAE {clae}"
    )

plt.title("Evolución del salario mediano - Top 5 sectores")
plt.xlabel("Fecha")
plt.ylabel("Salario mediano")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("Graficos/evolucion_salarios_top_claes.png", dpi=300)
#plt.show()

#   Normalizar salarios

# Asegurarse de que fecha sea datetime
dataframe["fecha"] = pd.to_datetime(dataframe["fecha"])

# Elegimos actividades / Industrias
top_claes = [6, 9, 7, 64, 19]

# Filtramos
df_top = dataframe[dataframe["clae2"].isin(top_claes)]

plt.figure(figsize=(10, 6))

for clae in top_claes:
    datos = df_top[df_top["clae2"] == clae].sort_values("fecha")

    # Normalización base 100
    salario_base = datos["salario_median"].iloc[0]
    salario_normalizado = (datos["salario_median"] / salario_base) * 100

    plt.plot(
        datos["fecha"],
        salario_normalizado,
        label=f"CLAE {clae}"
    )

plt.title("Evolución de salarios medianos normalizados (Base 2019 = 100)")
plt.xlabel("Fecha")
plt.ylabel("Índice salarial")
plt.legend()
plt.grid(True)

plt.savefig(
    "Graficos/salarios_normalizados_por_clae.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

#   Normalizar salarios para ver que sector creció más
#Independientemente de cuánto ganaban en pesos, ¿qué sector tuvo mayor crecimiento relativo?
#   Para que sirve: Eliminar sesgos de inflacion, sectores que empiezan muy alto, escala nominal 

#   Año base
base_year = 2019

salario_base = (
    dataframe[dataframe["fecha"].dt.year == base_year]
    .groupby("clae2")["salario_median"].mean()
)

dataframe["salario_normalizado"] = (
    dataframe["salario_median"] / dataframe["clae2"].map(salario_base)
)
#   
print(dataframe[["fecha", "clae2", "salario_median", "salario_normalizado"]].head()
)

plt.figure(figsize=(12, 6))

for clae in top_clae_ids:
    datos = dataframe[dataframe["clae2"] == clae]
    plt.plot(
        datos["fecha"],
        datos["salario_normalizado"],
        label=f"CLAE {clae}"
    )

plt.axhline(1, linestyle="--")  # línea base
plt.title("Crecimiento salarial normalizado (Base 2019 = 1)")
plt.xlabel("Fecha")
plt.ylabel("Índice salarial")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("Graficos/salarios_normalizados_top_claes.png", dpi=300)
#plt.show()

"""
Con salarios medianos normalizados con base en 2019,se observa un período de estancamiento durante 2020,
con una leve caída en el índice del sector CLAE 9.
A partir de 2021, los sectores seleccionados (CLAE 6, 7, 9, 19 y 64)
muestran trayectorias de crecimiento similares, lo que sugiere un comportamiento dominado por factores macroeconómicos.
Sin embargo, a mediados de 2023, el sector CLAE 64 presenta una ruptura significativa de esta dinámica,
pasando de ubicarse entre los sectores con menor crecimiento relativo a liderar el índice en un período de pocos meses
"""

#   Cuantificar la ruptura de la dinamica de CLAE 64

#   Filtrar clae64
clae64 = dataframe[dataframe["clae2"] == 64].sort_values("fecha")

#   Tomar valores aproximados del salto
inicio = clae64[clae64["fecha"] >= "2023-01-01"].iloc[0]
fin = clae64[clae64["fecha"] <= "2023-11-01"].iloc[-1]

crecimiento = (fin["salario_normalizado"] / inicio["salario_normalizado"] - 1) * 100

print(f"Crecimineto relativo CLAE 64 en 2023: {crecimiento:.2f}%")

"""
CLAE 64 fue la actividad con mayor crecimiento un 237% teniendo en cuenta el año 2019 como piso.
Este comportamiento atípico sugiere la presencia de factores específicos del sector, como recomposición salarial puntual, 
cambios regulatorios o efectos de base, que ameritan un análisis adicional.
"""

#   Comparar crecimiento con otras CLAES (durante el 2023)

#Filtrar 2023
datos_2023 = dataframe[
    (dataframe["fecha"].dt.year == 2023)
].copy()

#Tomar inicio y fin de año x CLAE
crecimiento_clae = []

for clae, grupo in datos_2023.groupby("clae2"):
    grupo = grupo.sort_values("fecha")

    inicio = grupo.iloc[0]["salario_normalizado"]
    fin = grupo.iloc[-1]["salario_normalizado"]

    crecimiento = (fin / inicio - 1) * 100

    crecimiento_clae.append({
        "clae2": clae,
        "crecimiento_pct": crecimiento 
    })

#convertir a dataframe y ordenar
crecimiento_df = pd.DataFrame(crecimiento_clae)

crecimiento_df = crecimiento_df.sort_values(
    "crecimiento_pct",
    ascending=False
)

print(crecimiento_df.head(10))

clae64 = crecimiento_df.loc[
    crecimiento_df["clae2"] == 64,
    "crecimiento_pct"
].values[0]

mean_claes = crecimiento_df.loc[
crecimiento_df["clae2"] != 64,
"crecimiento_pct"
].mean()

print(f"Crecimiento CLAE 64 en 2023: {clae64:.2f}%")
print(f"Promedio del resto de actividades: {mean_claes:.2f}%")
print(f"Diferencia: {clae64 - mean_claes:.2f} puntos porcentuales")

#   Grafico rapido para ver las crecimiento de actividades:

plt.figure(figsize=(10,5))
plt.bar(
    crecimiento_df["clae2"].astype(str),
    crecimiento_df["crecimiento_pct"]
)
plt.xticks(rotation=90)
plt.ylabel("Crecimiento % salario normalizado (2023)")
plt.title("Crecimiento salarial por actividad (CLAE)")
plt.tight_layout()
plt.show()

"""
Que concluciones podemos sacar?
CLAE 64 = 237% 
Promedio otras actividades = 124%

CLAE64 tuvo un crecimiento anomalo el ultimo año lo que deja una ruptura estructural
y debería tener un analisis especifico

"""

#       BLOQUE RANKING

#   Objetivos del bloque:
# En que posiscion quedó cada actividad
# En que percentil está CLAE 64
# Es realmente un Outlier?


#Crear Ranking (1 = mayor crecimiento)
crecimiento_df["ranking"] = crecimiento_df["crecimiento_pct"].rank(
    ascending=False,
    method="min"
)
crecimiento_df = crecimiento_df.sort_values("ranking")

print(crecimiento_df.head(10))

#   Calcular percentil
"""
Que es percentil: Concepto estadistico que se refiere a los valores que dividen un conjunto de datos
en cien partes iguales. Indica el valor por debajo del cual se encuentra un porcentaje especifico
 en el conjunto de datos 
"""

crecimiento_df["percentil"] = crecimiento_df["crecimiento_pct"].rank(
    pct=True
) * 100

#Extraer CLAE 64
fila_64 = crecimiento_df[crecimiento_df["clae2"] == 64]

ranking_64 = fila_64["ranking"].values[0]
percentil_64 = fila_64["percentil"].values[0]
crecimiento_64 = fila_64["crecimiento_pct"].values[0]

# print final (para informe de EDA 1)
print(f"CLAE 64:")
print(f"- Crecimiento 2023: {crecimiento_64:.2f}%")
print(f"- Ranking: puesto {int(ranking_64)}")
print(f"- Percentil: {percentil_64:.1f}")
"""
Al normalizar los salarios medianos con base 2019, se observa que la mayoría de las actividades presentan trayectorias similares
 a partir de 2021. Sin embargo, la actividad CLAE 64 exhibe un crecimiento extraordinario en 2023,
con una suba acumulada del 237,85%, ubicándose en el primer puesto del ranking y en el percentil 100 del conjunto analizado.
Este comportamiento sugiere una dinámica salarial diferencial respecto del resto de los sectores.
"""

# -------------------------
# Exportación para bloques siguientes
# -------------------------

dataframe.to_csv(
    "Data/salarios_limpios.csv",
    index=False
)