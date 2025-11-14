# CLAUDE.md - AI Assistant Guide for Modelo Prospectivo

**Last Updated:** 2025-11-14
**Project:** Modelo Prospectivo POLI 2026-2030
**Purpose:** Strategic institutional indicator forecasting platform

---

## 🎯 PROJECT OVERVIEW

### What is This Project?

This is a **prospective modeling and forecasting platform** for the Universidad Politécnica (POLI) designed to:
- Analyze historical performance across 6 strategic institutional lines
- Generate forecasts for indicators spanning 2026-2030 using multiple ML models
- Provide interactive scenario planning (Base, Optimistic, Pessimistic)
- Support strategic planning and decision-making for institutional leadership

### Technology Stack

- **Language:** Python 3.13.7 (virtual environment)
- **Web Framework:** Streamlit (interactive dashboards)
- **ML/Forecasting:** Prophet, ARIMA, ETS, Holt-Winters, Random Forest, XGBoost, SVR
- **Data Processing:** Pandas, NumPy, Scipy
- **Visualization:** Plotly, Altair, Matplotlib
- **Data I/O:** openpyxl, xlsxwriter, python-pptx, ReportLab
- **Database:** SQLite (proyecciones.db)

### Project Type

**Data Science / Business Intelligence Application** with:
- Multi-model ensemble forecasting
- Interactive web-based dashboards
- Excel-based data pipeline
- Scenario analysis capabilities

---

## 📁 CODEBASE STRUCTURE

### Directory Layout

```
Modelo_Prospectivo/
├── .devcontainer/              # Docker dev environment
│   └── devcontainer.json       # Auto-setup for VS Code/Codespaces
│
├── Data/                       # INPUT: Historical indicator data
│   ├── Dataset_Unificado.xlsx  # ⭐ Main unified dataset (ALL historical data)
│   ├── Resultados Consolidados.xlsx
│   └── [other data files]
│
├── Proyecciones/              # OUTPUT: Forecast results
│   ├── Proyecciones_Multimodelo*.xlsx  # All model forecasts
│   ├── Proyecciones_ARIMA_Escenarios.xlsx  # Scenario-based projections
│   └── Proyecciones_Indicadores.xlsx  # Individual indicator results
│
├── Slides/                    # Presentation assets
│   └── Diapositiva*.JPG       # 15 presentation slides
│
├── Scripts/                   # Virtual environment binaries
├── Lib/                       # Python packages (site-packages)
├── share/                     # Jupyter Lab extensions
│
├── app_streamlit.py           # ⭐ MAIN WEB APPLICATION (1322 lines)
├── Modelos.py                 # ⭐ CORE FORECASTING ENGINE (930 lines)
├── Presentacion.py            # Presentation viewer (609 lines)
├── ETL.py                     # Data extraction/transformation (133 lines)
├── Validación.py              # Data validation logic (133 lines)
├── generar_informe_unificado.py  # PDF report generation (310 lines)
│
├── add_rangeslider.py         # Utility: Add sliders to Plotly charts
├── remove_rangeslider.py      # Utility: Remove sliders from Plotly charts
├── fix_indent.py              # Utility: Fix Python indentation issues
├── fix_syntax.py              # Utility: Fix Python syntax errors
│
├── requirements.txt           # Python dependencies
├── pyvenv.cfg                 # Virtual environment config
├── proyecciones.db            # SQLite database (cached projections)
├── Wallpaper-POLI.jpg         # Institution logo/branding
├── Modelos_Pronostico.pptx    # PowerPoint presentation
└── Datos_Unificados.xlsx      # Unified data export
```

### Key Files for AI Assistants

| File | Lines | Purpose | When to Edit |
|------|-------|---------|--------------|
| `app_streamlit.py` | 1322 | Main web UI, visualization, user interactions | UI changes, new visualizations, dashboard updates |
| `Modelos.py` | 930 | ML models, forecasting logic, data validation | New models, parameter tuning, forecast logic |
| `ETL.py` | 133 | Data extraction, transformation, unification | New data sources, column mappings, data cleaning |
| `Validación.py` | 133 | Data consistency checks, quality validation | New validation rules, data integrity checks |
| `generar_informe_unificado.py` | 310 | PDF report generation with ReportLab | Report format changes, new exports |
| `Presentacion.py` | 609 | Streamlit-based presentation viewer | Presentation flow changes |

