import pandas as pd
import matplotlib.pyplot as plt

# ********** Parte 1. Exploración inicial de los datos **********

# Carga de datos
datos = pd.read_csv("datos.csv")

# Dimensiones del DataFrame
filas, columnas = datos.shape
print(f"Filas: {filas}, Columnas: {columnas}")

# Información respecto a los tipos de variable y los datos faltantes
datos.info()

# Hay identificadores duplicados?
print(f"Hay {datos["id_estudiante"].duplicated().sum()} identificadores duplicados.")

# Cuál es la unidad de observación?
print(datos.head())

# ********** Parte 2. Representatividad de la muestra **********

# Se crea una tabla de frecuencias para la columna grupo.
frecuencia_muestra = (datos["grupo"].value_counts(normalize=True)*100).round(1)
print(frecuencia_muestra)

# 2. Definimos los valores de la población
proporcion_poblacion = {"Urbano": 80.0, "Rural": 20.0}

# 3. Creamos un DataFrame combinando ambos
df_comparacion = pd.DataFrame({
    "Muestra (%)": frecuencia_muestra,
    "Población (%)": proporcion_poblacion
})

print(df_comparacion)

# 4. Creamos el gráfico de barras agrupadas
df_comparacion.plot(kind="bar", figsize=(8, 5), width=0.8)

# Personalización del gráfico
plt.title("Comparación de Proporciones: Muestra vs. Población")
plt.xlabel("Grupo Territorial")
plt.ylabel("Porcentaje (%)")
plt.xticks(rotation=0)  # Mantiene los nombres de los grupos horizontales
plt.legend(title="Origen")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("comparacion_proporciones.png")
plt.show()