# 🧮 Taller de Evaluación de Rendimiento — Sistemas Operativos
**Pontificia Universidad Javeriana · Facultad de Ingeniería · 2026-01**

> Martín Sanmiguel Delgado · Juan Manuel Baez Parra · Mateo Traslaviña Moreno

---

## 📋 Descripción

Este repositorio contiene el desarrollo completo del Taller de Evaluación de Rendimiento de la materia **Sistemas Operativos**. El objetivo es comparar el rendimiento de dos algoritmos de multiplicación de matrices (**Filas por Columnas** y **Filas por Transpuestas**) bajo distintos niveles de concurrencia (hilos POSIX y procesos Fork), ejecutados en 6 sistemas de cómputo con distribuciones Linux.

---

## 🗂️ Estructura del Repositorio

```text
.
├── bin/                            # Binarios compilados
│   ├── mxmForkFxC
│   ├── mxmForkFxT
│   ├── mxmPosixFxC
│   └── mxmPosixFxT
├── src/                            # Código fuente en C
│   ├── moduloMM.c                  # Módulo con la lógica matemática
│   ├── moduloMM.h                  # Cabecera del módulo
│   ├── mxmForkFxC.c                # Multiplicación Fork - Filas por Columnas
│   ├── mxmForkFxT.c                # Multiplicación Fork - Filas por Transpuestas
│   ├── mxmPosixFxC.c               # Multiplicación POSIX - Filas por Columnas
│   └── mxmPosixFxT.c               # Multiplicación POSIX - Filas por Transpuestas
├── Soluciones/                     # Resultados crudos (.dat) organizados por máquina
│   ├── Soluciones-Escritorio-1/
│   ├── Soluciones-escritorio-2/
│   ├── Soluciones-Maquina-Virutal/
│   ├── Soluciones-Pc-1/
│   ├── Soluciones-Pc-2/
│   └── Soluciones-Pc-Martin/
├── graficador.py                   # Suite de procesamiento de datos y graficación
├── graficador2.py                  # Suite de procesamiento de datos y graficación
├── graficador3.py                  # Suite de procesamiento de datos y graficación
├── graficador4.py                  # Suite de procesamiento de datos y graficación
├── lanzador.pl                     # Script Perl de automatización de experimentos
├── Makefile                        # Orquestador de compilación
├── Taller Rendimiento FINAL.pdf    # Informe final documentado del proyecto
└── README.md                       # Documentación del repositorio
```

---

## ⚙️ Requisitos

**Para compilar y ejecutar los experimentos:**
*   Linux (Ubuntu/Debian recomendado)
*   GCC con soporte para la biblioteca `pthread`
*   Perl 5+

**Para el procesamiento de datos y visualización:**
*   Python 3.8+
*   Bibliotecas: `pandas`, `seaborn`, `matplotlib`

*Instalación de dependencias de Python:*
```bash
pip install pandas seaborn matplotlib
```

---

## 🚀 Reproducción del Experimento

### 1. Compilación
Ejecutar el Makefile para compilar el código fuente y generar los ejecutables en la carpeta `bin/`.
```bash
make All
```

### 2. Permisos de Ejecución
Otorgar permisos a los binarios y al script automatizador.
```bash
chmod +x bin/*
chmod +x lanzador.pl
```

### 3. Ejecución de la Batería de Pruebas
```bash
./lanzador.pl
```
Este script compilará el código y ejecutará automáticamente las iteraciones definidas (30 por defecto) para cada combinación de matriz, algoritmo, mecanismo de concurrencia y máquina, exportando los tiempos a la carpeta `Soluciones/`.

### 4. Verificación de Integridad de Datos
Para confirmar que la recolección automatizada fue exitosa:
```bash
# Deben existir exactamente 48 archivos por cada una de las 6 máquinas (288 en total)
ls Soluciones/*/*.dat | wc -l

# Cada archivo debe contener exactamente 30 líneas (correspondientes a las iteraciones para la Ley de los Grandes Números)
wc -l Soluciones/*/*.dat
```

---