---

## 🔑 KEY CONVENTIONS & PATTERNS

### 1. **Indicator Type System**

All indicators are classified by their unit type, which drives validation and forecasting behavior:

```python
INDICATOR_TYPES = {
    '%': {
        'description': 'Percentage indicators',
        'value_range': (0, 100),
        'examples': ['Retention rate', 'Satisfaction %', 'Compliance %'],
        'confidence_interval': (0.01, 0.03),
        'max_annual_change': 5%  # Conservative growth limits
    },
    'ENT': {
        'description': 'Integer/Entity counts',
        'value_range': (0, None),
        'examples': ['Student count', 'Program count', 'Employee count'],
        'confidence_interval': (0.05, 0.15),
        'max_annual_change': 50%  # Allows strong growth
    },
    'DEC': {
        'description': 'Decimal values',
        'value_range': (0, None),
        'examples': ['Ratios', 'Scores', 'Averages'],
        'confidence_interval': (0.05, 0.12),
        'max_annual_change': 40%
    },
    '$': {
        'description': 'Currency/Financial metrics',
        'value_range': (0, None),
        'examples': ['EBITDA', 'Revenue', 'Costs'],
        'confidence_interval': (0.05, 0.15),
        'max_annual_change': 50%
    },
    'DEFAULT': {
        'description': 'Fallback for unclassified indicators',
        'confidence_interval': (0.05, 0.12),
        'max_annual_change': 40%
    }
}
```

**⚠️ CRITICAL:** Always respect indicator type limits when generating or validating forecasts!

### 2. **Six Strategic Lines of the Institution**

All indicators are grouped into strategic categories:

```python
STRATEGIC_LINES = {
    1: "Expansión",                        # Market expansion, enrollment growth
    2: "Transformación Organizacional",    # Digital transformation, org change
    3: "Calidad",                          # Accreditation, quality metrics
    4: "Experiencia",                      # Student/stakeholder satisfaction
    5: "Sostenibilidad",                   # Financial sustainability, efficiency
    6: "Educación para la Vida"            # Lifelong learning, continuing ed
}
```

**Navigation in app_streamlit.py:**
- Sidebar selector filters by strategic line
- Indicator dropdown is dynamically filtered
- All visualizations respect this hierarchy

### 3. **Column Name Constants**

The codebase uses a `COL` dictionary for consistent column references:

```python
COL = {
    'id': 'Id',
    'indicador': 'Indicador',
    'proceso': 'Proceso',
    'periodicidad': 'Periodicidad',
    'sentido': 'Sentido',              # Up/Down preference
    'fecha': 'Fecha',
    'anio': 'Año',
    'mes': 'Mes',
    'periodo': 'Periodo',
    'semestre': 'Semestre',
    'meta': 'Meta',
    'ejecucion': 'Ejecución',
    'cumplimiento': 'Cumplimiento',
    'meta_sign': 'Meta s',              # Unit type (%, ENT, DEC, $)
    'ejec_sign': 'Ejecución s',
    'llave': 'Llave',
    'linea': 'Linea',                   # Strategic line
    'objetivo': 'Objetivo',
    'tipo_cierre': 'Tipo_Cierre',       # Cumulative/Average/Last
    'proyeccion': 'Proyección'
}
```

**⚠️ When writing queries or transformations, ALWAYS use Spanish column names as defined in COL!**

### 4. **Data Periodicity**

Indicators are tracked at different frequencies:

- **Semestral:** Most common (Jan-Jun = S1, Jul-Dec = S2)
- **Anual:** Year-end closures
- **Mensual:** Monthly tracking (less common)

**Closure Type Logic (Tipo_Cierre):**
- `'Cumulative'`: Sum of both semesters (e.g., total revenue)
- `'Average'`: Mean of both semesters (e.g., retention rate)
- `'Last'`: Use most recent semester value (e.g., current enrollment)

### 5. **Forecasting Model Selection**

Available models in Modelos.py:

