# 📊 Generador de PDF Consolidado - Indicadores y Modelos

## 🎯 Descripción

Este módulo automatiza la creación de un **único PDF consolidado** que contiene todos los indicadores estratégicos de la institución, organizados por Línea Estratégica, con todos sus modelos de proyección, gráficos históricos y fichas de análisis.

### ✨ Características Principales

- **Automatización completa**: Itera automáticamente por todas las líneas, indicadores y modelos
- **Diseño institucional**: Replica fielmente el diseño visual de la aplicación Streamlit
- **PDF único consolidado**: Todo el contenido en un solo documento organizado jerárquicamente
- **Gráficos de alta calidad**: Genera gráficos Plotly con resolución profesional
- **Fichas de resumen**: Métricas clave, escenarios y análisis comparativos
- **Numeración automática**: Páginas numeradas automáticamente
- **Portadas organizadas**: Portada general y portadas por sección

## 📁 Estructura del PDF Generado

```
📄 Reporte_Consolidado_Indicadores_Modelos.pdf
│
├── 📋 PORTADA GENERAL
│   ├── Logo institucional
│   ├── Título del reporte
│   ├── Fecha de generación
│   └── Información institucional
│
├── 📂 LÍNEA ESTRATÉGICA: EXPANSIÓN
│   ├── Portada de sección
│   │
│   ├── 📊 INDICADOR: Total Población
│   │   ├── 🧠 MODELO: Media Móvil Tendencia
│   │   │   ├── Portada indicador-modelo
│   │   │   ├── 📋 Ficha de Resumen (métricas clave)
│   │   │   ├── 📈 Gráfico de Evolución y Proyección
│   │   │   └── 🌍 Comparativo de Escenarios
│   │   │
│   │   ├── 🧠 MODELO: ETS
│   │   │   ├── Portada indicador-modelo
│   │   │   ├── 📋 Ficha de Resumen
│   │   │   ├── 📈 Gráfico
│   │   │   └── 🌍 Comparativo de Escenarios
│   │   │
│   │   └── ... (otros modelos)
│   │
│   ├── 📊 INDICADOR: Total estudiantes nuevos
│   │   └── ... (todos los modelos)
│   │
│   └── ... (todos los indicadores de la línea)
│
├── 📂 LÍNEA ESTRATÉGICA: CALIDAD
│   └── ... (misma estructura)
│
├── 📂 LÍNEA ESTRATÉGICA: EXPERIENCIA
│   └── ...
│
├── 📂 LÍNEA ESTRATÉGICA: SOSTENIBILIDAD
│   └── ...
│
├── 📂 LÍNEA ESTRATÉGICA: TRANSFORMACIÓN ORGANIZACIONAL
│   └── ...
│
└── 📂 LÍNEA ESTRATÉGICA: EDUCACIÓN PARA LA VIDA
    └── ...
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.8+**
- Archivos de datos:
  - `Data/Dataset_Unificado.xlsx` (datos históricos)
  - `Data/Proyecciones_Multimodelo.xlsx` (proyecciones)
- Logo institucional: `Wallpaper-POLI.jpg` (opcional)

### Instalación de Dependencias

Las dependencias necesarias ya están incluidas en el archivo `requirements.txt` del proyecto:

```bash
pip install -r requirements.txt
```

**Dependencias principales utilizadas:**
- `reportlab`: Generación de PDFs
- `plotly`: Generación de gráficos interactivos
- `pandas`: Manipulación de datos
- `numpy`: Operaciones numéricas
- `pillow`: Procesamiento de imágenes
- `openpyxl`: Lectura de archivos Excel

## 📖 Uso del Módulo

### Ejecución Básica

Desde la terminal, en el directorio del proyecto:

```bash
python generar_pdf_consolidado.py
```

### Ejecución desde otro Script

```python
from generar_pdf_consolidado import main

# Generar el PDF completo
main()
```

### Ejecución Programática Avanzada

```python
from generar_pdf_consolidado import cargar_datos, GeneradorPDFConsolidado

# Cargar datos
df_hist, df_proj = cargar_datos()

# Crear generador
generador = GeneradorPDFConsolidado(df_hist, df_proj)

# Generar PDF
generador.generar_pdf()
```

## ⚙️ Configuración Personalizada

### Modificar Rutas de Archivos

Edita las constantes en `generar_pdf_consolidado.py`:

```python
# Rutas de datos
RUTA_DATASET = BASE_DIR / "Data" / "Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx"