## 📊 Análisis y Visualización (Scripts Python)

El repositorio cuenta con un conjunto de scripts en Python (`graficador.py` a `graficador4.py`) diseñados para leer los archivos crudos generados en la fase de recolección, calcular las medias aritméticas para mitigar el ruido computacional (OS Jitter), y generar las gráficas comparativas de escalabilidad, saturación de hardware y *overhead*.

Para ejecutar la suite de graficación:
```bash
python3 graficador.py
python3 graficador2.py
python3 graficador3.py
python3 graficador4.py
```

---

## 🖥️ Sistemas de Cómputo Evaluados

| ID | CPU | Núcleos Lógicos | Frec. Máx. | L2 | L3 | RAM | Tipo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PC-1 | Intel Core i7-6500U | 4 | 3.1 GHz | 0.5 MiB | 4 MiB | 7.8 GiB | Portátil |
| PC-2 | Intel Core i7-6500U | 4 | 3.1 GHz | 0.5 MiB | 4 MiB | 7.8 GiB | Portátil |
| Escritorio-1 | Intel Core i7-6700T | 8 | 3.6 GHz | 1.0 MiB | 8 MiB | 7.8 GiB | Desktop |
| Escritorio-2 | Intel Core i7-6700T | 8 | 3.6 GHz | 1.0 MiB | 8 MiB | 7.8 GiB | Desktop |
| PC-Martin | Intel Core i7-13650HX | 20 | 4.9 GHz | 11.5 MiB | 24 MiB | 14.8 GiB | Portátil |
| VM | Intel Xeon Gold 6240R | 4 vCPU | 2.4 GHz | 4.0 MiB | 35.8 MiB | 12 GiB | VMware |

---

## 🔬 Variables Experimentales

| Variable | Valores Evaluados |
| :--- | :--- |
| **Algoritmos Matemáticos** | FxC (Filas × Columnas), FxT (Filas × Transpuestas) |
| **Mecanismos de Concurrencia**| POSIX Threads (Memoria Compartida), Fork (Memoria Aislada) |
| **Tamaño de la Carga O(N^3)** | 512x512, 1024x1024, 2048x2048 |
| **Nivel de Concurrencia** | 1, 4, 8, 16 CPUs (unidades de ejecución) |
| **Repeticiones (Muestra)** | 30 iteraciones consecutivas por configuración |

---

## 📝 Hallazgos Principales

Los resultados empíricos y los análisis técnicos detallados se encuentran documentados en el informe final (`Taller Rendimiento FINAL.pdf`). Las conclusiones arquitectónicas más destacadas son:

*   **Supremacía de la Localidad Espacial:** El algoritmo FxT es significativamente superior a FxC al respetar el almacenamiento *Row-Major Order* del lenguaje C, mitigando la abrumadora penalización temporal de los fallos de caché (*cache misses*).
*   **Punto de Quiebre Arquitectónico:** POSIX Threads superó consistentemente la creación de procesos (*Fork*), consolidándose como la arquitectura ideal para cargas masivas. El mecanismo Fork demostró no ser escalable para matrices pesadas (2048x2048) debido a la colosal demanda de memoria y procesos de aislamiento.
*   **Penalización Administrativa:** En cargas de trabajo ligeras (512x512), el *overhead* de concurrencia administrado por el Kernel es mayor que el beneficio del paralelismo, provocando que la ejecución con 16 hilos sea menos eficiente que la puramente secuencial.
*   **Límites Físicos y Ley de Amdahl:** Al saturar equipos de 4 u 8 núcleos con 16 unidades de ejecución solicitadas por software, las curvas de rendimiento se estancan por completo producto de los continuos cambios de contexto (*context switching*).
*   **El Impacto de la Brecha Generacional:** El PC-Martin fue la única arquitectura capaz de mantener un paralelismo físico real con 16 unidades de ejecución simultáneas, demostrando que frente a cargas de tipo *Memory-bound*, una memoria Caché L3 masiva (24 MiB) y una alta densidad de núcleos superan la simple velocidad bruta de reloj.