```python
AVAILABLE_MODELS = [
    'Prophet',              # Facebook's time series model (best for seasonality)
    'ARIMA',                # AutoRegressive Integrated Moving Average
    'ETS',                  # Error-Trend-Seasonal
    'Holt-Winters',         # Exponential smoothing with seasonality
    'Random Forest',        # ML ensemble method
    'SVR',                  # Support Vector Regression
    'Linear Regression',    # Simple linear trends
    'Ensemble Ponderado',   # Weighted ensemble of models
    'Promedio de Modelos',  # Simple average of all models
    'Tendencia Histórica',  # Historical trend extrapolation
    'Crecimiento Histórico' # Historical growth rate projection
]
```

**Model Selection Heuristics:**
- **< 6 data points:** Use Linear Regression or Historical Trend only
- **6-12 data points:** Prophet, ARIMA, or ETS
- **> 12 data points:** Full model suite available
- **High volatility:** Use ensemble methods for stability
- **Strong seasonality:** Prefer Prophet or Holt-Winters

### 6. **Scenario Generation**

Three scenarios are automatically generated from base forecasts:

```python
SCENARIOS = {
    'Base': {
        'multiplier': 1.0,
        'description': 'Historical trend continuation'
    },
    'Optimista': {
        'multiplier': 1.15,  # +15% vs base (for positive indicators)
        'description': 'Favorable conditions, accelerated growth'
    },
    'Pesimista': {
        'multiplier': 0.85,  # -15% vs base (for positive indicators)
        'description': 'Conservative, risk-adjusted projections'
    }
}
```

**⚠️ Scenario logic respects indicator "sentido" (direction preference)!**
- For "up is better" indicators (e.g., revenue): Optimistic = higher values
- For "down is better" indicators (e.g., costs): Optimistic = lower values

---

## 🛠️ DEVELOPMENT WORKFLOWS

### Starting the Application

**Option 1: Dev Container (Recommended)**
```bash
# Open in VS Code with Dev Containers extension
# Automatically:
# 1. Builds Docker container with Python 3.11
# 2. Installs dependencies from requirements.txt
# 3. Starts Streamlit on http://localhost:8501
# 4. Opens preview in VS Code
```

**Option 2: Local Virtual Environment**
```bash
# Activate virtual environment
source Scripts/activate          # Linux/Mac
Scripts\activate.bat             # Windows

# Install dependencies
pip install -r requirements.txt

# Run main application
streamlit run app_streamlit.py --server.enableCORS false --server.enableXsrfProtection false
```

**Option 3: Presentation Mode**
```bash
streamlit run Presentacion.py
```

### Full Data Pipeline Execution

```bash
# Step 1: Extract and transform raw data
python ETL.py

# Step 2: Validate data consistency
python Validación.py

# Step 3: Generate forecasts (takes 5-15 minutes)
python Modelos.py

# Step 4: Launch interactive dashboard
streamlit run app_streamlit.py --server.enableCORS false --server.enableXsrfProtection false

# Optional: Generate PDF reports
python generar_informe_unificado.py
```

### Common Modifications

#### Adding a New Forecasting Model

**File:** `Modelos.py`

1. Import the model library
2. Create a `pronosticar_<model_name>()` function following this template:

```python
def pronosticar_nuevo_modelo(datos, periodos=10):
    """
    Forecast using New Model.

    Args:
        datos (pd.DataFrame): Historical data with ['Fecha', 'Ejecución']
        periodos (int): Number of future periods to forecast

    Returns:
        pd.DataFrame: Forecast with ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
    """
    try:
        # Prepare data
        X = datos[['Fecha']].values
        y = datos['Ejecución'].values

        # Train model
        model = NewModel()
        model.fit(X, y)

        # Generate forecast
        future_dates = pd.date_range(
            start=datos['Fecha'].max(),
            periods=periodos+1,
            freq='6MS'
        )[1:]

        predictions = model.predict(future_dates)

        # Format output
        forecast = pd.DataFrame({
            'ds': future_dates,
            'yhat': predictions,
            'yhat_lower': predictions * 0.95,  # Adjust confidence
            'yhat_upper': predictions * 1.05
        })

        return forecast

    except Exception as e:
        print(f"Error in nuevo_modelo: {str(e)}")
        return None
```

3. Add model to the main forecasting loop (search for "MODELOS DISPONIBLES")
4. Update UI in `app_streamlit.py` sidebar model selector

#### Adding a New Visualization to Dashboard

**File:** `app_streamlit.py`