# Logo y salida
LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"
OUTPUT_PDF = BASE_DIR / "Reporte_Consolidado_Indicadores_Modelos.pdf"
```

### Personalizar Años de Comparación

```python
# Años de análisis
BASE_YEAR = 2025        # Año base histórico
COMP_YEAR_1 = 2026      # Primer año de comparación
COMP_YEAR_2 = 2030      # Segundo año de comparación
```

### Ajustar Colores Institucionales

```python
COLORES_LINEAS = {
    "Expansión": "#2c5f8d",
    "Transformación_Organizacional": "#1e3a5f",
    "Calidad": "#4a90c8",
    # ... personaliza según tu paleta
}
```

## 📊 Contenido Generado

### 1. Portada General

- Logo institucional (si está disponible)
- Título del reporte
- Fecha y hora de generación
- Información institucional

### 2. Portada de Línea Estratégica

Para cada línea estratégica:
- Nombre de la línea con color institucional
- Descripción de la sección
- Separador visual

### 3. Portada Indicador-Modelo

Para cada combinación indicador-modelo:
- Nombre del indicador
- Modelo de proyección utilizado
- Línea estratégica asociada
- Fecha de análisis

### 4. Ficha de Resumen

Tabla con métricas clave:
- 📈 **Último Histórico** (BASE_YEAR)
- 🎯 **Proyección COMP_YEAR_1** (ej: 2026)
- ⭐ **Proyección COMP_YEAR_2** (ej: 2030)
- **Δ Variación Periodo**: Diferencia entre COMP_YEAR_2 y COMP_YEAR_1
- 📊 **Tendencia**: Creciente 🟢 / Decreciente 🔴 / Estable 🟡

### 5. Gráfico de Evolución y Proyección

Gráfico de líneas que incluye:
- **Serie histórica** (línea dorada continua)
- **Proyecciones por escenario**:
  - Realista (azul, línea punteada)
  - Pesimista (rojo, línea punteada)
  - Optimista (verde, línea punteada)
- **Línea divisoria** 2025/2026 (marca inicio de proyección)
- Ejes con formato apropiado según decimales del indicador

### 6. Comparativo de Escenarios

Tabla comparativa con:
- Proyecciones para COMP_YEAR_1 y COMP_YEAR_2
- Variación porcentual vs BASE_YEAR
- Diferenciación visual por escenario (colores de fondo)

## 🔍 Ejemplos de Salida

### Métricas en Ficha de Resumen

```
┌──────────────────────────────┬──────────────┐
│ MÉTRICA                      │ VALOR        │
├──────────────────────────────┼──────────────┤
│ 📈 Último Histórico          │ 25,340       │
│ 🎯 Proyección 2026           │ 26,500       │
│ ⭐ Proyección 2030           │ 30,200       │
│ Δ Variación Periodo          │ 3,700        │
│ 📊 Tendencia Periodo         │ Creciente 🟢 │
└──────────────────────────────┴──────────────┘
```

### Comparativo de Escenarios

```
┌────────────┬─────────────┬──────────┬─────────────┬──────────┐
│ ESCENARIO  │ PROY. 2026  │ Δ% vs    │ PROY. 2030  │ Δ% vs    │
│            │             │ 2025     │             │ 2025     │
├────────────┼─────────────┼──────────┼─────────────┼──────────┤
│ Realista   │ 26,500      │ +4.58%   │ 30,200      │ +19.17%  │
│ Pesimista  │ 25,800      │ +1.82%   │ 28,500      │ +12.46%  │
│ Optimista  │ 27,200      │ +7.34%   │ 32,000      │ +26.28%  │
└────────────┴─────────────┴──────────┴─────────────┴──────────┘
```

## 🎨 Diseño Visual

### Paleta de Colores

- **Azul Institucional Principal**: `#2c5f8d`
- **Azul Oscuro**: `#1e3a5f`
- **Azul Claro**: `#4a90c8`
- **Verde (Sostenibilidad/Optimista)**: `#2ecc71`
- **Rojo (Pesimista)**: `#e74c3c`
- **Dorado (Histórico)**: `#D4A017`

### Tipografía

