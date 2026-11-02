import pandas as pd

# Parte 1. Exploración inicial de los datos

# Carga de datos
datos = pd.read_csv("datos.csv")

# Dimensiones del DataFrame
filas, columnas = datos.shape
print(f"Filas: {filas}, Columnas: {columnas}")

# Información respecto a los tipos de variable y los datos faltantes
datos.info()

# Hay identificadores duplicados?
print(f"Hay {datos["id_estudiante"].duplicated().sum()} identificadores duplicados.")