1. Locate the visualization section (around lines 800-1200)
2. Add new Plotly figure:

```python
# ==============================
# NUEVA VISUALIZACIÓN
# ==============================
st.markdown("### 📊 Título de Nueva Visualización")

# Prepare data
df_viz = df_filtered.copy()

# Create Plotly figure
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_viz['Fecha'],
    y=df_viz['Ejecución'],
    mode='lines+markers',
    name='Histórico',
    line=dict(color='#2c5f8d', width=3),
    marker=dict(size=8)
))

# Layout
fig.update_layout(
    title="Título del Gráfico",
    xaxis_title="Eje X",
    yaxis_title="Eje Y",
    hovermode='x unified',
    template='plotly_white',
    height=500
)

st.plotly_chart(fig, use_container_width=True)
```

3. Add custom CSS styling if needed (lines 40-372)

#### Adding a New Data Validation Rule

**File:** `Validación.py`

1. Locate validation logic section
2. Add new check:

```python
# Nueva validación
def validar_nueva_regla(df, columna, condicion):
    """
    Validate new business rule.

    Args:
        df (pd.DataFrame): Data to validate
        columna (str): Column to check
        condicion: Validation condition

    Returns:
        pd.DataFrame: Rows that fail validation
    """
    fallos = df[df[columna] != condicion].copy()
    if len(fallos) > 0:
        print(f"⚠️ ALERTA: {len(fallos)} registros fallan la validación '{columna}'")
        print(fallos[[COL['id'], COL['indicador'], columna]])
    return fallos
```

3. Call validation in main ETL pipeline

---

## 🎨 CODE STYLE & PATTERNS

### UI/UX Conventions

**Color Palette (Institutional Branding):**
```python
COLORS = {
    'primary_dark': '#1e3a5f',      # Header, main titles
    'primary_medium': '#2c5f8d',    # Secondary elements
    'primary_light': '#4a90c8',     # Accents, highlights
    'background': '#f0f4f8',        # Main background
    'text': '#1e293b',              # Body text
    'success': '#10b981',           # Positive metrics
    'warning': '#f59e0b',           # Caution indicators
    'danger': '#ef4444',            # Negative metrics
    'gray': '#6b7280'               # Disabled/secondary text
}
```

**Typography:**
- **Font Family:** 'Poppins' (Google Fonts)
- **H1:** 2.5rem, weight 700 (page title)
- **H2:** 1.75rem, weight 600 (section headers)
- **H3:** 1.25rem, weight 600 (subsections)
- **Body:** 1rem, weight 400

**Streamlit Widgets:**
```python
# Standard selectbox pattern
selected_line = st.sidebar.selectbox(
    "🎯 Línea Estratégica",
    options=list(strategic_lines.keys()),
    format_func=lambda x: strategic_lines[x]
)

# Metric card pattern
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Valor Base 2025",
        value=f"{valor_2025:,.2f}",
        delta=None
    )
```

### Data Transformation Patterns

**Loading Excel Files:**
```python
# Standard Excel read pattern
df = pd.read_excel(
    "Data/Dataset_Unificado.xlsx",
    sheet_name="Unificado",
    parse_dates=['Fecha']
)

# Handle missing columns gracefully
required_columns = ['Id', 'Indicador', 'Fecha', 'Ejecución']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")
```

**Date Handling:**
```python
# Convert to datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Extract period components
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month
df['Semestre'] = df['Fecha'].dt.month.apply(lambda m: 1 if m <= 6 else 2)

# Generate future dates (semestral)
future_dates = pd.date_range(
    start=df['Fecha'].max(),
    periods=10,
    freq='6MS'  # 6 Month Start frequency
)
```

**Pivoting Data:**
```python
# Pivot from long to wide format
df_pivot = df.pivot_table(
    values='Ejecución',
    index='Id',
    columns='Fecha',
    aggfunc='first'
)
```

### Error Handling Patterns

**Forecasting Functions:**
```python
def pronosticar_modelo(datos, periodos=10):
    """Forecast with error handling."""
    try:
        # Validate minimum data points
        if len(datos) < MIN_DATA_POINTS:
            print(f"⚠️ Insufficient data: {len(datos)} < {MIN_DATA_POINTS}")
            return None

        # Core forecasting logic
        forecast = model.predict(...)

        # Validate output
        if forecast is None or len(forecast) == 0:
            print("⚠️ Model returned empty forecast")
            return None

        return forecast

    except Exception as e:
        print(f"❌ Error in pronosticar_modelo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
```