- **Familia principal**: Helvetica
- **Títulos**: Helvetica-Bold
- **Tamaños**:
  - Portada: 24pt
  - Sección: 20pt
  - Indicador: 16pt
  - Modelo: 14pt
  - Texto normal: 10pt

## 📈 Flujo de Procesamiento

```
┌─────────────────────────────────────────────────────┐
│ 1. CARGA DE DATOS                                   │
│    ├── Dataset_Unificado.xlsx (históricos)         │
│    └── Proyecciones_Multimodelo.xlsx               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. NORMALIZACIÓN Y VALIDACIÓN                       │
│    ├── Parseo de fechas                            │
│    ├── Renombrado de columnas                      │
│    └── Formato largo de proyecciones               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. ITERACIÓN JERÁRQUICA                             │
│    ├── Por cada Línea Estratégica                   │
│    │   ├── Por cada Indicador (orden manual)       │
│    │   │   └── Por cada Modelo disponible          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. GENERACIÓN DE CONTENIDO                          │
│    ├── Portadas                                     │
│    ├── Fichas de resumen                            │
│    ├── Gráficos Plotly → PNG                        │
│    └── Tablas comparativas                          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 5. CONSTRUCCIÓN DEL PDF                             │
│    ├── Ensamblaje de elementos (story)             │
│    ├── Aplicación de estilos                       │
│    ├── Numeración de páginas                       │
│    └── Generación del archivo final                │
└─────────────────────────────────────────────────────┘
```

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo..."

**Problema**: No encuentra los archivos de datos.

**Solución**:
```python
# Verifica que las rutas sean correctas
print(RUTA_DATASET.exists())  # Debe ser True
print(RUTA_PROYECCIONES.exists())  # Debe ser True
```

### Error: "Faltan columnas requeridas..."

**Problema**: El archivo de proyecciones no tiene las columnas esperadas.

**Solución**: Asegúrate de que `Proyecciones_Multimodelo.xlsx` contenga:
- `Indicador` o `indicador`
- `Modelo` o `modelo`
- `Fecha_Proyeccion` o `fecha_proyeccion`
- `Escenario_Realista` (o `proyeccion`)
- `Escenario_Pesimista` (o `ic_inferior`)
- `Escenario_Optimista` (o `ic_superior`)

### Error al generar gráficos

**Problema**: Falla la generación de imágenes Plotly.

**Solución**:
```bash
# Instalar/actualizar kaleido (motor de renderizado de Plotly)
pip install -U kaleido
```

### PDF vacío o incompleto

**Problema**: El PDF se genera pero está vacío o incompleto.

**Solución**:
1. Verifica que hay datos en los DataFrames:
   ```python
   print(f"Históricos: {len(df_hist)} registros")
   print(f"Proyecciones: {len(df_proj)} registros")
   ```
2. Revisa los logs de consola para identificar qué secciones se están procesando.

### Memoria insuficiente

**Problema**: Error de memoria al procesar muchos indicadores.

**Solución**: Procesar por lotes modificando el código para iterar sobre un subconjunto de líneas.

## 📊 Estadísticas Típicas

Un reporte completo típicamente contiene:

- **6 Líneas Estratégicas**
- **~50-60 Indicadores únicos**
- **~5-10 Modelos por indicador**
- **~300-600 páginas totales**
- **Tamaño de archivo**: 20-50 MB
- **Tiempo de generación**: 5-15 minutos (según hardware)

## 🔄 Actualizaciones Futuras

### Mejoras Planeadas

- [ ] Opción de filtrar líneas/indicadores específicos
- [ ] Generación paralela de gráficos (multiprocessing)
- [ ] Soporte para exportar secciones individuales
- [ ] Tabla de contenidos interactiva con bookmarks
- [ ] Modo "resumen ejecutivo" (solo métricas clave)
- [ ] Integración con scheduler para generación automática periódica

## 📞 Contacto y Soporte

Para preguntas, sugerencias o reportar problemas:

- **Proyecto**: Modelo Prospectivo POLI 2026-2030
- **Institución**: Politécnico Grancolombiano
- **Documentación adicional**: Ver `app_streamlit.py` para referencia de la aplicación web

## 📄 Licencia

Este módulo es parte del sistema de indicadores institucionales del Politécnico Grancolombiano.

---

**Generado con**: Python + ReportLab + Plotly
**Última actualización**: 2025-01-26
