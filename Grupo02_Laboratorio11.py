import pandas as pd
import matplotlib.pyplot as plt

# ********** Parte 1. Exploración inicial de los datos **********

# PUNTO 1
# Carga de datos
datos = pd.read_csv("datos.csv")
# Dimensiones del DataFrame
filas, columnas = datos.shape
print(f"Filas: {filas}, Columnas: {columnas}")
# Información respecto a los tipos de variable y los datos faltantes
datos.info()
# Hay identificadores duplicados?
print(f"Hay {datos["id_estudiante"].duplicated().sum()} identificadores duplicados.")

# PUNTO 2
# Cuál es la unidad de observación?
print(datos.head())

# ********** Parte 2. Representatividad de la muestra **********

# PUNTO 3
# Se crea una tabla de frecuencias para la columna grupo.
frecuencia_muestra = (datos["grupo"].value_counts(normalize=True)*100).round(1)
print(frecuencia_muestra)
# Se definen los valores de la población con la informacion presentada en poblacion_referncia.csv
proporcion_poblacion = {"Urbano": 80.0, "Rural": 20.0}
# Se crea un dataframe que integra frecuencia_muestra y proporcion_poblacion
df_comparacion = pd.DataFrame({
    "Muestra (%)": frecuencia_muestra,
    "Población (%)": proporcion_poblacion
})
# Verificamos la correcta creación del dataframe
print(df_comparacion)

# PUNTO 4
# Se crea el gráfico de barras agrupadas
df_comparacion.plot(kind="bar", figsize=(8, 5), width=0.8)
# Personalización del gráfico
plt.title("Comparación de Proporciones: Muestra vs. Población")
plt.xlabel("Grupo Territorial")
plt.ylabel("Porcentaje (%)")
plt.xticks(rotation=0)
plt.legend(title="Origen")
plt.grid(axis="y", linestyle="--", alpha=0.7)
#plt.savefig("comparacion_proporciones.png")
plt.show()

# ********** Parte 3. Datos faltantes y exclusión de observaciones **********

# PUNTO 6
# Suma de la cantidad de valores faltantes
n_faltantes = datos.isnull().sum()
# DataFrame con n_faltantes y porcentaje de faltantes
faltantes = pd.DataFrame({
    "Número de faltantes": n_faltantes,
    "Porcentaje de faltantes": (n_faltantes/12).round(1)
})
print(faltantes)

# PUNTO 7
# Se creó un DataFrame donde el porcentaje de faltantes esta representado frente a la totalidad de los registros.
# Se utilizó .groupby() para agrupar por la variable "grupo"
df_faltantes_grupo = datos.groupby('grupo')[['dispositivo', 'acceso_internet', 'uso_plataforma']].apply(lambda x: x.isnull().mean() * 100).round(1)
print(df_faltantes_grupo)

# PUNTO 8

# Crear la variable booleana respuesta_completa
datos["respuesta_completa"] = (
    datos[["dispositivo", "acceso_internet", "uso_plataforma"]]
    .notna()
    .all(axis=1)
)

# Crear subconjunto con observaciones completas
datos_completos = datos[datos["respuesta_completa"]]

# Número de estudiantes que permanecen y que se excluyen
n_permanecen = datos_completos.shape[0]
n_excluidos = datos.shape[0] - n_permanecen

print(f"Estudiantes que permanecen: {n_permanecen}")
print(f"Estudiantes excluidos: {n_excluidos}")

# PUNTO 9

# Composición por grupos en la base original
composicion_original = (
    datos["grupo"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

# Composición por grupos en la base filtrada
composicion_filtrada = (
    datos_completos["grupo"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

# Porcentaje de estudiantes que permanece dentro de cada grupo
permanencia_grupo = (
    datos_completos.groupby("grupo").size()
    / datos.groupby("grupo").size()
    * 100
).round(1)

# Tabla resumen
comparacion_grupos = pd.DataFrame({
    "Original (%)": composicion_original,
    "Filtrada (%)": composicion_filtrada,
    "% que permanece": permanencia_grupo
})

print(comparacion_grupos)

# ********** Parte 4. Consecuencias para el análisis **********

# PUNTO 10

# Estadísticas descriptivas - Base original
print("BASE ORIGINAL")
print(datos.groupby("grupo")["uso_plataforma"].describe())


# Estadísticas descriptivas - Base filtrada
print("BASE FILTRADA")
print(datos_completos.groupby("grupo")["uso_plataforma"].describe())


# Boxplot comparativo

fig, axes = plt.subplots(1, 2, figsize=(12,5))

datos.boxplot(
    column="uso_plataforma",
    by="grupo",
    ax=axes[0]
)
axes[0].set_title("Base original")
axes[0].set_ylabel("Uso plataforma")

datos_completos.boxplot(
    column="uso_plataforma",
    by="grupo",
    ax=axes[1]
)
axes[1].set_title("Base filtrada")

plt.suptitle("")
plt.tight_layout()
plt.show()