**UI Data Loading:**
```python
@st.cache_data
def load_data(file_path):
    """Load and cache data with error handling."""
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return pd.DataFrame()
```

---

## 🚨 COMMON PITFALLS & SOLUTIONS

### 1. **Hard-coded Windows Paths**

**Problem:**
```python
# WRONG - Hard-coded Windows path in Modelos.py
INPUT_FILE = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Modelo_Prospectivo\Data\Dataset_Unificado.xlsx"
```

**Solution:**
```python
# RIGHT - Use pathlib for cross-platform paths
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "Data" / "Dataset_Unificado.xlsx"
```

**Files to check:** Modelos.py (lines 73-74), generar_informe_unificado.py

### 2. **Missing Data Handling**

**Problem:** Forecasting models crash when indicators have insufficient historical data.

**Solution:**
```python
# Check data availability before forecasting
MIN_DATA_POINTS = 6  # Defined in Modelos.py

if len(df_indicador) < MIN_DATA_POINTS:
    st.warning(f"⚠️ Indicador tiene solo {len(df_indicador)} puntos. Mínimo: {MIN_DATA_POINTS}")
    # Use fallback: historical trend or skip
```

### 3. **Outlier Detection Too Aggressive**

**Problem:** Strong legitimate growth trends (e.g., 50% year-over-year) flagged as outliers.

**Solution (already implemented in Modelos.py):**
```python
OUTLIER_THRESHOLD = 3.5  # Increased from 2.5 to be more tolerant

# Use weighted z-score with higher weight on recent data
RECENT_WEIGHT = 0.8
```

### 4. **Excel File Locking**

**Problem:** "Permission denied" errors when writing Excel files while they're open.

**Solution:**
```python
import os
import time

# Close file before writing
output_file = "Proyecciones/output.xlsx"

# Retry logic for file operations
max_retries = 3
for attempt in range(max_retries):
    try:
        df.to_excel(output_file, index=False)
        break
    except PermissionError:
        if attempt < max_retries - 1:
            print(f"⚠️ Archivo bloqueado. Reintentando en 2s... ({attempt+1}/{max_retries})")
            time.sleep(2)
        else:
            print(f"❌ No se pudo guardar. Cierre el archivo: {output_file}")
```

### 5. **Streamlit Caching Issues**

**Problem:** Old data persists after updating Excel files.

**Solution:**
```python
# Use @st.cache_data with TTL for data that may change
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_data(file_path):
    return pd.read_excel(file_path)

# Or manually clear cache in sidebar
if st.sidebar.button("🔄 Recargar Datos"):
    st.cache_data.clear()
    st.rerun()
```

### 6. **Indicator Type Misclassification**

**Problem:** Currency values treated as percentages, leading to wrong validation limits.

**Solution:**
```python
# Always verify indicator type detection
def detectar_tipo_indicador(meta_value, valores_historicos=None):
    """
    Detect indicator type with fallbacks.
    Priority: Meta column → Historical values → DEFAULT
    """
    if pd.notna(meta_value):
        tipo = str(meta_value).strip().upper()
        if tipo in ['%', 'ENT', 'DEC', '$']:
            return tipo

    # Fallback: Analyze historical values
    if valores_historicos is not None and len(valores_historicos) > 0:
        max_val = valores_historicos.max()
        if 0 <= max_val <= 100:
            return '%'
        elif all(valores_historicos == valores_historicos.astype(int)):
            return 'ENT'

    return 'DEFAULT'
```

---

## 🧪 TESTING & VALIDATION

### Current Testing Approach

**⚠️ No automated tests currently exist.**

Testing is done through:
1. **Manual validation** via `Validación.py`
2. **Visual inspection** of dashboard charts
3. **Excel output review** in `/Proyecciones/`
4. **Data consistency checks** (closure calculations)

### Recommended Testing Strategy

**Unit Tests to Add:**

