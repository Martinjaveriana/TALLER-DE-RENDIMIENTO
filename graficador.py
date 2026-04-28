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

# 4. Generar Gráficas con Seaborn
sns.set_theme(style="whitegrid")

# Gráfica A: Comparativa en BARRAS de las 4 Máquinas para la matriz 2048 (PosixFxC)
plt.figure(figsize=(10, 6))
df_2048_posix = df[(df['Tamaño Matriz'] == 2048) & (df['Algoritmo'] == 'mxmPosixFxC')]

if not df_2048_posix.empty:
    # Cambiamos lineplot por barplot
    sns.barplot(data=df_2048_posix, x='Hilos', y='Tiempo Promedio (s)', hue='Máquina', palette='muted')

    plt.title('Comparativa de Rendimiento - Matriz 2048x2048 (PosixFxC)')
    plt.ylabel('Tiempo Promedio de Ejecución (Segundos)')
    plt.xlabel('Cantidad de Hilos')
    plt.savefig('grafica_barras_maquinas_2048.png', dpi=300)
plt.close()

# Gráfica B
primera_maquina = df['Máquina'].iloc[0] if not df.empty else "Desconocida"
plt.figure(figsize=(10, 6))
df_maq = df[(df['Máquina'] == primera_maquina) & (df['Tamaño Matriz'] == 1024)]
if not df_maq.empty:
    sns.lineplot(data=df_maq, x='Hilos', y='Tiempo Promedio (s)', hue='Algoritmo', marker='s', linewidth=2)
    plt.title(f'Rendimiento de Algoritmos en {primera_maquina} - Matriz 1024x1024')
    plt.ylabel('Tiempo Promedio (Segundos)')
    plt.xlabel('Número de Hilos / Procesos')
    plt.xticks([1, 4, 8, 16])
    plt.savefig('grafica_algoritmos_1024.png', dpi=300)
plt.close()

# 5. Exportar Consolidado Base
df.sort_values(by=['Máquina', 'Algoritmo', 'Tamaño Matriz', 'Hilos']).to_csv('1_tabla_consolidada_base.csv', index=False)
print("-> 1_tabla_consolidada_base.csv generada.")

# =====================================================================
# 6. ARCHIVOS ADICIONALES DE PROMEDIOS
# =====================================================================

# A) Promedio Global por Máquina
df_promedio_maquina = df.groupby('Máquina')['Tiempo Promedio (s)'].mean().reset_index()
df_promedio_maquina.to_csv('2_promedios_globales_por_maquina.csv', index=False)
print("-> 2_promedios_globales_por_maquina.csv generado.")

# B) Promedio por Algoritmo y Tamaño de Matriz
df_promedio_algo_matriz = df.groupby(['Algoritmo', 'Tamaño Matriz'])['Tiempo Promedio (s)'].mean().reset_index()
df_promedio_algo_matriz.to_csv('3_promedios_por_algoritmo_y_matriz.csv', index=False)
print("-> 3_promedios_por_algoritmo_y_matriz.csv generado.")

# C) Tabla Cruzada (Pivot Table): AHORA INCLUYE HILOS
# Esto organizará los datos por Máquina -> Tamaño -> Hilos en las filas
tabla_cruzada = pd.pivot_table(df,
                                values='Tiempo Promedio (s)',
                                index=['Máquina', 'Tamaño Matriz', 'Hilos'],
                                columns=['Algoritmo'],
                                aggfunc='mean')
tabla_cruzada.to_csv('4_tabla_cruzada_resumen.csv')
print("-> 4_tabla_cruzada_resumen.csv generada (incluye Hilos).")

print("\n¡Listo! Las tablas y gráficas se han actualizado con el desglose de hilos.")