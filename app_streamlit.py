import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors
import random
from pathlib import Path


# ==============================
# CONFIGURACIÓN STREAMLIT
# ==============================
st.set_page_config(
    page_title="Modelo Prospectivo Poli 2026-2030",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración del tema personalizado
st.markdown("""
    <style>
        /* Importar fuentes */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* Estilo general */
        * {
            font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main {
            background-color: #f5f8ff !important;
            color: #2c3e50;
            line-height: 1.6;
        }
        
        /* Fondo de la aplicación */
        .stApp {
            background-color: #f5f8ff !important;
        }
        
        /* Contenedor principal */
        .main .block-container {
            padding: 1.5rem 2.5rem;
            max-width: 1600px;
            background-color: transparent;
        }
        
        /* Secciones */
        .stContainer {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        
        /* Títulos */
        h1 {
            color: #0F385A;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0 0 1.5rem 0;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding-bottom: 1rem;
            border-bottom: 3px solid #1a73e8;
            background: linear-gradient(135deg, #0F385A 0%, #1a73e8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        h2 {
            color: #1a3d6d;
            font-size: 1.75rem;
            font-weight: 700;
            margin: 2rem 0 1.25rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e2e8f0;
            position: relative;
        }
        
        h2:after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -2px;
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, #1a73e8, #34a853);
            border-radius: 2px;
        }
        
        h3 {
            color: #2c5282;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 1.75rem 0 1rem 0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0f2d5f !important;  /* Azul oscuro institucional */
            color: white !important;
            padding: 1.5rem 1.25rem;
            box-shadow: 4px 0 20px rgba(0,0,0,0.1);
        }
        
        /* Texto en sidebar */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            color: rgba(255,255,255,0.9) !important;
        }
        
        /* Títulos en sidebar */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white !important;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            padding-bottom: 0.75rem;
            margin-bottom: 1.25rem;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #0F385A;
            font-weight: 700;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e2e8f0;
        }
        
        /* Botones */
        .stButton > button {
            background: linear-gradient(135deg, #1e88e5 0%, #0d47a1 100%);
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 0.8rem 1.75rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
            width: 100%;
            margin: 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.5s ease, height 0.5s ease;
        }
        
        .stButton > button:hover::after {
            width: 200px;
            height: 200px;
            opacity: 0;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(30, 136, 229, 0.4);
            background: linear-gradient(135deg, #2196f3 0%, #1565c0 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 6px rgba(26, 115, 232, 0.3);
        }
        
        /* Controles de formulario */
        .stSelectbox, .stTextInput, .stNumberInput, .stDateInput, .stCheckbox {
            margin: 0.75rem 0 1.25rem;
            font-size: 0.95rem;
        }
        
        /* Selectores */
        .stSelectbox > div, .stTextInput > div, .stNumberInput > div, .stDateInput > div {
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            background-color: #ffffff;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        
        .stSelectbox > div:hover, .stTextInput > div:hover, 
        .stNumberInput > div:hover, .stDateInput > div:hover {
            border-color: #90cdf4;
            box-shadow: 0 0 0 3px rgba(144, 205, 244, 0.2);
        }
        
        .stSelectbox > div:focus-within, .stTextInput > div:focus-within, 
        .stNumberInput > div:focus-within, .stDateInput > div:focus-within {
            border-color: #1a73e8;
            box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.2);
        }
        
        /* Checkboxes */
        .stCheckbox {
            color: #2d3748;
            font-size: 0.95rem;
            margin: 1rem 0;
        }
        
        .stCheckbox > label {
            cursor: pointer;
            padding: 0.5rem 0.5rem 0.5rem 0;
            display: flex;
            align-items: center;
            transition: all 0.2s;
            border-radius: 6px;
            margin: 0.25rem 0;
        }
        
        .stCheckbox > label:hover {
            background-color: #f7fafc;
            transform: translateX(2px);
        }
        
        .stCheckbox > label > div:first-child {
            margin-right: 0.75rem;
            border-radius: 4px;
            border: 1px solid #cbd5e0;
        }
        
        .stCheckbox > label > div[data-baseweb="checkbox"] {
            background-color: #1a73e8;
            border-color: #1a73e8;
        }
        
        /* Pestañas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            margin: 2rem 0 1.5rem 0;
            border-bottom: 2px solid #e3f2fd;
            padding-bottom: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #f8fafc;
            border-radius: 8px 8px 0 0;
            padding: 0.85rem 1.75rem;
            margin: 0 4px 0 0;
            font-weight: 500;
            color: #546e7a;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            position: relative;
            bottom: 0;
            font-size: 0.95rem;
            letter-spacing: 0.3px;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e2e8f0;
            color: #334155;
        }
        
        .stTabs [aria-selected="true"] {
            background: #1e88e5;
            color: white !important;
            font-weight: 600;
            border: none;
            box-shadow: 0 -4px 0 #0d47a1 inset, 0 4px 12px rgba(30, 136, 229, 0.2);
            transform: translateY(-1px);
        }
        
        /* Tarjetas y métricas */
        .stMetric {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-left: 4px solid #1a73e8;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin: 0.75rem 0;
            border: 1px solid #e2e8f0;
        }
        
        .stMetric:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-left-color: #1557b0;
        }
        
        .stMetric > div {
            margin: 0;
        }
        
        .stMetric > div > div:first-child {
            color: #4a5568;
            font-size: 0.95rem;
            font-weight: 500;
            letter-spacing: 0.3px;
        }
        
        .stMetric > div > div:last-child {
            color: #1a365d;
            font-size: 1.75rem;
            font-weight: 700;
            margin-top: 0.5rem;
        }
        
        /* Gráficos */
        .stPlotlyChart {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            background: white;
        }
        
        /* Tooltips */
        .stTooltip {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 0.9rem;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            background: white;
            max-width: 300px;
        }
        
        /* Secciones colapsables */
        .stExpander {
            background: #ffffff;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 1rem 0;
            overflow: hidden;
        }
        
        .stExpander > label {
            padding: 1rem 1.5rem;
            font-weight: 600;
            color: #2d3748;
            background-color: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .stExpander > div[data-testid="stExpanderContent"] {
            padding: 1.5rem;
        }
        
        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a0aec0;
        }
    </style>
""", unsafe_allow_html=True)


# Encabezado principal
st.markdown("""
<div style="text-align: center; margin: 0 0 2.5rem 0; padding: 3.5rem 2rem; background: linear-gradient(135deg, #0f2d5f 0%, #1e88e5 100%); border-radius: 12px; box-shadow: 0 10px 25px rgba(15, 45, 95, 0.2); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkZWZzPjxwYXR0ZXJuIGlkPSJwYXR0ZXJuIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgcGF0dGVyblRyYW5zZm9ybT0icm90YXRlKDQ1KSI+PHJlY3Qgd2lkdGg9IjUwJSIgaGVpZ2h0PSI1MCUiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wMykiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjcGF0dGVybikiLz48L3N2Zz4=');"></div>
    <h1 style="color: white; font-size: 2.75rem; font-weight: 800; margin: 0 0 0.75rem 0; letter-spacing: -0.5px; text-transform: uppercase; position: relative; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        MODELO DE PROSPECTIVA POLI
    </h1>
    <div style="height: 6px; width: 180px; background: linear-gradient(90deg, rgba(255,255,255,0.8), #ffffff); margin: 0 auto 1.25rem; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.15rem; margin: 0; font-weight: 400; max-width: 800px; margin: 0 auto; line-height: 1.6; position: relative; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">
        Plataforma de análisis y proyección de indicadores estratégicos 2026-2030
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# LECTURA DE DATOS REALES
# ==============================
# Usar pathlib para rutas multiplataforma
BASE_DIR = Path(__file__).parent
RUTA_DATASET = str(BASE_DIR / "Data" / "Dataset_Unificado.xlsx")
RUTA_PROYECCIONES = str(BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx")

# Datos históricos
df_hist = pd.read_excel(RUTA_DATASET)
df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"])

# Proyecciones (2026-2030) - Nueva estructura
df_proj_raw = pd.read_excel(RUTA_PROYECCIONES)
df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"])

# Transformar la estructura de datos para compatibilidad
# Convertir las columnas de escenarios en filas
df_proj_list = []
if not df_proj_raw.empty:
    for _, row in df_proj_raw.iterrows():
        base_data = {
            'Indicador': row['Indicador'],
            'Periodicidad': row.get('Periodicidad', 'Semestral'),
            'Fecha': row['Fecha_Proyeccion'],
            'Modelo': row['Modelo']
        }
        
        # Agregar cada escenario como una fila separada
        if pd.notna(row.get('Escenario_Base')):
            df_proj_list.append({**base_data, 'Escenario': 'Base', 'Proyección': row['Escenario_Base']})
        if pd.notna(row.get('Escenario_Pesimista')):
            df_proj_list.append({**base_data, 'Escenario': 'Pesimista', 'Proyección': row['Escenario_Pesimista']})
        if pd.notna(row.get('Escenario_Optimista')):
            df_proj_list.append({**base_data, 'Escenario': 'Optimista', 'Proyección': row['Escenario_Optimista']})

df_proj = pd.DataFrame(df_proj_list) if df_proj_list else pd.DataFrame()


# ==============================
# SIDEBAR - CONTROLES
# ==============================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #0F385A; font-size: 1.5rem; font-weight: 600; margin: 0;">
            ⚙️ CONTROLES DE ESCENARIO
        </h2>
        <div style="height: 3px; background: linear-gradient(90deg, #1a73e8, #34a853, #ea4335); margin: 0.5rem auto; width: 80%; border-radius: 3px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Líneas Estratégicas con colores en tonos azules profesionales
    lineas_estrategicas = {
        "Expansión": ("Expansión", "#1a73e8"),
        "Transformación Organizacional": ("Transformación_Organizacional", "#4285f4"), 
        "Calidad": ("Calidad", "#5c8bf2"),
        "Experiencia": ("Experiencia", "#7ea7f7"),
        "Sostenibilidad": ("Sostenibilidad", "#a0bff5"),
        "Educación para la vida": ("Educación_para_toda_la_vida", "#0d47a1")
    }

    linea_sel = st.selectbox(
        "🎯 Línea Estratégica", 
        list(lineas_estrategicas.keys()),
        help="Selecciona la línea estratégica"
    )

    # Obtener el nombre real de la línea y su color
    display_name, color_linea = lineas_estrategicas[linea_sel]
    
    # Filtrar indicadores por línea estratégica seleccionada
    if 'Linea' in df_hist.columns:
        # Filtrar por el nombre exacto de la línea
        df_hist_filtrado = df_hist[df_hist["Linea"] == display_name]
        
        # Si no hay coincidencias, intentar con el nombre mostrado (sin guiones)
        if df_hist_filtrado.empty:
            df_hist_filtrado = df_hist[df_hist["Linea"].str.replace('_', ' ') == linea_sel]
        
        # Si aún no hay coincidencias, mostrar todos los indicadores
        if df_hist_filtrado.empty:
            df_hist_filtrado = df_hist
        
        indicadores = sorted(df_hist_filtrado["Indicador"].unique())
    else:
        indicadores = sorted(df_hist["Indicador"].unique())
    
    indicador_sel = st.selectbox("Selecciona un Indicador", indicadores, key="selector_indicador")
    # Obtener todos los modelos disponibles (incluyendo ARIMA)
    modelos = sorted(df_proj["Modelo"].unique()) if not df_proj.empty else []
    
    if not modelos:
        st.error("⚠️ No se encontraron modelos en el archivo de proyecciones. Verifica la estructura del archivo Excel.")
        st.stop()
    
    # Mapeo de nombres de modelos para mejor visualización
    modelo_display_names = {
        'ARIMA': '📊 ARIMA',
        'Random_Forest': '🌳 Random Forest',
        'SVR': '🎯 Support Vector Regression',
        'Linear_Regression': '📈 Regresión Lineal',
        'Prophet': '🔮 Prophet',
        'Crecimiento_Historico': '📜 Crecimiento Histórico'
    }
    
    # Crear lista de opciones con nombres mejorados
    modelo_options = [modelo_display_names.get(m, m) for m in modelos]
    modelo_display_sel = st.selectbox("🧠 Modelo ML", modelo_options, help="Selecciona el modelo de Machine Learning para las proyecciones")
    
    # Obtener el nombre real del modelo seleccionado
    modelo_sel = next((k for k, v in modelo_display_names.items() if v == modelo_display_sel), modelo_display_sel)

    # Filtrar escenarios por modelo seleccionado
    escenarios_disponibles = ['Base', 'Pesimista', 'Optimista']
    if not df_proj.empty and modelo_sel in df_proj["Modelo"].unique():
        escenarios_modelo = df_proj[df_proj["Modelo"] == modelo_sel]["Escenario"].unique()
        escenarios_disponibles = [e for e in escenarios_disponibles if e in escenarios_modelo]
    
    if not escenarios_disponibles:
        st.warning(f"⚠️ No se encontraron escenarios para el modelo {modelo_sel}")
        escenarios_sel = []
    else:
        st.write("🌍 **Selecciona Escenarios:**")
        
        # Mapeo de iconos para escenarios
        escenario_icons = {
            'Base': '⚖️',
            'Pesimista': '📉',
            'Optimista': '📈'
        }
        
        # Crear checkboxes para cada escenario
        escenarios_sel = []
        for escenario in escenarios_disponibles:
            icon = escenario_icons.get(escenario, '🌍')
            default_value = escenario in ['Base', 'Optimista']  # Seleccionar Base y Optimista por defecto
            if st.checkbox(f"{icon} {escenario}", value=default_value, key=f"escenario_{escenario}"):
                escenarios_sel.append(escenario)

    # Botón para refrescar (si hay randomización futura)
    if st.button("🔄 Refrescar"):
        st.rerun()
    
    # ==============================
    # CONFIGURACIÓN DEL GRÁFICO
    # ==============================
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1rem 0;">
        <h3 style="color: #0F385A; font-size: 1.25rem; font-weight: 600; margin: 0;">
            📊 CONFIGURACIÓN DEL GRÁFICO
        </h3>
        <div style="height: 2px; background: linear-gradient(90deg, #1a73e8, #34a853); margin: 0.5rem auto; width: 70%; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tipo de visualización
    tipo_visualizacion = st.selectbox(
        "📈 Tipo de Visualización",
        ["Semestral", "Anual"],
        help="Selecciona qué datos mostrar en el gráfico"
    )
    
    # Tipo de gráfico
    tipo_grafico = st.selectbox(
        "📊 Tipo de Gráfico",
        ["Línea", "Barras", "Dispersión"],
        help="Selecciona el tipo de visualización"
    )
    
    # Mostrar números en el gráfico
    mostrar_numeros = st.checkbox("🔢 Mostrar números en el gráfico", value=True)
    
    # Mostrar línea divisoria
    mostrar_linea_divisoria = st.checkbox("📏 Mostrar línea divisoria", value=True)

# ==============================
# FILTRAR DATOS SEGÚN SELECCIÓN
# ==============================
# Histórico del indicador
if 'Linea' in df_hist.columns:
    # Usar el display_name que ya tiene el formato correcto para la base de datos
    df_hist_sel = df_hist[
        (df_hist["Indicador"] == indicador_sel) &
        (df_hist["Linea"] == display_name)
    ]
    
    # Si no hay coincidencias, intentar con el nombre mostrado (sin guiones)
    if df_hist_sel.empty:
        df_hist_sel = df_hist[
            (df_hist["Indicador"] == indicador_sel) &
            (df_hist["Linea"].str.replace('_', ' ') == linea_sel)
        ]
else:
    df_hist_sel = df_hist[df_hist["Indicador"] == indicador_sel]

# Proyección del indicador (múltiples escenarios)
df_proj_sel = df_proj[
    (df_proj["Indicador"] == indicador_sel) &
    (df_proj["Modelo"] == modelo_sel) &
    (df_proj["Escenario"].isin(escenarios_sel))
]

# ==============================
# KPIs PRINCIPALES (valores 2030 por escenario)
# ==============================
# Mostrar línea estratégica seleccionada con su color
st.markdown(f"""
<div style="background: {color_linea};
            padding: 1.25rem 1.5rem; 
            border-radius: 8px; 
            margin: 1.5rem 0 2rem 0; 
            text-align: left;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-left: 5px solid darken({color_linea}, 10%);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 1rem;">
    <div style="font-size: 1.8rem;">🎯</div>
    <div>
        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem;">LÍNEA ESTRATÉGICA</div>
        <h3 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 700; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">
            {linea_sel}
        </h3>
    </div>
</div>
""", unsafe_allow_html=True)

# Estilo personalizado para las métricas
st.markdown("""
<style>
    .metric-container {
        display: flex;
        flex-direction: column;
        background: #ffffff;
        border-radius: 10px;
        padding: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: #4361ee;
    }
    .metric-title {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #1e293b;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
</style>
""", unsafe_allow_html=True)

# Crear columnas para las métricas
col1, col2, col3 = st.columns(3)

# Métrica 1: Modelo seleccionado
with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-icon">📊</div>
        <div class="metric-title">Modelo Seleccionado</div>
        <div class="metric-value">{modelo_sel}</div>
    </div>
    """, unsafe_allow_html=True)

# Métrica 2: Escenarios activos
with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-icon">🌍</div>
        <div class="metric-title">Escenarios Activos</div>
        <div class="metric-value">{len(escenarios_sel)}</div>
    </div>
    """, unsafe_allow_html=True)

# Métrica 3: Promedio 2030
with col3:
    if not df_proj_sel.empty and len(escenarios_sel) > 0:
        df2030 = df_proj_sel[df_proj_sel["Fecha"].dt.year == 2030]
        if not df2030.empty:
            valor_promedio_2030 = df2030["Proyección"].mean()
            valor_formateado = f"{valor_promedio_2030:,.0f}"
        else:
            valor_formateado = "N/A"
    else:
        valor_formateado = "N/A"
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-icon">📌</div>
        <div class="metric-title">Promedio 2030</div>
        <div class="metric-value">{valor_formateado}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# GRÁFICO PRINCIPAL
# ==============================
st.subheader(f"📊 Evolución del Indicador: {indicador_sel}")

fig = go.Figure()

# Separar datos históricos por fuente usando las columnas correctas
df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"]  # Datos semestrales
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"]         # Datos anuales (cierre)

# Configuración avanzada
with st.expander("⚙️ Configuración Avanzada"):
    st.write(f"**Tipo de Visualización:** {tipo_visualizacion}")
    st.info("Ajusta la configuración avanzada del gráfico según tus necesidades.")
    st.write(f"**Tipo de Gráfico:** {tipo_grafico}")
    st.write(f"**Mostrar Números:** {mostrar_numeros}")
    st.write(f"**Mostrar Línea Divisoria:** {mostrar_linea_divisoria}")
    
    st.write("**Columnas disponibles en datos históricos:**")
    st.write(df_hist_sel.columns.tolist())
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Datos Históricos:**")
        st.write(f"- Total: {len(df_hist_sel)} registros")
        st.write(f"- Semestrales (Fuente='Semestral'): {len(df_hist_semestral)} registros")
        st.write(f"- Anuales (Fuente='Cierre'): {len(df_hist_anual)} registros")
        
        if not df_hist_semestral.empty:
            st.write("**Semestrales por semestre:**")
            df_s1 = df_hist_semestral[df_hist_semestral["Semestre"] == 1]
            df_s2 = df_hist_semestral[df_hist_semestral["Semestre"] == 2]
            st.write(f"- Semestre 1: {len(df_s1)} registros")
            st.write(f"- Semestre 2: {len(df_s2)} registros")
        
        if not df_hist_sel.empty:
            st.write("**Fuentes disponibles:**")
            fuentes = df_hist_sel["Fuente"].unique()
            st.write(fuentes.tolist())
        
        if not df_hist_semestral.empty:
            st.write("**Fechas Semestrales:**")
            st.write(df_hist_semestral["Fecha"].dt.strftime("%Y-%m").tolist())
        
        if not df_hist_anual.empty:
            st.write("**Fechas Anuales:**")
            st.write(df_hist_anual["Fecha"].dt.strftime("%Y-%m").tolist())
    
    with col2:
        st.write("**Datos Proyectados:**")
        st.write(f"- Total: {len(df_proj_sel)} registros")
        
        for escenario in escenarios_sel:
            df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
            if not df_esc.empty:
                df_s1 = df_esc[df_esc["Fecha"].dt.month == 6]
                df_s2 = df_esc[df_esc["Fecha"].dt.month == 12]
                st.write(f"- {escenario}: {len(df_esc)} total, {len(df_s1)} S1, {len(df_s2)} S2")

# Función para agregar trazas según el tipo de gráfico
def format_number(value, decimal_places):
    """Formatea un número según la cantidad de decimales especificada"""
    if pd.isna(value) or value == '':
        return ''
    try:
        # Asegurarse de que decimal_places sea un entero
        decimal_places = int(decimal_places) if not pd.isna(decimal_places) else 0
        # Formatear el número con separadores de miles y los decimales correspondientes
        return f"{float(value):,.{decimal_places}f}"
    except (ValueError, TypeError):
        return str(value)

def agregar_traza(fig, x, y, nombre, color, tipo_grafico, mostrar_numeros=True, decimal_places=0):
    """
    Agrega una traza al gráfico con formato personalizado de decimales
    
    Args:
        fig: Figura de Plotly
        x: Datos del eje X
        y: Datos del eje Y
        nombre: Nombre de la traza
        color: Color de la traza
        tipo_grafico: Tipo de gráfico ('Línea', 'Barras', 'Dispersión')
        mostrar_numeros: Si se muestran los valores numéricos
        decimal_places: Número de decimales a mostrar
    """
    # Obtener el formato de texto con los decimales correctos
    text_format = y.apply(lambda val: format_number(val, decimal_places)) if mostrar_numeros else None
    
    # Configuración común para todos los tipos de gráfico
    common_kwargs = {
        'x': x,
        'y': y,
        'name': nombre,
        'hovertemplate': f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>',
        'textfont': dict(size=10, color=color) if mostrar_numeros else None
    }
    
    if tipo_grafico == "Línea":
        # Para líneas, solo mostramos los marcadores sin texto para evitar duplicados
        fig.add_trace(go.Scatter(
            **common_kwargs,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=8, color=color, line=dict(width=1, color='white'))
        ))
        
        # Agregar etiquetas de texto como una traza separada para mejor control
        if mostrar_numeros:
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode="text",
                text=text_format,
                textposition="top center",
                textfont=dict(size=10, color=color),
                showlegend=False,
                hoverinfo='skip'
            ))
            
    elif tipo_grafico == "Barras":
        fig.add_trace(go.Bar(
            **common_kwargs,
            marker_color=color,
            text=text_format if mostrar_numeros else None,
            textposition="outside",
            textfont_size=10,
            textangle=0
        ))
        
    elif tipo_grafico == "Dispersión":
        fig.add_trace(go.Scatter(
            **common_kwargs,
            mode="markers",
            marker=dict(size=10, color=color, symbol="circle", line=dict(width=1, color='white')),
            text=text_format if mostrar_numeros else None,
            textposition="top center"
        ))

# Obtener el número de decimales para el indicador seleccionado
decimal_places = 0  # Valor por defecto
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    # Tomar el primer valor de Decimales_Ejecucion (debería ser el mismo para todos los registros del mismo indicador)
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

# Configuración de colores para las proyecciones
colores_escenarios = {
    'Base': '#1a73e8',        # Azul principal
    'Pesimista': '#ea4335',   # Rojo para pesimista
    'Optimista': '#34a853'    # Verde para optimista
}

# Agregar datos históricos según la configuración
if tipo_visualizacion == "Semestral":
    # Para "Semestral" mostrar todos los datos semestrales en una línea
    if not df_hist_semestral.empty:
        agregar_traza(fig, df_hist_semestral["Fecha"], df_hist_semestral["Ejecución"], 
                     "Histórico Semestral", "#5c8bf2", tipo_grafico, mostrar_numeros, decimal_places)

elif tipo_visualizacion == "Anual":
    # Para "Anual" mostrar solo datos de cierre (anuales)
    if not df_hist_anual.empty:
        agregar_traza(fig, df_hist_anual["Fecha"], df_hist_anual["Ejecución"], 
                     "Histórico Anual (Cierre)", "#5c8bf2", tipo_grafico, mostrar_numeros, decimal_places)

# Si no hay datos separados, mostrar línea histórica general
if df_hist_semestral.empty and df_hist_anual.empty and not df_hist_sel.empty:
    agregar_traza(fig, df_hist_sel["Fecha"], df_hist_sel["Ejecución"], 
                 "Histórico", "#5c8bf2", tipo_grafico, mostrar_numeros, decimal_places)

# Agregar proyecciones para cada escenario seleccionado
for escenario in escenarios_sel:
    df_escenario = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    if not df_escenario.empty:
        color_escenario = colores_escenarios.get(escenario, "#5c8bf2")
        agregar_traza(fig, df_escenario["Fecha"], df_escenario["Proyección"], 
                     f"Proyección {escenario}", color_escenario, tipo_grafico, mostrar_numeros, decimal_places)

# Agregar proyecciones según la configuración
colores = ['#FF00FF', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
for i, escenario in enumerate(escenarios_sel):
    df_escenario = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    if not df_escenario.empty:
        # Separar proyecciones por semestre
        df_proj_s1 = df_escenario[df_escenario["Fecha"].dt.month == 6]  # Junio (S1)
        df_proj_s2 = df_escenario[df_escenario["Fecha"].dt.month == 12]  # Diciembre (S2)
        
        # Asignar colores específicos según el tipo de escenario
        if escenario == "Optimista":
            color = "#00FF00"  # Verde brillante para optimista
        elif escenario == "Pesimista":
            color = "#FF0000"  # Rojo para pesimista
        elif escenario == "Base":
            color = "#4169E1"  # Azul real para base
        else:
            color = colores[i % len(colores)]  # Color por defecto
        
        # Agregar proyecciones según la configuración
        if tipo_visualizacion == "Semestral":
            # Para semestral: combinar S1 y S2 en una sola línea continua
            if not df_escenario.empty:
                # Ordenar por fecha para asegurar el orden correcto
                df_escenario = df_escenario.sort_values('Fecha')
                
                # Crear una sola traza para la línea
                fig.add_trace(go.Scatter(
                    x=df_escenario["Fecha"],
                    y=df_escenario["Proyección"],
                    mode='lines+markers',
                    name=escenario,
                    line=dict(color=color, width=2.5),
                    marker=dict(size=8, color=color, symbol='circle', 
                              line=dict(width=1, color='white')),
                    hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
                ))
                
                # Agregar etiquetas de texto para los puntos
                if mostrar_numeros:
                    # Combinar S1 y S2 y ordenar por fecha
                    puntos = []
                    if not df_proj_s1.empty:
                        puntos.extend([(d, v, 'S1') for d, v in zip(df_proj_s1["Fecha"], 
                                                                  df_proj_s1["Proyección"].apply(lambda x: format_number(x, decimal_places)))])
                    if not df_proj_s2.empty:
                        puntos.extend([(d, v, 'S2') for d, v in zip(df_proj_s2["Fecha"], 
                                                                  df_proj_s2["Proyección"].apply(lambda x: format_number(x, decimal_places)))])
                    
                    # Ordenar por fecha
                    puntos.sort()
                    
                    # Agregar una sola traza de texto para todos los puntos
                    if puntos:
                        fechas, valores, _ = zip(*puntos)
                        # Calcular la posición vertical de las etiquetas (más cerca de los puntos)
                        y_positions = df_escenario[df_escenario["Fecha"].isin(fechas)]["Proyección"]
                        offset = y_positions.max() * 0.015  # Reducir el desplazamiento vertical
                        
                        fig.add_trace(go.Scatter(
                            x=fechas,
                            y=y_positions + offset,  # Ajuste más sutil
                            mode='text',
                            text=valores,
                            textposition='top center',
                            textfont=dict(size=10, color=color, family='Arial'),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
                
        elif tipo_visualizacion == "Anual":
            # Para anual: mostrar solo diciembre (S2)
            if not df_proj_s2.empty:
                agregar_traza(fig, df_proj_s2["Fecha"], df_proj_s2["Proyección"], 
                             f"{escenario} (S2)", color, tipo_grafico, mostrar_numeros, decimal_places)
            elif not df_escenario.empty:
                # Si no hay datos anuales específicos, mostrar todos los datos
                agregar_traza(fig, df_escenario["Fecha"], df_escenario["Proyección"], 
                             f"{escenario}", color, tipo_grafico, mostrar_numeros, decimal_places)
        
        # Si no hay datos separados por semestre y no se ha agregado nada, mostrar línea general
        if df_proj_s1.empty and df_proj_s2.empty and tipo_visualizacion == "Semestral y Anual":
            agregar_traza(fig, df_escenario["Fecha"], df_escenario["Proyección"], 
                         f"Proyección ({modelo_sel}-{escenario})", color, tipo_grafico, mostrar_numeros)

# Línea vertical divisoria entre histórico y proyección
if mostrar_linea_divisoria and not df_hist_sel.empty and not df_proj_sel.empty:
    # Fecha específica para la división: 2025-S2 (diciembre de 2025)
    fecha_division = pd.Timestamp('2025-12-31')
    
    # Agregar línea vertical usando add_shape
    fig.add_shape(
        type="line",
        x0=fecha_division,
        x1=fecha_division,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="red", width=3, dash="dash")
    )
    
    # Agregar anotación para la línea divisoria
    fig.add_annotation(
        x=fecha_division,
        y=0.95,
        yref="paper",
        text="División Histórico/Proyección",
        showarrow=False,
        font=dict(color="red", size=12),
        xanchor="left"
    )

# Combinar fechas históricas y proyectadas para el eje X
todas_fechas = pd.concat([df_hist_sel["Fecha"], df_proj_sel["Fecha"]]).drop_duplicates().sort_values()

fig.update_layout(
    template="plotly_white",  # Cambiar a tema claro para mejor legibilidad
    xaxis_title="Fecha",
    yaxis_title=indicador_sel,
    height=600,  # Aumentar altura para mejor visualización
    margin=dict(l=50, r=50, t=80, b=80),  # Márgenes más amplios
    font=dict(family="Arial", size=12, color="#2c3e50"),  # Fuente más legible
    yaxis=dict(
        tickformat=",",
        separatethousands=True
    ),
    xaxis=dict(
        tickformat="%Y-%m",
        tickmode="array",
        ticktext=[f"{fecha.year}-S{1 if fecha.month <= 6 else 2}" for fecha in todas_fechas],
        tickvals=todas_fechas.tolist(),
        tickangle=45
    )
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# TABLA DE DATOS
# ==============================
with st.expander("📋 Ver Datos Detallados"):
    # Datos históricos
    df_hist_display = df_hist_sel.rename(columns={"Ejecución": "Valor"})[["Fecha", "Indicador", "Valor"]]
    df_hist_display["Tipo"] = "Histórico"
    df_hist_display["Escenario"] = "N/A"
    
    # Datos proyectados
    df_proj_display = df_proj_sel.rename(columns={"Proyección": "Valor"})[["Fecha", "Indicador", "Valor", "Escenario"]]
    df_proj_display["Tipo"] = "Proyección"
    
    # Combinar datos
    df_merge = pd.concat([df_hist_display, df_proj_display])
    st.dataframe(df_merge.sort_values("Fecha"), use_container_width=True)

# ==============================
# FICHAS DE RESUMEN DE ESCENARIOS
# ==============================
st.subheader("📊 Resumen de Escenarios")

# Calcular valores de referencia (último valor histórico)
# Priorizar datos anuales sobre semestrales
if not df_hist_anual.empty:
    ultimo_valor_historico = df_hist_anual["Ejecución"].iloc[-1]
elif not df_hist_semestral.empty:
    ultimo_valor_historico = df_hist_semestral["Ejecución"].iloc[-1]
else:
    ultimo_valor_historico = df_hist_sel["Ejecución"].iloc[-1] if not df_hist_sel.empty else 0

# Definir colores para las fichas
colores_fichas = ['#FF00FF', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']

# Crear fichas para cada escenario seleccionado
for i, escenario in enumerate(escenarios_sel):
    df_escenario = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    
    if not df_escenario.empty:
        # Valores del escenario
        valor_2026 = df_escenario[df_escenario["Fecha"].dt.year == 2026]["Proyección"].iloc[0] if not df_escenario[df_escenario["Fecha"].dt.year == 2026].empty else 0
        valor_2030 = df_escenario[df_escenario["Fecha"].dt.year == 2030]["Proyección"].iloc[0] if not df_escenario[df_escenario["Fecha"].dt.year == 2030].empty else 0
        
        # Cálculos de variación
        variacion_2026 = ((valor_2026 - ultimo_valor_historico) / ultimo_valor_historico * 100) if ultimo_valor_historico != 0 else 0
        variacion_2030 = ((valor_2030 - ultimo_valor_historico) / ultimo_valor_historico * 100) if ultimo_valor_historico != 0 else 0
        variacion_periodo = ((valor_2030 - valor_2026) / valor_2026 * 100) if valor_2026 != 0 else 0
        
        # Determinar color y tipo de escenario
        if escenario == "Optimista":
            color = "#00FF00"  # Verde brillante
            tipo_escenario = "Optimista"
        elif escenario == "Pesimista":
            color = "#FF0000"  # Rojo
            tipo_escenario = "Pesimista"
        elif escenario == "Base":
            color = "#4169E1"  # Azul real
            tipo_escenario = "Base"
        else:
            color = colores_fichas[i % len(colores_fichas)]
            tipo_escenario = "Neutral"
        
        # Crear ficha con columnas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                <h3>🌍 {escenario}</h3>
                <p style="font-size: 14px; margin: 5px 0;">{tipo_escenario}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric(
                "📈 2026",
                f"{valor_2026:,.0f}",
                f"{variacion_2026:+.1f}%"
            )
        
        with col3:
            st.metric(
                "🎯 2030",
                f"{valor_2030:,.0f}",
                f"{variacion_2030:+.1f}%"
            )
        
        with col4:
            st.metric(
                "📊 Variación 2026-2030",
                f"{variacion_periodo:+.1f}%",
                f"{valor_2030 - valor_2026:+,.0f}"
            )
        
        with col5:
            # Indicador de tendencia con mejor visualización
            if variacion_periodo > 0:
                tendencia = "🟢 Creciente"
                color_tendencia = "#d4edda"
                color_texto = "#155724"
            elif variacion_periodo < 0:
                tendencia = "🔴 Decreciente"
                color_tendencia = "#f8d7da"
                color_texto = "#721c24"
            else:
                tendencia = "🟡 Estable"
                color_tendencia = "#fff3cd"
                color_texto = "#856404"
            
            st.markdown(f"""
            <div style="background-color: {color_tendencia}; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid {color_texto};">
                <h4 style="color: {color_texto}; margin: 0;">{tendencia}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")  # Separador entre fichas
    
    