```python
# tests/test_modelos.py
import pytest
from Modelos import detectar_tipo_indicador, validar_proyeccion_realista

def test_detectar_tipo_indicador_porcentaje():
    """Test that percentages are correctly detected."""
    valores = pd.Series([45.2, 67.8, 89.1, 92.3])
    tipo = detectar_tipo_indicador('%', valores)
    assert tipo == '%'

def test_validar_proyeccion_realista_rechaza_extremos():
    """Test that extreme projections are rejected."""
    ultimo_valor = 100
    proyeccion = 500  # 400% growth
    tipo = 'ENT'

    es_valida = validar_proyeccion_realista(
        proyeccion,
        ultimo_valor,
        tipo
    )
    assert es_valida == False, "Should reject 400% growth"

def test_pronosticar_con_datos_insuficientes():
    """Test that forecasting handles insufficient data gracefully."""
    datos = pd.DataFrame({
        'Fecha': pd.date_range('2024-01-01', periods=3, freq='6MS'),
        'Ejecución': [100, 110, 120]
    })

    forecast = pronosticar_prophet(datos, periodos=10)
    assert forecast is None, "Should return None with < 6 data points"
```

**Integration Tests:**

```python
# tests/test_etl.py
def test_etl_pipeline_completo():
    """Test full ETL pipeline from raw to unified data."""
    # Run ETL
    import ETL

    # Verify output exists
    assert os.path.exists("Datos_Unificados.xlsx")

    # Load and validate
    df = pd.read_excel("Datos_Unificados.xlsx")
    assert 'Id' in df.columns
    assert 'Indicador' in df.columns
    assert len(df) > 0
```

### Manual Testing Checklist

Before committing changes, verify:

- [ ] **Data Loading:** All Excel files load without errors
- [ ] **Strategic Lines:** All 6 lines appear in sidebar
- [ ] **Indicator Filtering:** Selecting a line filters indicators correctly
- [ ] **Model Selection:** All 11+ models are selectable
- [ ] **Scenario Generation:** Base, Optimistic, Pessimistic all display
- [ ] **Charts Render:** Plotly visualizations load without errors
- [ ] **Date Ranges:** Historical and forecast periods are correct
- [ ] **Data Export:** CSV download works
- [ ] **Responsive Design:** UI adapts to different screen sizes
- [ ] **Error Handling:** Missing data shows user-friendly warnings

---

## 📊 DATA STRUCTURES & SCHEMAS

### Input Data Schema (Dataset_Unificado.xlsx)

**Sheet: "Unificado"**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Id | int | Unique indicator ID | 101 |
| Indicador | str | Indicator name | "Matrícula Total" |
| Proceso | str | Business process | "Admisiones" |
| Linea | str | Strategic line (1-6) | "Expansión" |
| Objetivo | str | Strategic objective | "Aumentar cobertura" |
| Periodicidad | str | Frequency | "Semestral", "Anual" |
| Fecha | datetime | Period date | 2024-06-30 |
| Año | int | Year | 2024 |
| Semestre | int | Semester (1 or 2) | 1 |
| Meta | str | Indicator type | "%", "ENT", "DEC", "$" |
| Ejecución | float | Actual value | 45678.50 |
| Cumplimiento | float | Compliance % | 98.2 |
| Tipo_Cierre | str | Closure type | "Cumulative", "Average", "Last" |

### Output Data Schema (Proyecciones_Multimodelo.xlsx)

**Sheet: "Proyecciones"**

| Column | Type | Description |
|--------|------|-------------|
| Id | int | Indicator ID (links to input) |
| Indicador | str | Indicator name |
| Modelo | str | ML model used |
| Escenario | str | "Base", "Optimista", "Pesimista" |
| Fecha_Proyeccion | datetime | Future date |
| Año | int | Projected year |
| Semestre | int | Projected semester |
| Valor_Proyectado | float | Forecast value |
| Limite_Inferior | float | Lower confidence bound |
| Limite_Superior | float | Upper confidence bound |
| Fecha_Generacion | datetime | When forecast was created |

### Database Schema (proyecciones.db - SQLite)

**Table: proyecciones**

```sql
CREATE TABLE proyecciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicador_id INTEGER NOT NULL,
    indicador_nombre TEXT NOT NULL,
    modelo TEXT NOT NULL,
    escenario TEXT NOT NULL,
    fecha_proyeccion DATE NOT NULL,
    valor_proyectado REAL NOT NULL,
    limite_inferior REAL,
    limite_superior REAL,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(indicador_id, modelo, escenario, fecha_proyeccion)
);
```

