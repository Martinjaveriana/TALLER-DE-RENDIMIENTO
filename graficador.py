import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuración de la ruta principal
directorio_base = 'Soluciones'
datos = []

print("Buscando archivos .dat en las subcarpetas de las máquinas...")

# 2. Caminar por todas las subcarpetas
for raiz, directorios, archivos in os.walk(directorio_base):
    for archivo in archivos:
        if archivo.endswith('.dat'):
            maquina = os.path.basename(raiz)
            partes = archivo.replace('.dat', '').split('-')

            algoritmo = partes[0]
            tamano = int(partes[1])
            hilos = int(partes[3])

            ruta_completa = os.path.join(raiz, archivo)

            # Leer los 30 tiempos y calcular el promedio
            with open(ruta_completa, 'r') as f:
                tiempos = [float(linea.strip()) for linea in f if linea.strip()]

            if tiempos:
                promedio = sum(tiempos) / len(tiempos)
                datos.append({
                    'Máquina': maquina,
                    'Algoritmo': algoritmo,
                    'Tamaño Matriz': tamano,
                    'Hilos': hilos,
                    'Tiempo Promedio (s)': promedio
                })

# 3. Convertir a DataFrame de Pandas
df = pd.DataFrame(datos)
print(f"Se procesaron {len(df)} combinaciones exitosamente.\n")

# =====================================================================
# 4. GENERACIÓN MASIVA DE GRÁFICAS DETALLADAS Y TABLAS CSV
# =====================================================================
sns.set_theme(style="whitegrid")

carpeta_graficas = 'Graficas_Detalladas'
os.makedirs(carpeta_graficas, exist_ok=True)

print("Generando 48 gráficas individuales y sus tablas CSV... Esto tomará unos segundos.")

for algo in df['Algoritmo'].unique():
    for tam in df['Tamaño Matriz'].unique():
        for hilo in df['Hilos'].unique():

            df_filtrado = df[(df['Algoritmo'] == algo) &
                             (df['Tamaño Matriz'] == tam) &
                             (df['Hilos'] == hilo)]

            if not df_filtrado.empty:
                # Nombre base para que la imagen y el CSV se llamen igual
                nombre_base = f"{algo}_Matriz{tam}_Hilos{hilo}"

                # --- NUEVO: Exportar los datos exactos de la gráfica a CSV ---
                ruta_csv = os.path.join(carpeta_graficas, f"Tabla_{nombre_base}.csv")
                # Solo guardamos las columnas que importan para esta vista
                df_filtrado[['Máquina', 'Tiempo Promedio (s)']].to_csv(ruta_csv, index=False)

                # --- Generar la gráfica ---
                plt.figure(figsize=(8, 6))

                sns.barplot(data=df_filtrado, x='Máquina', y='Tiempo Promedio (s)', hue='Máquina', palette='viridis',
                            legend=False)

                plt.title(f'Rendimiento: {algo} | Matriz {tam}x{tam} | {hilo} Hilo(s)', pad=20, fontsize=14)
                plt.ylabel('Tiempo Promedio de Ejecución (Segundos)')
                plt.xlabel('Sistema de Cómputo (Máquina)')

                plt.xticks(rotation=45, ha='right')

                ruta_guardado = os.path.join(carpeta_graficas, f"Grafica_{nombre_base}.png")

                plt.tight_layout(pad=2.0)
                plt.savefig(ruta_guardado, dpi=300)
                plt.close()

print(f"¡Gráficas individuales y tablas CSV guardadas en la carpeta '{carpeta_graficas}' sin solapamientos!")