# 🧮 Taller de Evaluación de Rendimiento — Sistemas Operativos
**Pontificia Universidad Javeriana · Facultad de Ingeniería · 2026-01**

> Martín Sanmiguel Delgado · Juan Manuel Baez Parra · Mateo Traslaviña Moreno

---

## 📋 Descripción

Este repositorio contiene el desarrollo completo del Taller de Evaluación de Rendimiento de la materia **Sistemas Operativos**. El objetivo es comparar el rendimiento de dos algoritmos de multiplicación de matrices (**Filas por Columnas** y **Filas por Transpuestas**) bajo distintos niveles de concurrencia (hilos POSIX y procesos Fork), ejecutados en 6 sistemas de cómputo con Linux.

---

## 🗂️ Estructura del Repositorio

```
TALLER-DE-RENDIMIENTO/
│
├── src/                        # Código fuente en C
│   ├── moduloMM.c              # Módulo con los algoritmos de multiplicación
│   ├── moduloMM.h              # Cabecera del módulo
│   ├── mxmPosixFxC.c          # Multiplicación POSIX - Filas por Columnas
│   ├── mxmPosixFxT.c          # Multiplicación POSIX - Filas por Transpuestas
│   ├── mxmForkFxC.c           # Multiplicación Fork - Filas por Columnas
│   └── mxmForkFxT.c           # Multiplicación Fork - Filas por Transpuestas
│
├── bin/                        # Binarios compilados (generados con make)
│
├── Soluciones/                 # Archivos .dat con los tiempos crudos por máquina
│   ├── <Máquina>/
│   │   └── <algoritmo>-<tamaño>-Hilos-<n>.dat
│
├── Graficas_Detalladas/        # Gráficas de barras por combinación + CSVs
├── Graficas_Escalabilidad/     # Gráficas de líneas de escalabilidad por máquina
│
├── Makefile                    # Compila todos los ejecutables
├── lanzador.pl                 # Script Perl de automatización de experimentos
│
├── consolidar_datos.py         # Script Python — Fase 1: consolida .dat → CSV + gráficas resumen
├── graficar_escalabilidad.py   # Script Python — Fase 2: genera gráficas de escalabilidad
│
├── 1_tabla_consolidada_base.csv
├── 2_promedios_globales_por_maquina.csv
├── 3_promedios_por_algoritmo_y_matriz.csv
├── 4_tabla_cruzada_resumen.csv
│
└── README.md
```

---

## ⚙️ Requisitos

**Para compilar y ejecutar los experimentos:**
- Linux (Ubuntu recomendado)
- GCC con soporte para `-lpthread`
- Perl 5+

**Para el análisis de datos:**
- Python 3.8+
- Pandas, Seaborn, Matplotlib

Instalación de dependencias Python:
```bash
pip install pandas seaborn matplotlib
```

---

## 🚀 Cómo reproducir el experimento

### 1. Compilar los binarios
```bash
make All
```

### 2. Crear la carpeta de resultados y dar permisos
```bash
mkdir -p Soluciones
chmod +x bin/*
chmod +x lanzador.pl
```

### 3. Ejecutar la batería de experimentos
```bash
./lanzador.pl
```
Esto ejecutará automáticamente **1,440 corridas** (4 algoritmos × 3 tamaños × 4 niveles de hilos × 30 repeticiones) y guardará los tiempos en archivos `.dat` dentro de `Soluciones/`.

> ⚠️ **Importante:** La ruta del proyecto no debe contener espacios. Si tu ruta tiene espacios (ej. `semestre_ 2026_01`), copia el proyecto a una ruta limpia:
> ```bash
> cp -r /ruta/con\ espacios/TALLER-DE-RENDIMIENTO ~/taller
> cd ~/taller
> ```

### 4. Verificar que los resultados sean correctos
```bash
# Debe mostrar 48 archivos
ls Soluciones/ | wc -l

# Todos deben tener exactamente 30 líneas
wc -l Soluciones/*.dat
```

---

## 📊 Análisis de Datos (Scripts Python)

Los scripts deben ejecutarse desde la raíz del proyecto, **donde están los archivos `.dat`**.

### Fase 1 — Consolidación y gráficas de barras
```bash
python3 consolidar_datos.py
```
**Genera:**
- `1_tabla_consolidada_base.csv` — todos los promedios consolidados
- `2_promedios_globales_por_maquina.csv`
- `3_promedios_por_algoritmo_y_matriz.csv`
- `4_tabla_cruzada_resumen.csv`
- `Graficas_Detalladas/` — 48 gráficas de barras + CSV por combinación

### Fase 2 — Gráficas de escalabilidad
```bash
python3 graficar_escalabilidad.py
```
**Requiere:** que `1_tabla_consolidada_base.csv` ya exista (correr Fase 1 primero).

**Genera:**
- `Graficas_Escalabilidad/` — gráficas de líneas (Hilos vs Tiempo) por máquina y algoritmo

---

## 🖥️ Sistemas de Cómputo Evaluados

| ID | CPU | Núcleos | Frec. Máx. | L2 | L3 | RAM | Tipo |
|---|---|---|---|---|---|---|---|
| PC-1 | Intel Core i7-6500U | 4 | 3.1 GHz | 0.5 MiB | 4 MiB | 7.8 GiB | Portátil |
| PC-2 | Intel Core i7-6500U | 4 | 3.1 GHz | 0.5 MiB | 4 MiB | 7.8 GiB | Portátil |
| Escritorio-1 | Intel Core i7-6700T | 8 | 3.6 GHz | 1.0 MiB | 8 MiB | 7.8 GiB | Desktop |
| Escritorio-2 | Intel Core i7-6700T | 8 | 3.6 GHz | 1.0 MiB | 8 MiB | 7.8 GiB | Desktop |
| PC-Martin | Intel Core i7-13650HX | 20 | 4.9 GHz | 11.5 MiB | 24 MiB | 14.8 GiB | Portátil |
| VM | Intel Xeon Gold 6240R | 4 vCPU | 2.4 GHz | 4.0 MiB | 35.8 MiB | 12 GiB | VMware |

---

## 🔬 Variables Experimentales

| Variable | Valores |
|---|---|
| Algoritmos | FxC (Filas×Columnas), FxT (Filas×Transpuestas) |
| Mecanismo de concurrencia | POSIX Threads, Fork |
| Tamaño de matriz | 512×512, 1024×1024, 2048×2048 |
| Nivel de concurrencia | 1, 4, 8, 16 hilos/procesos |
| Repeticiones por combinación | 30 |
| Métrica principal | Tiempo promedio de ejecución (segundos) |

---

## 📝 Hallazgos Principales

- **FxT es consistentemente más rápido que FxC** gracias al aprovechamiento de localidad espacial en caché (Row-Major Order en C).
- **POSIX Threads supera a Fork** por compartir el espacio de memoria, eliminando el overhead de crear procesos independientes.
- **El overhead de concurrencia domina en matrices pequeñas** (512×512): usar 16 hilos puede ser menos eficiente que la ejecución secuencial.
- **Existe un límite físico de hardware** (Ley de Amdahl): en equipos con 4 núcleos, solicitar 8 o 16 hilos no genera mejora adicional.

---

## 📄 Informe

El informe completo en PDF se encuentra en la raíz del repositorio e incluye introducción, diseño experimental, análisis de resultados con gráficas y conclusiones.