---

## 🔧 DEPENDENCIES & PACKAGE MANAGEMENT

### Critical Dependencies

**DO NOT UPGRADE** without testing thoroughly:
- `xgboost>=1.7.0` - Breaking changes in earlier versions
- `python-pptx>=0.6.21` - Presentation generation compatibility
- `prophet` - Can be finicky with pandas versions
- `statsmodels` - ARIMA API changed significantly across versions

### Installing New Dependencies

```bash
# 1. Activate virtual environment
source Scripts/activate

# 2. Install package
pip install new-package

# 3. Update requirements.txt
pip freeze > requirements.txt

# 4. Test thoroughly
streamlit run app_streamlit.py

# 5. Update CLAUDE.md if package adds new conventions
```

### Dependency Conflicts

**Common Issue:** Prophet + Pandas version mismatch

```bash
# Solution: Pin compatible versions
pip install prophet==1.1.1 pandas==1.5.3
```

---

## 🚀 DEPLOYMENT NOTES

### Current Deployment: Dev Container

The application is designed for **local/team deployment** via VS Code Dev Containers:

1. **Open repository in VS Code**
2. **Install "Dev Containers" extension**
3. **Click "Reopen in Container"**
4. **Auto-starts on:** http://localhost:8501

### Production Deployment (Not Configured)

To deploy to production, you would need to:

