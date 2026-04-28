import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# =====================================================================
# 1. CONFIGURACIÓN Y CARGA DE DATOS
# =====================================================================
# Asegúrate de que este archivo CSV exista (lo generamos en la etapa anterior)
archivo_datos = '1_tabla_consolidada_base.csv'

# Verificación de que el archivo existe
if not os.path.exists(archivo_datos):
    print(f"Error: No se encontró el archivo '{archivo_datos}'. Por favor, ejecuta primero el script de consolidación.")
    exit()

print("Cargando datos consolidados...")
df = pd.DataFrame()
try:
    df = pd.read_csv(archivo_datos)
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
    exit()

print(f"Se cargaron {len(df)} registros para graficar.\n")

# Carpeta de salida para las nuevas gráficas
carpeta_graficas = 'Graficas_Escalabilidad'
os.makedirs(carpeta_graficas, exist_ok=True)

sns.set_theme(style="whitegrid")

# =====================================================================
# 2. GENERACIÓN AUTOMÁTICA DE GRÁFICAS DE ESCALABILIDAD
# =====================================================================
print(f"Generando gráficas de escalabilidad por hilos...")

# Iterar por cada Algoritmo y por cada Máquina
for maquina in df['Máquina'].unique():
    print(f"-> Procesando máquina: {maquina}...")

    for algo in df['Algoritmo'].unique():

        # Filtrar datos para este algoritmo y esta máquina
        df_filtrado = df[(df['Algoritmo'] == algo) & (df['Máquina'] == maquina)]

        if not df_filtrado.empty:
            # --- Configuración de la gráfica de líneas ---
            plt.figure(figsize=(10, 7))

            # Crear la gráfica de líneas: Eje X = Hilos, Líneas = Tamaño de Matriz
            sns.lineplot(
                data=df_filtrado,
                x='Hilos',
                y='Tiempo Promedio (s)',
                hue='Tamaño Matriz',  # Crea una línea de color diferente por cada matriz
                marker='o',  # Pone un círculo en 1, 4, 8, 16
                palette='Set1',  # Paleta de colores distintivos
                linewidth=2.5,
                markersize=8
            )

            # --- Títulos y Etiquetas ---
            plt.title(f'Escalabilidad: Hilos vs Tiempo en {maquina}\nAlgoritmo: {algo}', fontsize=14, pad=15)
            plt.xlabel('Número de Hilos (Nivel de Concurrencia)', fontsize=12)
            plt.ylabel('Tiempo Promedio de Ejecución (Segundos)', fontsize=12)

            # Forzar que el Eje X solo muestre tus cantidades de hilos exactas
            plt.xticks([1, 4, 8, 16], fontsize=11)
            plt.yticks(fontsize=11)

            # Mover la leyenda afuera de la gráfica si tapa algo
            plt.legend(title='Tamaño de Matriz', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)

            # --- Guardado ---
            nombre_archivo = f"Escalabilidad_{maquina}_{algo}.png"
            ruta_guardado = os.path.join(carpeta_graficas, nombre_archivo)

            plt.tight_layout()
            plt.savefig(ruta_guardado, dpi=300)
            plt.close()

print(f"\n¡Se generaron las gráficas de escalabilidad en la carpeta '{carpeta_graficas}'!")