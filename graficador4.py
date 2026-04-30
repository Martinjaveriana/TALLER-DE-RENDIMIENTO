import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =====================================================================
# 1. CARGA DE DATOS Y LIMPIEZA
# =====================================================================
archivo_datos = '1_tabla_consolidada_base.csv'

if not os.path.exists(archivo_datos):
    print(f"Error: No se encontró el archivo '{archivo_datos}'.")
    exit()

print("Cargando datos para el análisis comparativo agrupado...")
df = pd.read_csv(archivo_datos)

# Limpieza de nombres de máquinas (Quitar "Solucion")
df['Máquina'] = df['Máquina'].str.replace('Solucion', '', case=False)
df['Máquina'] = df['Máquina'].str.replace('_', ' ')
df['Máquina'] = df['Máquina'].str.replace('-', ' ')
df['Máquina'] = df['Máquina'].str.strip()

carpeta_graficas = 'Graficas_Comparativa_Hardware'
os.makedirs(carpeta_graficas, exist_ok=True)

sns.set_theme(style="whitegrid")

# --- NUEVO: CREAR UNA PALETA DE COLORES FIJA ---
# Obtenemos todas las máquinas únicas (ordenadas alfabéticamente para consistencia)
maquinas_unicas = sorted(df['Máquina'].unique())
# Usamos una paleta cualitativa que distingue muy bien las categorías (tab10)
colores_base = sns.color_palette("tab10", len(maquinas_unicas))
# Creamos un diccionario que vincula para siempre una máquina a un color
paleta_fija = dict(zip(maquinas_unicas, colores_base))

# =====================================================================
# 2. GENERACIÓN DE GRÁFICAS DE BARRAS AGRUPADAS
# =====================================================================
print("Generando gráficas comparativas de hardware...")

# Iteramos por cada Algoritmo y Tamaño de Matriz
for algo in df['Algoritmo'].unique():
    for tam in df['Tamaño Matriz'].unique():

        df_filtrado = df[(df['Algoritmo'] == algo) & (df['Tamaño Matriz'] == tam)]

        if not df_filtrado.empty:
            plt.figure(figsize=(12, 7))

            # --- ORDENAMIENTO DE BARRAS (Menor a Mayor) ---
            # Calculamos el tiempo promedio de cada máquina para este escenario exacto
            # y ordenamos de menor (más rápido) a mayor (más lento)
            orden_maquinas = df_filtrado.groupby('Máquina')['Tiempo Promedio (s)'].mean().sort_values().index.tolist()

            # Crear gráfica de barras: X = CPUs, Color(Hue) = Máquina
            sns.barplot(
                data=df_filtrado,
                x='Hilos',  # Eje X (mantenemos la columna interna 'Hilos')
                y='Tiempo Promedio (s)',  # Altura de la barra
                hue='Máquina',  # Cada barra de color es una máquina
                hue_order=orden_maquinas,  # Fuerza el orden de más rápido a más lento
                palette=paleta_fija  # --- NUEVO: Usar el diccionario de colores fijos ---
            )

            # --- Títulos y Etiquetas ---
            plt.title(f'Rendimiento de Hardware vs Nivel de Concurrencia\nAlgoritmo: {algo} | Matriz: {tam}x{tam}',
                      fontsize=15, pad=15)
            plt.xlabel('Número de CPUs Solicitadas', fontsize=12)
            plt.ylabel('Tiempo Promedio de Ejecución (Segundos)', fontsize=12)

            # Ubicar la leyenda afuera para que no tape las barras
            plt.legend(title='Sistema de Cómputo\n(Ordenado de Menor a Mayor tiempo)',
                       bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)

            nombre_archivo = f"Comparativa_{algo}_Matriz{tam}.png"
            ruta_guardado = os.path.join(carpeta_graficas, nombre_archivo)

            plt.tight_layout()
            plt.savefig(ruta_guardado, dpi=300)
            plt.close()

print(f"\n¡Se generaron las gráficas comparativas en la carpeta '{carpeta_graficas}' manteniendo los colores estáticos!")