1. **Configure Streamlit Cloud** (recommended) or **Docker deployment**
2. **Set environment variables** for file paths
3. **Add authentication** (Streamlit doesn't have built-in auth)
4. **Enable HTTPS** and CSRF protection (currently disabled)
5. **Set up database** for multi-user concurrent access
6. **Implement caching strategy** for large Excel files

**Security Warnings:**
```python
# Currently DISABLED for development:
--server.enableCORS false           # ⚠️ Re-enable for production
--server.enableXsrfProtection false # ⚠️ Re-enable for production
```

---

## 📝 GIT WORKFLOW

### Branch Strategy

**Development Branch:**
```
claude/claude-md-mhzedm36f0rt8izy-019784XCs2QdiFnnnrFCsddh
```

### Commit Guidelines

```bash
# Make changes
git add <files>

# Commit with descriptive message
git commit -m "feat: Add new forecasting model for XYZ
- Implement Seasonal ARIMA (SARIMA) in Modelos.py
- Add SARIMA option to app_streamlit.py sidebar
- Update requirements.txt with seasonal dependencies"

# Push to development branch
git push -u origin claude/claude-md-mhzedm36f0rt8izy-019784XCs2QdiFnnnrFCsddh
```

### Commit Message Conventions

- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring (no behavior change)
- `docs:` Documentation updates
- `style:` Formatting, CSS changes
- `test:` Adding tests
- `chore:` Maintenance (dependencies, build config)

---

## 🤖 AI ASSISTANT BEST PRACTICES

### When Modifying Code

1. **Always read the file first** before editing
2. **Respect existing patterns** (e.g., COL dictionary for column names)
3. **Test changes locally** before committing
4. **Update CLAUDE.md** if you introduce new conventions
5. **Check both app_streamlit.py AND Modelos.py** for related changes

### When Adding Features

1. **Check if similar functionality exists** (avoid duplication)
2. **Follow indicator type system** for validation
3. **Use Plotly for visualizations** (consistent with existing charts)
4. **Add user-facing messages** in Spanish (UI language)
5. **Test with different strategic lines** and scenarios

### When Debugging

1. **Check Excel files first** - Most issues stem from data format
2. **Look for hard-coded paths** - Windows vs Linux compatibility
3. **Verify indicator types** - Wrong type = wrong validation
4. **Clear Streamlit cache** - Use st.cache_data.clear()
5. **Check console output** - Many errors print to terminal

### Communication with Users

- **Use Spanish** for user-facing messages (UI language)
- **Use English** for code comments and technical docs
- **Be specific** about indicator names and strategic lines
- **Show data** when discussing changes (e.g., "Indicator 'Matrícula Total' in line 'Expansión'")

---

## 📞 GETTING HELP

### Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Prophet Docs:** https://facebook.github.io/prophet/
- **Plotly Python:** https://plotly.com/python/
- **Pandas API:** https://pandas.pydata.org/docs/

### Common Questions

**Q: Where is the main entry point?**
A: `app_streamlit.py` - Run with `streamlit run app_streamlit.py`

**Q: How do I add a new indicator?**
A: Add rows to `Data/Dataset_Unificado.xlsx` with proper columns (Id, Indicador, Meta, etc.)

**Q: Forecasts look wrong. What should I check?**
A:
1. Verify indicator type in 'Meta' column
2. Check for outliers in historical data
3. Review min/max limits in `LIMITES_POR_TIPO`
4. Ensure sufficient historical data points (MIN_DATA_POINTS = 6)

**Q: How do I change the institutional logo?**
A: Replace `Wallpaper-POLI.jpg` with new image (same filename)

**Q: Can I deploy this to Streamlit Cloud?**
A: Yes, but you'll need to:
- Fix hard-coded file paths
- Add secrets management for database
- Re-enable CORS and CSRF protection

---

## 📅 MAINTENANCE SCHEDULE

### Regular Tasks

**Weekly:**
- [ ] Update `Data/Dataset_Unificado.xlsx` with new semester data
- [ ] Run `Validación.py` to check data consistency
- [ ] Review dashboard for anomalies

**Monthly:**
- [ ] Regenerate forecasts with `Modelos.py`
- [ ] Export updated projections to `/Proyecciones/`
- [ ] Generate PDF reports with `generar_informe_unificado.py`

**Quarterly:**
- [ ] Review model performance against actuals
- [ ] Adjust `LIMITES_POR_TIPO` if needed
- [ ] Update presentation slides in `/Slides/`

**Annually:**
- [ ] Update strategic objectives and goals
- [ ] Review and update indicator catalog
- [ ] Upgrade dependencies (carefully!)

---

## 🎓 LEARNING THE CODEBASE

### Recommended Reading Order

1. **Start with:** `app_streamlit.py` (lines 1-200) - Configuration and setup
2. **Then read:** `Modelos.py` (lines 1-100) - Configuration and type system
3. **Explore:** `ETL.py` - Data pipeline
4. **Study:** `app_streamlit.py` visualization sections - Plotly patterns
5. **Deep dive:** `Modelos.py` forecasting functions - ML implementations

### Key Concepts to Understand

1. **Indicator Type System** - Drives all validation and forecasting
2. **Strategic Lines** - Organizational structure for indicators
3. **Scenario Generation** - How optimistic/pessimistic are calculated
4. **Closure Types** - Cumulative vs Average vs Last value logic
5. **Model Ensembling** - How multiple forecasts are combined

---

## 🔒 SECURITY & DATA PRIVACY

### Sensitive Data

**This repository contains:**
- Institutional performance data
- Strategic planning information
- Financial metrics (EBITDA, revenue)

**⚠️ DO NOT:**
- Commit Excel files to public repositories
- Share proyecciones.db publicly
- Expose Streamlit dashboard to internet without authentication

### Access Control

**Current State:** No authentication (local use only)

**For Production:** Implement one of:
- Streamlit Cloud authentication
- OAuth2 integration
- Basic auth with streamlit-authenticator
- VPN-only access

---

## ✅ QUICK REFERENCE CHECKLIST

### Before Committing Code

- [ ] Tested locally with `streamlit run app_streamlit.py`
- [ ] No hard-coded Windows paths
- [ ] Spanish used for user-facing messages
- [ ] Code follows existing patterns (COL dictionary, etc.)
- [ ] Indicator type system respected
- [ ] Error handling added for new functions
- [ ] No sensitive data in commit
- [ ] CLAUDE.md updated if new conventions added

### Before Pushing to Production

- [ ] All tests pass (when tests exist)
- [ ] Validation.py runs without errors
- [ ] Excel outputs look correct
- [ ] Dashboard loads without crashes
- [ ] All 6 strategic lines work
- [ ] All scenarios generate properly
- [ ] Performance is acceptable (< 5 sec load time)
- [ ] Mobile responsiveness checked

---

**Last Updated:** 2025-11-14
**Maintained By:** AI Assistant (Claude)
**Version:** 1.0

---

_This document is a living guide. Update it whenever you introduce new patterns, conventions, or architectural changes._
