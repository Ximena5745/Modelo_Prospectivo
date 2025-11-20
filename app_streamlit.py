import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np 
import os
from PIL import Image
import glob
import base64

# ==============================
# FUNCIÓN PARA CARGAR LOGO (antes de todo)
# ==============================
def get_base64_image(image_path):
    """Convierte imagen a base64 para embedding en HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# ==============================
# CONFIGURACIÓN_STREAMLIT
# ==============================
st.set_page_config(
    page_title="Modelo Prospectivo Poli 2026-2030",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# PANTALLA DE CARGA / SPLASH SCREEN
# ==============================
# Crear placeholder para la pantalla de carga
splash_placeholder = st.empty()

# Mostrar pantalla de carga
with splash_placeholder.container():
    st.markdown("""
    <style>
        /* Ocultar elementos de Streamlit durante la carga */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Pantalla de carga overlay */
        .splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #0a243a 0%, #10385a 30%, #10385a 70%, #2e5c84 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        /* Logo animado */
        .splash-logo {
            width: 280px;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            animation: pulse 2s ease-in-out infinite;
            margin-bottom: 2rem;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Texto de carga */
        .splash-text {
            color: white;
            font-family: 'Poppins', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Mensaje secundario */
        .splash-subtitle {
            color: rgba(255,255,255,0.9);
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            font-weight: 400;
            margin-bottom: 2.5rem;
            text-align: center;
            animation: slideUp 1s ease-out;
        }
        
        /* Spinner de carga */
        .splash-spinner {
            width: 60px;
            height: 60px;
            border: 5px solid rgba(255,255,255,0.2);
            border-top: 5px solid #2ecc71;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Barra de progreso */
        .progress-container {
            width: 400px;
            height: 6px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 2rem;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #2ecc71, #3498db, #f1c40f);
            border-radius: 10px;
            animation: loading 2s ease-in-out infinite;
            box-shadow: 0 0 10px rgba(46, 204, 113, 0.5);
        }
        
        @keyframes loading {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }
        
        /* Versión */
        .splash-version {
            position: absolute;
            bottom: 30px;
            color: rgba(255,255,255,0.6);
            font-family: 'Poppins', sans-serif;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Intentar cargar el logo
    BASE_DIR_TEMP = Path(__file__).parent
    LOGO_PATH_TEMP = BASE_DIR_TEMP / "Wallpaper-POLI.jpg"
    
    if LOGO_PATH_TEMP.exists():
        logo_base64_temp = get_base64_image(LOGO_PATH_TEMP)
        logo_html = f'<img src="data:image/jpeg;base64,{logo_base64_temp}" class="splash-logo" alt="Logo POLI">'
    else:
        logo_html = '<div style="width: 280px; height: 200px; background: rgba(255,255,255,0.1); border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 3rem; margin-bottom: 2rem;">📊</div>'
    
    st.markdown(f"""
    <div class="splash-screen">
        {logo_html}
        <div class="splash-text">
            🚀 Plataforma Prospectiva POLI
        </div>
        <div class="splash-subtitle">
            Cargando indicadores y proyecciones...
        </div>
        <div class="splash-spinner"></div>
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        <div class="splash-version">
            v2.0 - Dashboard Interactivo | 2025
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simular carga (puedes ajustar el tiempo)
    import time
    time.sleep(2.5)  # 2.5 segundos de pantalla de carga

# Limpiar la pantalla de carga
splash_placeholder.empty()

# Intentar cargar el logo
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"
logo_base64 = get_base64_image(LOGO_PATH) if LOGO_PATH.exists() else None

# ==============================
# ESTILOS CSS MEJORADOS
# ==============================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        /* ==================== RESET Y BASE ==================== */
        * { 
            font-family: 'Poppins', sans-serif;
        }
        
        .main { 
            background-color: #f0f4f8; 
            color: #1e293b; 
        }
        
        .stApp { 
            background-color: #f0f4f8; 
        }
        
        .main .block-container { 
            padding: 2rem 3rem; 
            max-width: 1800px; 
        }
        
        /* ==================== TIPOGRAFÍA ==================== */
        h1 { 
            color: #1e3a5f !important; 
            font-size: 2.5rem; 
            font-weight: 700; 
            margin-bottom: 0.5rem; 
            letter-spacing: -0.5px; 
        }
        
        h2 { 
            color: #2c5f8d !important; 
            font-size: 1.75rem; 
            font-weight: 600; 
            margin: 2rem 0 1rem 0; 
            padding-bottom: 0.5rem; 
            border-bottom: 3px solid #4a90c8; 
        }
        
        h3 { 
            color: #2c5f8d !important; 
            font-size: 1.25rem; 
            font-weight: 600; 
            margin: 1.5rem 0 0.75rem 0; 
        }
        
        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] { 
            background: linear-gradient(180deg, #0A243A 0%, #10385A 30%, #10385A 70%, #2E5C84 100%);
            padding: 1.5rem 1rem;
            overflow-y: auto !important;  /* 🔥 PERMITIR SCROLL VISIBLE */
            max-height: 100vh !important;  /* 🔥 ALTURA MÁXIMA DE VIEWPORT */
        }
        
        /* 🔥 AJUSTAR CONTENEDOR INTERNO DEL SIDEBAR */
        [data-testid="stSidebar"] > div:first-child {
            overflow-y: auto !important;
            max-height: calc(100vh - 2rem) !important;
            padding-bottom: 2rem !important;  /* 🔥 ESPACIO AL FINAL */
        }
        
        /* 🔥 SCROLLBAR PERSONALIZADA PARA SIDEBAR */
        [data-testid="stSidebar"]::-webkit-scrollbar,
        [data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
            width: 8px;
        }
        
        [data-testid="stSidebar"]::-webkit-scrollbar-track,
        [data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }
        
        [data-testid="stSidebar"]::-webkit-scrollbar-thumb,
        [data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.3);
            border-radius: 4px;
        }
        
        [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover,
        [data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.5);
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown { 
            color: white !important; 
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 { 
            border-bottom: 2px solid rgba(255,255,255,0.3); 
            padding-bottom: 0.5rem; 
            margin-bottom: 1rem; 
        }
        
        [data-testid="stSidebar"] label {
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        /* ==================== BOTONES ==================== */
        .stButton > button { 
            background: linear-gradient(135deg, #2c5f8d 0%, #1e3a5f 100%);
            color: white !important; 
            border: none; 
            border-radius: 8px; 
            padding: 0.75rem 1.5rem; 
            font-weight: 600; 
            font-size: 0.95rem; 
            box-shadow: 0 4px 12px rgba(30, 58, 95, 0.4); 
            transition: all 0.3s ease; 
            width: 100%; 
        }
        
        .stButton > button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 6px 20px rgba(30, 58, 95, 0.5);
            background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0px);
        }
        
        /* ==================== DROPDOWNS / SELECTBOX ==================== */
        .stSelectbox {
            margin-bottom: 0.8rem;  /* 🔥 REDUCIDO de 1.2rem a 0.8rem */
        }
        
        .stSelectbox label {
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;  /* 🔥 REDUCIDO de 0.95rem */
            margin-bottom: 0.4rem !important;  /* 🔥 REDUCIDO de 0.5rem */
            display: block !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        /* Campo del dropdown */
        .stSelectbox > div > div {
            background-color: #f8fafc !important;
            color: #1e293b !important;
            border: 2px solid rgba(255,255,255,0.4) !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
            font-weight: 500 !important;
        }
        
        /* Texto seleccionado */
        .stSelectbox > div > div > div {
            color: #1e293b !important;
            font-weight: 500 !important;
        }
        
        /* Hover state */
        .stSelectbox > div > div:hover {
            background-color: #ffffff !important;
            border-color: rgba(255,255,255,0.6) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        }
        
        /* Focus state */
        .stSelectbox > div > div:focus-within {
            border-color: #ffffff !important;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Dropdown expandido - MENÚ DE OPCIONES */
        [data-baseweb="popover"] {
            background-color: #ffffff !important;
            border: 2px solid #cbd5e0 !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
            margin-top: 4px !important;
        }
        
        /* Opciones individuales */
        [data-baseweb="menu"] > ul > li {
            background-color: #ffffff !important;
            color: #1e293b !important;
            padding: 12px 16px !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
        }
        
        /* Hover en opciones */
        [data-baseweb="menu"] > ul > li:hover {
            background-color: #e3f2fd !important;
            color: #1e3a5f !important;
            font-weight: 600 !important;
        }
        
        /* Opción seleccionada */
        [data-baseweb="menu"] > ul > li[aria-selected="true"] {
            background-color: #2c5f8d !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        /* Flecha del dropdown */
        .stSelectbox svg {
            fill: #1e293b !important;
        }
        
        /* ==================== CHECKBOXES MEJORADOS ==================== */
        .stCheckbox {
            margin-bottom: 0.5rem;  /* 🔥 REDUCIDO de 0.8rem a 0.5rem */
        }
        
        .stCheckbox label {
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;  /* 🔥 REDUCIDO de 0.9rem */
        }
        
        /* Eliminar TODOS los fondos de los spans y contenedores */
        .stCheckbox label span,
        .stCheckbox label div,
        .stCheckbox span,
        .stCheckbox > label,
        [data-testid="stSidebar"] .stCheckbox > label,
        [data-testid="stSidebar"] .stCheckbox label span {
            background-color: transparent !important;
            background: transparent !important;
            padding: 0 !important;
        }
        
        /* Caja del checkbox NO seleccionado - vacía/transparente con borde blanco */
        .stCheckbox > label > div[data-testid="stCheckbox"],
        .stCheckbox > label > div > div[role="checkbox"] {
            background-color: transparent !important;
            background: transparent !important;
            border: 2px solid rgba(255,255,255,0.8) !important;
            border-radius: 4px !important;
        }
        
        /* Checkbox SELECCIONADO - fondo azul claro */
        .stCheckbox input:checked ~ div[data-testid="stCheckbox"],
        .stCheckbox input:checked ~ div > div[role="checkbox"] {
            background-color: #5DADE2 !important;
            background: #5DADE2 !important;
            border: 2px solid #3498db !important;
        }
        
        /* Asegurar que el ícono de check sea visible cuando está seleccionado */
        .stCheckbox input:checked ~ div svg,
        .stCheckbox input:checked ~ div > div svg {
            fill: white !important;
            color: white !important;
        }
        
        /* Ocultar check cuando NO está seleccionado */
        .stCheckbox input:not(:checked) ~ div svg,
        .stCheckbox input:not(:checked) ~ div > div svg {
            display: none !important;
        }
        
        /* ==================== DOWNLOAD BUTTON ==================== */
        [data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
            border-left: 4px solid #229954 !important;
            color: white !important;
            padding: 0.75rem 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 12px rgba(46, 204, 113, 0.4) !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(46, 204, 113, 0.5) !important;
        }
        
        /* ==================== MÉTRICAS ==================== */
        .metric-card { 
            background: white; 
            border-radius: 12px; 
            padding: 1.5rem; 
            border-left: 4px solid #2c5f8d; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            transition: all 0.3s ease; 
        }
        
        .metric-card:hover { 
            transform: translateY(-4px); 
            box-shadow: 0 8px 24px rgba(0,0,0,0.15); 
        }
        
        .metric-label { 
            color: #64748b; 
            font-size: 0.875rem; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
            margin-bottom: 0.5rem; 
        }
        
        .metric-value { 
            color: #1e3a5f; 
            font-size: 2rem; 
            font-weight: 700; 
            line-height: 1; 
        }
        
        /* ==================== GRÁFICOS ==================== */
        .stPlotlyChart { 
            border-radius: 12px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            overflow: hidden; 
            margin: 1.5rem 0;
            background: white;
            padding: 1rem;
        }
        
        /* ==================== EXPANDER ===================== */
        .streamlit-expanderHeader {
            background-color: #f8fafc !important;
            border: 2px solid #2c5f8d !important;
            border-radius: 8px !important;
            color: #1e3a5f !important;
            font-weight: 700 !important;
            padding: 0.75rem 1.25rem !important;
            margin: 1.5rem 0 1rem 0 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
            font-size: 1.1rem !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #e6f0fa !important;
            border-color: #1e3a5f !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            transform: translateY(-1px);
        }
        
        /* Estilo para el texto del expander */
        .streamlit-expanderHeader .st-emotion-cache-1ck1k16 {
            color: #1e3a5f !important;
            font-weight: 700 !important;
        }
        
        /* Estilo para el ícono del expander */
        .streamlit-expanderHeader svg {
            color: #1e3a5f !important;
            stroke-width: 2.5px;
        }
        
        /* Estilo para el contenedor del expander */
        .stExpander {
            margin: 1.5rem 0 !important;
        }
        
        /* Estilo para el contenido del expander */
        .streamlit-expanderContent {
            background-color: #10385A !important;
            border: 2px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 8px 8px !important;
            padding: 1.5rem !important;
            margin-top: -8px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        }
        
        /* Estilo para el modo oscuro */
        @media (prefers-color-scheme: dark) {
            .streamlit-expanderHeader {
                background-color: #1e3a5f !important;
                border-color: #3d7ab8 !important;
                color: #ffffff !important;
            }
            
            .streamlit-expanderHeader:hover {
                background-color: #2c5f8d !important;
                border-color: #4a90c8 !important;
            }
            
            .streamlit-expanderHeader .st-emotion-cache-1ck1k16 {
                color: #10385A !important;
            }
            
            .streamlit-expanderHeader svg {
                color: #10385A !important;
            }
            
            .streamlit-expanderContent {
                background-color: #1e293b !important;
                border-color: #2d3748 !important;
                color: #e2e8f0 !important;
            }
        }
        
        /* ==================== DATAFRAME ==================== */
        .stDataFrame {
            border: 2px solid #4a90c8 !important;
            border-radius: 8px !important;
        }
        
        /* ==================== MODO OSCURO OVERRIDE ==================== */
        @media (prefers-color-scheme: dark) {
            .stSelectbox > div > div,
            [data-baseweb="popover"],
            [data-baseweb="menu"] > ul > li {
                background-color: white !important;
                color: #1e293b !important;
            }
            
            [data-baseweb="menu"] > ul > li:hover {
                background-color: #e3f2fd !important;
                color: #1e3a5f !important;
            }
            
            [data-baseweb="menu"] > ul > li[aria-selected="true"] {
                background-color: #2c5f8d !important;
                color: white !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# HEADER CON LOGO INTEGRADO
# ==============================
if logo_base64:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0A243A 0%, #10385A 30%, #10385A 70%, #2E5C84 100%); padding: 2.5rem 2rem; border-radius: 0 0 20px 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin: -1rem -3rem 2rem -3rem;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 2.5rem;">
            <div style="flex-shrink: 0;">
                <img src="data:image/jpeg;base64,{logo_base64}" style="width: 220px; height: auto; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.25);">
            </div>
            <div style="flex-grow: 1; text-align: left;">
                <h1 style="color: #FFFFFF !important; font-size: 2.6rem; font-weight: 800; margin: 0 0 0.75rem 0; letter-spacing: -0.5px; -webkit-text-fill-color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                    Plataforma Prospectiva de Indicadores Institucionales
                </h1>
                <div style="height: 5px; width: 300px; background: linear-gradient(90deg, #2ecc71, #3498db, #f1c40f); border-radius: 3px; margin-bottom: 0.75rem; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"></div>
                <p style="color: #FFFFFF !important; font-size: 1.2rem; margin: 0; font-weight: 500; letter-spacing: 0.3px; -webkit-text-fill-color: #FFFFFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                    📊 Análisis y proyección de indicadores estratégicos 2026-2030
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 50%, #3d7ab8 100%); padding: 2.5rem 2rem; border-radius: 0 0 20px 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin: -1rem -3rem 2rem -3rem; text-align: center;">
        <h1 style="color: #FFFFFF !important; font-size: 2.6rem; font-weight: 800; margin: 0 0 0.75rem 0; letter-spacing: -0.5px; -webkit-text-fill-color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
            Plataforma Prospectiva de Indicadores Institucionales
        </h1>
        <div style="height: 5px; width: 300px; background: linear-gradient(90deg, #2ecc71, #3498db, #f1c40f); border-radius: 3px; margin: 0 auto 0.75rem; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"></div>
        <p style="color: #FFFFFF !important; font-size: 1.2rem; margin: 0; font-weight: 500; letter-spacing: 0.3px; -webkit-text-fill-color: #FFFFFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
            📊 Análisis y proyección de indicadores estratégicos 2026-2030
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# LECTURA DE DATOS
# ==============================
RUTA_DATASET = BASE_DIR / "Data" / "Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx"

# Validar existencia de archivos
if not RUTA_DATASET.exists():
    st.error(f"❌ No se encontró el archivo histórico: {RUTA_DATASET}")
    st.stop()
if not RUTA_PROYECCIONES.exists():
    st.error(f"❌ No se encontró el archivo de proyecciones: {RUTA_PROYECCIONES}")
    st.stop()

try:
    df_hist = pd.read_excel(str(RUTA_DATASET))
    if 'Fecha' not in df_hist.columns:
        posibles_fechas = [c for c in df_hist.columns if str(c).strip().lower().replace(' ', '_') in [
            'fecha', 'periodo', 'periodo_fecha']]
        if posibles_fechas:
            df_hist = df_hist.rename(columns={posibles_fechas[0]: 'Fecha'})
    df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"], errors='coerce')

    _sheets = pd.read_excel(str(RUTA_PROYECCIONES), sheet_name=None)
    if isinstance(_sheets, dict):
        df_proj_raw = pd.concat(_sheets.values(), ignore_index=True)
    else:
        df_proj_raw = _sheets
    
    colmap = {str(c): str(c).strip().lower().replace(' ', '_').replace('ó', 'o').replace('é', 'e').replace('á', 'a').replace('í','i').replace('ú','u') for c in df_proj_raw.columns}
    df_proj_raw.columns = list(colmap.values())

    rename_rules = {}
    for cand in ['fecha_proyeccion', 'fecha_proyecccion', 'fecha', 'fecha_proyeccion_']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Fecha_Proyeccion'
            break
    for cand in ['indicador']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Indicador'
            break
    for cand in ['modelo', 'metodo', 'modelo_ml']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Modelo'
            break
    for cand in ['periodicidad']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Periodicidad'
            break
    if 'escenario_base' in df_proj_raw.columns: rename_rules['escenario_base'] = 'Escenario_Realista'
    if 'escenario_pesimista' in df_proj_raw.columns: rename_rules['escenario_pesimista'] = 'Escenario_Pesimista'
    if 'escenario_optimista' in df_proj_raw.columns: rename_rules['escenario_optimista'] = 'Escenario_Optimista'
    if 'proyeccion' in df_proj_raw.columns: rename_rules['proyeccion'] = 'Escenario_Realista'
    if 'ic_inferior' in df_proj_raw.columns: rename_rules['ic_inferior'] = 'Escenario_Pesimista'
    if 'ic_superior' in df_proj_raw.columns: rename_rules['ic_superior'] = 'Escenario_Optimista'

    if rename_rules:
        df_proj_raw = df_proj_raw.rename(columns=rename_rules)

    required = {'Indicador', 'Modelo', 'Fecha_Proyeccion', 'Escenario_Realista', 'Escenario_Pesimista', 'Escenario_Optimista'}
    missing = [c for c in required if c not in df_proj_raw.columns]
    if missing:
        st.error(f"❌ Faltan columnas requeridas: {missing}")
        st.stop()

    df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"], errors='coerce')
    if df_proj_raw["Fecha_Proyeccion"].isna().all():
        st.error("❌ No se pudieron parsear las fechas en 'Fecha_Proyeccion'")
        st.stop()
except Exception as e:
    st.exception(e)
    st.stop()

df_proj_list = []
if not df_proj_raw.empty:
    for _, row in df_proj_raw.iterrows():
        base_data = {'Indicador': row['Indicador'], 'Periodicidad': row.get('Periodicidad', 'Semestral'), 'Fecha': row['Fecha_Proyeccion'], 'Modelo': row['Modelo']}
        if pd.notna(row.get('Escenario_Realista')): df_proj_list.append({**base_data, 'Escenario': 'Realista', 'Proyección': row['Escenario_Realista']})
        if pd.notna(row.get('Escenario_Pesimista')): df_proj_list.append({**base_data, 'Escenario': 'Pesimista', 'Proyección': row['Escenario_Pesimista']})
        if pd.notna(row.get('Escenario_Optimista')): df_proj_list.append({**base_data, 'Escenario': 'Optimista', 'Proyección': row['Escenario_Optimista']})

df_proj = pd.DataFrame(df_proj_list) if df_proj_list else pd.DataFrame()
expected_proj_cols = ['Indicador', 'Periodicidad', 'Fecha', 'Modelo', 'Escenario', 'Proyección']
for c in expected_proj_cols:
    if c not in df_proj.columns:
        df_proj[c] = pd.Series(dtype='object')

# ==============================
# ORDEN MANUAL DE INDICADORES
# ==============================
ORDEN_INDICADORES = {
    "Calidad": [
        "Programas acreditables acreditados Sede Bogotá",
        "Relación Estudiante-Docente Tiempo completo",
        "Relación estudiante docente Tiempo Completo Equivalente",
        "Productos de investigación, innovación y creación",
        "Estudiantes vinculados a investigación",
        "Número de programas nuevos con registro calificado aprobado",
        "Número de renovaciones de registro calificado",
        "% de profesores (Contrato Indefinido- Fijo) impactados plan de desarrollo docente"
    ],
    "Educación_para_toda_la_vida": [
        "Ingresos totales de educación para la vida",
        "Total Ingresos B2B",
        "Total Ingresos B2G",
        "Otros ingresos (Cursos -Opciones de grado)"
    ],
    "Expansión": [
        "Total Población",
        "Total estudiantes nuevos",
        "Total Matriculados antiguos",
        "Estudiantes Pregrado",
        "Estudiantes Posgrado",
        "Estudiantes Presencial",
        "Estudiantes Virtual",
        "Brand equity",
        "Conocimiento espontaneo",
        "Lanzamiento de nuevos programas virtual"
    ],
    "Experiencia": [
        "Índice de satisfacción del estudiante (SSI)",
        "Permanencia Intersemestral",
        "NPS Estudiantes",
        "Porcentaje de cumplimiento del Acuerdo de Nivel de Servicio (ANS)"
    ],
    "Sostenibilidad": [
        "Cumplimiento de Ingresos",
        "Cumplimiento EBIDTA",
        "Caja",
        "Utilidad Neta",
        "Estudiantes con Becas",
        "Índice de Inclusión",
        "Impacto de actividades de Responsabilidad y proyección",
        "GreenMetric - Nacional",
        "Compensación de Gases de Efecto Invernadero",
        "Nivel de empleabilidad del graduado",
        "Participación de POLI- voluntariados (Estudiantes- Colaboradores)",
        "CAPEX",
        "Nivel de Cumplimiento Opex"
    ],
    "Transformación_Organizacional": [
        "Disponibilidad de servicios tecnológicos",
        "Great Place to Work",
        "Resultado de la evaluación 360 (evaluación por competencias)",
        "Índice de rotación",
        "Nivel de efectividad de las capacitaciones",
        "Cumplimiento de diagnóstico necesidades de capacitación por área",
        "Nivel de Satisfacción Servicios Prestados - Comunicaciones Internas"
    ]
}

# ==============================
# INICIALIZAR SESSION STATE
# ==============================
if 'mostrar_modelos' not in st.session_state:
    st.session_state['mostrar_modelos'] = False

if 'mostrar_historia_completa' not in st.session_state:
    st.session_state['mostrar_historia_completa'] = False

# ==============================
# SIDEBAR CON COLORES INSTITUCIONALES
# ==============================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem; padding: 1rem 0.5rem; background: rgba(255,255,255,0.1); border-radius: 12px; border: 2px solid rgba(255,255,255,0.2);">
        <h2 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 700; letter-spacing: 1px;">⚙️ CONTROLES</h2>
    </div>
    """, unsafe_allow_html=True)
    
    lineas_estrategicas = {
        "Expansión": ("Expansión", "#2c5f8d"), 
        "Transformación Organizacional": ("Transformación_Organizacional", "#1e3a5f"), 
        "Calidad": ("Calidad", "#4a90c8"), 
        "Experiencia": ("Experiencia", "#5ca3d6"), 
        "Sostenibilidad": ("Sostenibilidad", "#2ecc71"), 
        "Educación para la vida": ("Educación_para_toda_la_vida", "#3498db")
    }
    
    linea_sel = st.selectbox("🎯 Línea Estratégica", list(lineas_estrategicas.keys()))
    display_name, color_linea = lineas_estrategicas[linea_sel]
    
    # Filtrado de indicadores
    if 'Linea' in df_hist.columns:
        df_hist_filtrado = df_hist[df_hist["Linea"] == display_name]
        if df_hist_filtrado.empty: 
            df_hist_filtrado = df_hist[df_hist["Linea"].str.replace('_', ' ') == linea_sel]
        if df_hist_filtrado.empty: 
            df_hist_filtrado = df_hist
        
        indicadores_disponibles = set(df_hist_filtrado["Indicador"].unique())
        orden_manual = ORDEN_INDICADORES.get(display_name, [])
        if orden_manual:
            indicadores = [ind for ind in orden_manual if ind in indicadores_disponibles]
            indicadores_faltantes = sorted(indicadores_disponibles - set(indicadores))
            indicadores.extend(indicadores_faltantes)
        else:
            indicadores = sorted(indicadores_disponibles)
    else:
        indicadores = sorted(df_hist["Indicador"].unique())
    
    indicador_sel = st.selectbox("📊 Indicador", indicadores)
    
    # Modelos ML
    modelos = []
    if isinstance(df_proj, pd.DataFrame) and not df_proj.empty and {'Modelo','Indicador'}.issubset(df_proj.columns):
        modelos = sorted(
            df_proj[df_proj['Indicador'] == indicador_sel]['Modelo']
            .dropna().astype(str).unique()
        )
    
    modelo_display_names = {
        'Media_Movil_Tendencia': '📊 Media_Movil_Tendencia',
        'ETS': '📈 ETS',
        'Modelo_Conservador': '📉 Modelo_Conservador',
        'Polinomial_Grado_2': '📈 Polinomial_Grado_2',
        'Proyeccion_CAGR': '🎯 Proyeccion_CAGR',
        'Regresion_Lineal': '📈 Regresión Lineal',
        'Heuristico_2obs': '🔮 Heurístico',
        'Ensemble_Ponderado': '🤝 Ensemble Ponderado',
        'Promedio_Modelos': '➗ Promedio de Modelos',
        'Suavizado_Exponencial' :'📊  Suavizado_Exponencial'
    }
    
    if modelos:
        modelo_options = [modelo_display_names.get(m, m) for m in modelos]
        modelo_display_sel = st.selectbox("🧠 Modelo ML", modelo_options)
        inv_map = {v: k for k, v in modelo_display_names.items()}
        modelo_sel = inv_map.get(modelo_display_sel, modelo_display_sel)
    else:
        st.warning("⚠️ No hay proyecciones para este indicador")
        modelo_sel = ""
    
    # Escenarios
    escenarios_disponibles = ['Realista', 'Pesimista', 'Optimista']
    if modelo_sel and not df_proj.empty and modelo_sel in df_proj["Modelo"].unique():
        escenarios_modelo = df_proj[(df_proj["Modelo"] == modelo_sel) & (df_proj["Indicador"] == indicador_sel)]["Escenario"].unique()
        escenarios_disponibles = [e for e in escenarios_disponibles if e in escenarios_modelo]
    
    st.markdown("**🌍 Escenarios:**")
    escenarios_sel = []
    escenario_icons = {'Realista': '⚖️', 'Pesimista': '📉', 'Optimista': '📈'}
    for escenario in escenarios_disponibles:
        icon = escenario_icons.get(escenario, '🌍')
        if st.checkbox(f"{icon} {escenario}", value=True, key=f"esc_{escenario}"):
            escenarios_sel.append(escenario)
    
    if not escenarios_sel:
        escenarios_sel = escenarios_disponibles[:]
    
    st.markdown("<hr style='margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown("**📊 Visualización:**")
    tipo_visualizacion = st.selectbox("Periodo", ["Semestral", "Anual"], label_visibility="collapsed")
    mostrar_numeros = st.checkbox("Mostrar valores", value=True)
    mostrar_linea_divisoria = st.checkbox("Línea divisoria", value=True)
    
    st.markdown("<hr style='margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    if st.button("🔄 REFRESCAR"): 
        st.rerun()
    
    st.markdown("<hr style='margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    if st.button("📊 MODELOS", use_container_width=True, key="btn_modelos"):
        st.session_state['mostrar_modelos'] = True
        st.rerun()

# ==============================
# VISTA DE MODELOS (MODAL)
# ==============================
if st.session_state['mostrar_modelos']:
    SLIDES_DIR = BASE_DIR / "Slides"
    
    import re
    def natural_sort_key(text):
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', str(text))]
    
    if SLIDES_DIR.exists():
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp', '*.PNG', '*.JPG', '*.JPEG']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(str(SLIDES_DIR / ext)))
        
        image_files.sort(key=natural_sort_key)
        
        if image_files:
            if 'slide_index' not in st.session_state:
                st.session_state.slide_index = 0
            
            if st.session_state.slide_index >= len(image_files):
                st.session_state.slide_index = len(image_files) - 1
            if st.session_state.slide_index < 0:
                st.session_state.slide_index = 0
            
            st.markdown("""
            <style>
                .modal-header {
                    background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 50%, #4a90c8 100%);
                    padding: 2rem;
                    border-radius: 12px 12px 0 0;
                    margin: -2rem -2rem 1.5rem -2rem;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 16px rgba(30, 58, 95, 0.4);
                }
                .slide-container {
                    background: white;
                    border-radius: 12px;
                    padding: 2rem;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
                    margin: 1rem 0;
                }
                .slide-image-wrapper {
                    border: 3px solid #2c5f8d;
                    border-radius: 12px;
                    padding: 0.5rem;
                    background: #f8fafc;
                    box-shadow: 0 4px 12px rgba(44, 95, 141, 0.2);
                    margin: 1.5rem 0;
                }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="modal-header">
                <h1 style="color: white; font-size: 2.2rem; font-weight: 700; margin: 0;">📊 Modelos de Machine Learning</h1>
                <div style="height: 4px; width: 200px; background: linear-gradient(90deg, #2ecc71, #f1c40f); margin: 0.75rem auto 0.5rem; border-radius: 3px;"></div>
                <p style="font-size: 1rem; color: rgba(255,255,255,0.95); margin: 0;">Visualización de los modelos utilizados en las proyecciones</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.container():
                col_space1, col_btn, col_space2 = st.columns([2, 1, 2])
                with col_btn:
                    if st.button("❌ CERRAR", use_container_width=True, key="btn_cerrar_modelos", type="primary"):
                        st.session_state['mostrar_modelos'] = False
                        if 'slide_index' in st.session_state:
                            del st.session_state['slide_index']
                        st.rerun()
                
                st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 2px solid #e3f2fd;'>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <p style='color: #64748b; font-size: 1rem; margin: 0;'>📁 <strong>{len(image_files)}</strong> slides disponibles</p>
                </div>
                """, unsafe_allow_html=True)
                
                current_image_path = image_files[st.session_state.slide_index]
                image_name = Path(current_image_path).stem
                
                st.markdown(f"""
                <div style="text-align: center; margin: 1.5rem 0;">
                    <h2 style="color: #2c5f8d; font-weight: 600; font-size: 1.5rem; margin: 0.5rem 0;">
                        Slide {st.session_state.slide_index + 1} de {len(image_files)}
                    </h2>
                    <p style="color: #64748b; font-size: 0.9rem; font-style: italic; margin: 0.25rem 0;">{image_name}</p>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    image = Image.open(current_image_path)
                    st.markdown('<div class="slide-image-wrapper">', unsafe_allow_html=True)
                    st.image(image, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error al cargar la imagen: {e}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
                
                with col1:
                    if st.button("⏮️ PRIMERA", use_container_width=True, disabled=(st.session_state.slide_index == 0), key="btn_primera"):
                        st.session_state.slide_index = 0
                        st.rerun()
                
                with col2:
                    if st.button("⬅️ ANTERIOR", use_container_width=True, disabled=(st.session_state.slide_index == 0), key="btn_anterior"):
                        st.session_state.slide_index = max(0, st.session_state.slide_index - 1)
                        st.rerun()
                
                with col3:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 0.75rem; background: linear-gradient(135deg, #2c5f8d 0%, #1e3a5f 100%); 
                    color: white; border-radius: 8px; font-weight: 700; font-size: 1.1rem; box-shadow: 0 2px 8px rgba(44, 95, 141, 0.4);">
                        {st.session_state.slide_index + 1} / {len(image_files)}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    if st.button("SIGUIENTE ➡️", use_container_width=True, disabled=(st.session_state.slide_index == len(image_files) - 1), key="btn_siguiente"):
                        st.session_state.slide_index = min(len(image_files) - 1, st.session_state.slide_index + 1)
                        st.rerun()
                
                with col5:
                    if st.button("ÚLTIMA ⏭️", use_container_width=True, disabled=(st.session_state.slide_index == len(image_files) - 1), key="btn_ultima"):
                        st.session_state.slide_index = len(image_files) - 1
                        st.rerun()
                
                st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 2px solid #e3f2fd;'>", unsafe_allow_html=True)
                
                with st.expander("🖼️ Ver todas las miniaturas", expanded=False):
                    st.markdown("<br>", unsafe_allow_html=True)
                    num_cols = 4
                    for idx in range(0, len(image_files), num_cols):
                        cols = st.columns(num_cols)
                        for col_idx, img_idx in enumerate(range(idx, min(idx + num_cols, len(image_files)))):
                            with cols[col_idx]:
                                try:
                                    img_path = image_files[img_idx]
                                    img = Image.open(img_path)
                                    img_name = Path(img_path).stem
                                    
                                    is_current = img_idx == st.session_state.slide_index
                                    border_color = "#2c5f8d" if is_current else "#e2e8f0"
                                    border_width = "4px" if is_current else "2px"
                                    bg_color = "#e3f2fd" if is_current else "white"
                                    
                                    st.markdown(f"""
                                    <div style="border: {border_width} solid {border_color}; border-radius: 8px; 
                                    padding: 0.5rem; margin-bottom: 0.5rem; background: {bg_color}; 
                                    transition: all 0.3s ease;">
                                    """, unsafe_allow_html=True)
                                    
                                    st.image(img, use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                                    
                                    button_style = "🎯" if is_current else "📌"
                                    
                                    if st.button(f"{button_style} Slide {img_idx + 1}", key=f"thumb_{img_idx}", 
                                               use_container_width=True):
                                        st.session_state.slide_index = img_idx
                                        st.rerun()
                                    
                                    st.markdown(f"""
                                    <p style='text-align: center; font-size: 0.7rem; color: #64748b; 
                                    margin-top: 0.25rem; font-weight: {"bold" if is_current else "normal"};'>
                                    {img_name[:25]}...
                                    </p>
                                    """, unsafe_allow_html=True)
                                    
                                except Exception as e:
                                    st.error(f"❌ Error: {img_idx + 1}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ No se encontraron imágenes en la carpeta Slides")
            st.info(f"📁 Ruta esperada: {SLIDES_DIR}")
            
            if st.button("Cerrar", key="btn_cerrar_warning"):
                st.session_state['mostrar_modelos'] = False
                st.rerun()
    else:
        st.error(f"❌ No se encontró la carpeta: {SLIDES_DIR}")
        
        if st.button("Cerrar", key="btn_cerrar_error"):
            st.session_state['mostrar_modelos'] = False
            st.rerun()
    
    st.stop()

# ==============================
# FUNCIONES AUXILIARES
# ==============================
@st.cache_data
def convert_df_to_xlsx(df):
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
        workbook = writer.book
        worksheet = writer.sheets['Datos']
        # Ajustar el ancho de las columnas
        for i, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, min(max_length, 30))  # Limitar el ancho máximo a 30
    return output.getvalue()

def calcular_config_etiquetas(num_puntos: int, tipo_visualizacion: str) -> dict:
    """
    Calcula la configuración de etiquetas para los ejes de la gráfica.
    
    Args:
        num_puntos: Número de puntos de datos
        tipo_visualizacion: 'Anual' o 'Semestral'
        
    Returns:
        dict: Configuración de etiquetas para los ejes que incluye:
            - show: si mostrar las etiquetas
            - angle: ángulo de rotación en grados
            - skip: cada cuántas etiquetas mostrar
            - size: tamaño de la fuente
    """
    base_config = {
        'show': True,
        'size': 12  # Tamaño de fuente base
    }
    
    if tipo_visualizacion == "Anual":
        if num_puntos <= 10:
            return {**base_config, 'angle': 0, 'skip': 1}
        elif num_puntos <= 20:
            return {**base_config, 'angle': 45, 'skip': 1}
        else:
            return {**base_config, 'angle': 45, 'skip': max(1, num_puntos // 10)}
    else:  # Semestral
        if num_puntos <= 20:
            return {**base_config, 'angle': 0, 'skip': 1}
        elif num_puntos <= 40:
            return {**base_config, 'angle': 45, 'skip': 2, 'size': 11}
        else:
            return {
                **base_config, 
                'angle': 45, 
                'skip': max(2, num_puntos // 10),
                'size': 10  # Tamaño más pequeño para muchos puntos
            }

def format_number(value, decimals):
    if pd.isna(value): return ''
    try:
        decimals = int(decimals) if pd.notna(decimals) else 0
        return f"{float(value):,.{decimals}f}"
    except:
        return str(value)

def ultimo_semestre_val(df_hist_source: pd.DataFrame, target_year: int = 2025):
    try:
        if df_hist_source is None or df_hist_source.empty:
            return np.nan
        dfh = df_hist_source.copy()
        if 'Fuente' in dfh.columns:
            dfh = dfh[dfh['Fuente'] == 'Semestral']
        dfx = dfh[dfh['Fecha'].dt.year == target_year]
        if not dfx.empty:
            return dfx.sort_values('Fecha').iloc[-1]['Ejecución']
        dfx_prev = dfh[dfh['Fecha'].dt.year == (target_year - 1)]
        if not dfx_prev.empty:
            return dfx_prev.sort_values('Fecha').iloc[-1]['Ejecución']
        dfx_lte = dfh[dfh['Fecha'] <= pd.to_datetime(f'{target_year}-12-31')]
        if not dfx_lte.empty:
            return dfx_lte.sort_values('Fecha').iloc[-1]['Ejecución']
        return np.nan
    except Exception:
        return np.nan

def periodo_label(fecha, tipo: str) -> str:
    if pd.isna(fecha):
        return ''
    f = pd.to_datetime(fecha)
    y = int(f.year)
    if tipo == "Semestral":
        return f"{y}-01 a {y}-06" if f.month <= 6 else f"{y}-07 a {y}-12"
    return f"{y}-01 a {y}-12"

def periodos_rango_por_ano(year: int, tipo: str):
    if tipo == "Semestral":
        return [
            (pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year, month=6, day=30)),
            (pd.Timestamp(year=year, month=7, day=1), pd.Timestamp(year=year, month=12, day=31)),
        ]
    return [
        (pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year, month=12, day=31)),
    ]

# ==============================
# FILTRAR DATOS
# ==============================
if 'Linea' in df_hist.columns:
    df_hist_sel = df_hist[(df_hist["Indicador"] == indicador_sel) & (df_hist["Linea"] == display_name)]
    if df_hist_sel.empty: 
        df_hist_sel = df_hist[(df_hist["Indicador"] == indicador_sel) & (df_hist["Linea"].str.replace('_', ' ') == linea_sel)]
else:
    df_hist_sel = df_hist[df_hist["Indicador"] == indicador_sel]

df_proj_sel = df_proj[
    (df_proj["Indicador"] == indicador_sel) & 
    (df_proj["Modelo"] == modelo_sel) & 
    (df_proj["Escenario"].isin(escenarios_sel))
].copy()

df_proj_sel['Fecha'] = pd.to_datetime(df_proj_sel['Fecha'])
df_proj_sel = df_proj_sel.sort_values('Fecha')

# ==============================
# Detectar indicadores bianuales (usar años 2027 y 2029)
# ==============================
bianual_ids = {202, 361}
bianual_names = {"Great Place to Work", "Índice de Inclusión"}
indicator_is_bianual = False
indicator_id = None
for possible_id_col in ['Id', 'ID', 'id', 'Indicador_Id', 'IndicadorId']:
    if possible_id_col in df_hist_sel.columns and not df_hist_sel.empty:
        try:
            indicator_id = int(df_hist_sel.iloc[0][possible_id_col])
        except Exception:
            indicator_id = df_hist_sel.iloc[0][possible_id_col]
        break

if (indicator_id in bianual_ids) or (indicador_sel in bianual_names):
    indicator_is_bianual = True

# Años de comparación por defecto (pueden cambiarse según periodicidad)
if indicator_is_bianual:
    COMP_YEAR_1, COMP_YEAR_2 = 2027, 2029
else:
    COMP_YEAR_1, COMP_YEAR_2 = 2026, 2030

# Año base histórico usado para calcular variaciones (no se modifica)
BASE_YEAR = 2025

# Configuración de decimales y sentido
decimal_places = 0
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

if 'Sentido' in df_hist_sel.columns and not df_hist_sel.empty:
    sentido = df_hist_sel['Sentido'].iloc[0] if not df_hist_sel.empty else 'Positivo'
    indicador_negativo = str(sentido).strip().lower() == 'negativo'
else:
    indicador_negativo = False

colores_escenarios = {
    'Optimista': '#2ecc71',
    'Base': '#2c5f8d',
    'Pesimista': '#e74c3c',
    'Histórico Semestral': '#D4A017',
    'Histórico Anual': '#D4A017'
}

# ==============================
# TARJETAS DE RESUMEN
# ==============================
df_base = df_proj[(df_proj["Indicador"] == indicador_sel) & (df_proj["Modelo"] == modelo_sel) & (df_proj["Escenario"] == 'Realista')]

if not df_base.empty:
    valor_y1 = df_base[df_base['Fecha'].dt.year == COMP_YEAR_1]['Proyección'].max()
    valor_y2 = df_base[df_base['Fecha'].dt.year == COMP_YEAR_2]['Proyección'].max()
    ultimo_historico = ultimo_semestre_val(df_hist_sel, target_year=BASE_YEAR)
    variacion_periodo = valor_y2 - valor_y1 if pd.notna(valor_y2) and pd.notna(valor_y1) else 0

    st.markdown(f'<div style="background:{colores_escenarios.get("Base", "#2c5f8d")}; color:#ffffff; font-weight:800; font-size:1.15rem; padding:.6rem .9rem; border-radius:10px; margin: 0 0 .75rem 0; letter-spacing:.3px;">⚖️ ESCENARIO BASE</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="metric-card" style="border-left-color: #2ecc71;"><div class="metric-label">📈 ÚLTIMO HISTÓRICO</div><div class="metric-value" style="color: #1e293b;">{format_number(ultimo_historico, decimal_places)}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #2c5f8d;"><div class="metric-label">🎯 PROYECCIÓN ({COMP_YEAR_1})</div><div class="metric-value" style="color: #2c5f8d;">{format_number(valor_y1, decimal_places)}</div></div>', unsafe_allow_html=True)
    with col3:
        delta_color = "#2ecc71" if variacion_periodo > 0 else ("#e74c3c" if variacion_periodo < 0 else "#f1c40f")
        st.markdown(f'<div class="metric-card" style="border-left-color: #f39c12;"><div class="metric-label">⭐ PROYECCIÓN ({COMP_YEAR_2})</div><div class="metric-value" style="color: #f39c12; margin-bottom: 0.25rem;">{format_number(valor_y2, decimal_places)}</div><div style="color: {delta_color}; font-size: 1rem; font-weight: 600; margin-top: 0.25rem;">Δ {valor_y2 - valor_y1:+,.{int(decimal_places)}f}</div></div>', unsafe_allow_html=True)
    with col4:
        if variacion_periodo > 0: tendencia, icon_tend, color_tend = "Creciente", "🟢", "#2ecc71"
        elif variacion_periodo < 0: tendencia, icon_tend, color_tend = "Decreciente", "🔴", "#e74c3c"
        else: tendencia, icon_tend, color_tend = "Estable", "🟡", "#f1c40f"
        st.markdown(f'<div class="metric-card" style="border-left-color: {color_tend};"><div class="metric-label">📊 TENDENCIA PERIODO</div><div style="font-size: 2rem; margin: 0.5rem 0;">{icon_tend}</div><div style="color: {color_tend}; font-size: 1.1rem; font-weight: 700;">{tendencia}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.warning(f"⚠️ No se encontraron datos para el Escenario Realista del indicador {indicador_sel}")
    st.markdown("<br>", unsafe_allow_html=True)

# ==============================
# GRÁFICO PRINCIPAL CON TAMAÑO DE LETRA DINÁMICO
# ==============================
st.subheader("Evolución Histórica y Proyección Detallada")

df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"].copy()
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"].copy()

if tipo_visualizacion == "Semestral" and not df_hist_semestral.empty:
    df_hist_semestral['Fecha'] = df_hist_semestral['Fecha'].apply(
        lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
    )
if tipo_visualizacion == "Anual" and not df_hist_anual.empty:
    df_hist_anual['Fecha'] = df_hist_anual['Fecha'].apply(
        lambda x: pd.Timestamp(year=x.year, month=6, day=30)
    )

fig = go.Figure()

df_hist_trace = df_hist_semestral if tipo_visualizacion == "Semestral" else df_hist_anual
if df_hist_trace.empty:
    df_hist_trace = df_hist_anual if not df_hist_anual.empty else df_hist_semestral
if df_hist_trace.empty:
    df_hist_trace = df_hist_sel.copy()
    if tipo_visualizacion == "Semestral":
        df_hist_trace['Fecha'] = df_hist_trace['Fecha'].apply(
            lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
        )
    else:
        df_hist_trace['Fecha'] = df_hist_trace['Fecha'].apply(
            lambda x: pd.Timestamp(year=x.year, month=6, day=30)
        )

# 🔥 FILTRAR DATOS DESDE 2021-S2 POR DEFECTO
fecha_corte_vista = pd.Timestamp(year=2021, month=7, day=1)  # 2021-S2
df_hist_trace_original = df_hist_trace.copy()

# 🔥 FILTRAR DATOS DESDE 2021-S2 POR DEFECTO
fecha_corte_vista = pd.Timestamp(year=2021, month=7, day=1)  # 2021-S2
df_hist_trace_original = df_hist_trace.copy()

# Verificar si hay datos anteriores a 2021-S2
tiene_datos_antiguos = not df_hist_trace[df_hist_trace['Fecha'] < fecha_corte_vista].empty

# Aplicar filtro solo si NO se ha activado "mostrar historia completa"
if not st.session_state['mostrar_historia_completa'] and tiene_datos_antiguos:
    df_hist_trace = df_hist_trace[df_hist_trace['Fecha'] >= fecha_corte_vista].copy()

# 🔥 CALCULAR CONFIGURACIÓN DE ETIQUETAS DINÁMICAMENTE
num_puntos_historicos = len(df_hist_trace)
config_etiquetas = calcular_config_etiquetas(num_puntos_historicos, tipo_visualizacion)

trace_name = "Histórico Semestral" if tipo_visualizacion == "Semestral" else "Histórico Anual"

if not df_hist_trace.empty:
    fig.add_trace(go.Scatter(
        x=df_hist_trace["Fecha"], 
        y=df_hist_trace["Ejecución"], 
        name=trace_name, 
        line=dict(color='#D4A017', width=2), 
        marker=dict(size=6, color='#D4A017', line=dict(width=1, color='white')), 
        mode='lines+markers', 
        hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
    ))
    
    if indicador_negativo:
        fig.add_annotation(
            x=0.98, y=0.92, xref='paper', yref='paper',
            text="<i>Nota: Los colores están invertidos (menor = mejor)</i>",
            showarrow=False, font=dict(size=10, color="#666666"), align="right"
        )
    
    # 🔥 MOSTRAR NÚMEROS SOLO SI LA CONFIGURACIÓN LO PERMITE
    if mostrar_numeros and config_etiquetas['show']:
        # Filtrar puntos según 'skip' (mostrar 1 de cada N)
        skip = config_etiquetas['skip']
        indices_mostrar = list(range(0, len(df_hist_trace), skip))
        
        df_etiquetas = df_hist_trace.iloc[indices_mostrar].copy()
        text_values = df_etiquetas["Ejecución"].apply(lambda x: format_number(x, decimal_places))
        
        # 🔥 CALCULAR OFFSET AUMENTADO (7% del rango total para mayor separación)
        y_range = df_hist_trace["Ejecución"].max() - df_hist_trace["Ejecución"].min()
        offset_value = y_range * 0.07  # 🔥 AUMENTADO de 5% a 7% para más espacio
        
        # 🔥 APLICAR OFFSET: sumar al valor Y para separar de la línea
        y_values_offset = df_etiquetas["Ejecución"] + offset_value
        
        fig.add_trace(go.Scatter(
            x=df_etiquetas["Fecha"], 
            y=y_values_offset,  # 🔥 VALORES CON OFFSET AUMENTADO
            mode="text", 
            text=text_values, 
            textposition="middle center",
            textfont=dict(
                size=config_etiquetas['size'], 
                color='#D4A017', 
                family="Poppins",
                weight=800  # 🔥 EXTRA BOLD para máxima visibilidad
            ),
            showlegend=False, 
            hoverinfo='skip', 
            texttemplate='%{text}', 
            cliponaxis=False
        ))

for escenario in escenarios_sel:
    df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    if not df_esc.empty:
        color = colores_escenarios.get(escenario, '#2c5f8d')
        df_plot = df_esc.copy()
        
        if tipo_visualizacion == "Semestral":
            df_plot['Fecha'] = df_plot['Fecha'].apply(
                lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
            )
        else:
            df_plot['Año'] = df_plot['Fecha'].dt.year
            df_plot = df_plot.sort_values('Fecha').groupby('Año').last().reset_index()
            df_plot['Fecha'] = df_plot['Año'].apply(lambda y: pd.Timestamp(year=y, month=6, day=30))
        
        df_plot = df_plot.sort_values('Fecha')
        
        if not df_plot.empty:
            fig.add_trace(go.Scatter(
                x=df_plot["Fecha"], y=df_plot["Proyección"], 
                name=escenario + (" (Anual)" if tipo_visualizacion == "Anual" else ""), 
                line=dict(color=color, width=2, dash='dot'), 
                marker=dict(size=6, color=color, line=dict(width=1, color='white')), 
                mode='lines+markers', 
                hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
            ))
            
            # 🔥 MOSTRAR NÚMEROS DE PROYECCIÓN SOLO SI LA CONFIGURACIÓN LO PERMITE
            if mostrar_numeros and config_etiquetas['show']:
                # Calcular configuración para proyecciones (usualmente menos puntos)
                num_puntos_proy = len(df_plot)
                config_proy = calcular_config_etiquetas(num_puntos_proy, tipo_visualizacion)
                
                # Filtrar puntos según 'skip'
                skip = config_proy['skip']
                indices_mostrar = list(range(0, len(df_plot), skip))
                df_etiquetas_proy = df_plot.iloc[indices_mostrar].copy()
                
                text_values = df_etiquetas_proy["Proyección"].apply(lambda x: format_number(x, decimal_places))
                
                # 🔥 CALCULAR OFFSET DIFERENCIADO SEGÚN ESCENARIO Y SENTIDO DEL INDICADOR
                if not df_plot.empty:
                    y_range_proy = df_plot["Proyección"].max() - df_plot["Proyección"].min()
                    
                    # 🔥 AJUSTAR SEGÚN SENTIDO DEL INDICADOR (OFFSETS AUMENTADOS)
                    if not indicador_negativo:
                        # SENTIDO POSITIVO: Mayor valor = Mejor (Optimista arriba)
                        if escenario == "Optimista":
                            offset_proy = y_range_proy * 0.10  # 🔥 10% arriba (aumentado de 8%)
                        elif escenario == "Base":
                            offset_proy = y_range_proy * 0.07  # 🔥 7% arriba (aumentado de 5%)
                        else:  # Pesimista
                            offset_proy = y_range_proy * 0.04  # 🔥 4% arriba (aumentado de 2%)
                    else:
                        # SENTIDO NEGATIVO: Menor valor = Mejor (Pesimista arriba, Optimista abajo)
                        if escenario == "Pesimista":
                            offset_proy = y_range_proy * 0.04  # 🔥 4% arriba
                        elif escenario == "Base":
                            offset_proy = y_range_proy * 0.07  # 🔥 7% arriba
                        else:  # Optimista
                            offset_proy = y_range_proy * 0.10  # 🔥 10% arriba
                else:
                    offset_proy = 0
                
                # 🔥 APLICAR OFFSET: sumar al valor Y
                y_values_offset_proy = df_etiquetas_proy["Proyección"] + offset_proy
                
                fig.add_trace(go.Scatter(
                    x=df_etiquetas_proy["Fecha"], 
                    y=y_values_offset_proy,  # 🔥 VALORES CON OFFSET SEGÚN SENTIDO
                    mode="text", 
                    text=text_values, 
                    textposition="middle center",
                    textfont=dict(
                        size=config_proy['size'], 
                        color=color, 
                        family="Poppins",
                        weight=800  # 🔥 EXTRA BOLD
                    ),
                    showlegend=False, 
                    hoverinfo='skip', 
                    texttemplate='%{text}', 
                    cliponaxis=False
                ))

if mostrar_linea_divisoria:
    fecha_corte = pd.Timestamp(year=2025, month=12, day=31)
    fecha_corte_str = fecha_corte.strftime('%Y-%m-%d')
    fig.add_vline(x=fecha_corte_str, line_width=2, line_dash="dash", line_color="#808080")
    fig.add_annotation(
        x=fecha_corte_str, y=1, xref="x", yref="paper",
        text="Inicio Proyección", showarrow=False, xanchor="left", yanchor="top",
        font=dict(color="#808080", size=12, weight="bold"), yshift=-10
    )

# Configurar ejes
tickvals = []
ticktext = []
hist_years = sorted(df_hist_trace['Fecha'].dt.year.unique()) if not df_hist_trace.empty else []  # 🔥 Usar df_hist_trace filtrado
proj_years = sorted(df_proj_sel['Fecha'].dt.year.unique()) if not df_proj_sel.empty else []
all_years = sorted(set(hist_years + proj_years))

if all_years:
    min_year = min(all_years) if all_years else 2021  # 🔥 Usar el mínimo real de los datos filtrados
    max_year = max(max(all_years), COMP_YEAR_2)
    all_years = list(range(min_year, max_year + 1))
else:
    all_years = list(range(2021, 2031))  # 🔥 Default desde 2021

if tipo_visualizacion == "Semestral":
    for year in all_years:
        tickvals.append(f"{year}-03-15")
        ticktext.append(f"{year}-S1")
        tickvals.append(f"{year}-09-15")
        ticktext.append(f"{year}-S2")
elif tipo_visualizacion == "Anual":
    for year in all_years:
        tickvals.append(f"{year}-06-30")
        ticktext.append(str(year))

shapes = []
period_index = 0
for y in all_years:
    for x0, x1 in periodos_rango_por_ano(y, tipo_visualizacion):
        if period_index % 2 == 0:
            shapes.append(dict(
                type='rect', xref='x', yref='paper', x0=x0, x1=x1, y0=0, y1=1,
                fillcolor='rgba(0,0,0,0.03)', line=dict(width=0), layer='below'
            ))
        period_index += 1

fig.update_layout(
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    height=700,  # 🔥 AUMENTADO de 600 a 700px para optimizar espacio
    font=dict(family="Poppins", size=12, color="#1e293b", weight=600),  # 🔥 Fuente base aumentada a 12px y bold
    title=dict(
        text=f"<b>{indicador_sel}</b>",
        x=0.5, y=0.97, xanchor='center', yanchor='top',
        font=dict(size=20, color="#1e3a5f", family="Poppins", weight="bold")  # 🔥 Título aumentado a 20px
    ),
    annotations=[
        dict(
            text="Evolución Histórica y Proyección",
            x=0.02, y=0.92, xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color="#4a5568", family="Poppins", weight=600)  # 🔥 Subtítulo a 14px
        )
    ],
    hovermode='x unified',
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.95)", bordercolor="#cbd5e0", borderwidth=1.5,
        font=dict(size=13, family="Poppins", color="#1e293b", weight=600),  # 🔥 Leyenda a 13px
        itemsizing='constant', itemclick=False, itemdoubleclick=False
    ),
    xaxis=dict(
        title=dict(
            text="<b>PERIODO</b>",
            font=dict(size=15, weight=700, family="Poppins", color="#1e293b"),  # 🔥 Aumentado a 15px
            standoff=10  # 🔥 Mayor separación
        ),
        showgrid=True, gridcolor='rgba(0,0,0,0.05)', gridwidth=1,
        tickmode='array',  # 🔥 FORZAR uso de tickvals/ticktext personalizados
        tickvals=tickvals, 
        ticktext=ticktext, 
        tickfont=dict(size=12, family="Poppins", color="#1e293b", weight=600),  # 🔥 AUMENTADO a 12px
        linecolor='#cbd5e0', linewidth=2, mirror=True, showline=True, 
        automargin=True, 
        tickangle=-45,  # 🔥 DIAGONAL para mejor legibilidad con muchas etiquetas
        title_standoff=15, fixedrange=False,  # 🔥 HABILITAR ZOOM (fixedrange=False)
        ticklabeloverflow='allow', 
        ticklabelposition='outside',
        range=[
            df_hist_trace['Fecha'].min().strftime('%Y-%m-%d') if not df_hist_trace.empty else "2021-07-01", 
            df_proj_sel['Fecha'].max().strftime('%Y-%m-%d') if not df_proj_sel.empty else f"{COMP_YEAR_2}-12-31"
        ]
    ),
    yaxis=dict(
        title=dict(
            text=f"<b>{indicador_sel.upper()}</b>",
            font=dict(size=15, weight=700, family="Poppins", color="#1e293b"),  # 🔥 Aumentado a 15px
            standoff=12  # 🔥 Aumentado de 10 a 12
        ),
        showgrid=True, gridcolor='rgba(0,0,0,0.05)', gridwidth=1,
        tickformat=f",.{int(decimal_places)}f",
        tickfont=dict(size=12, family="Poppins", color="#1e293b", weight=600),  # 🔥 Aumentado a 12px
        title_standoff=18, showline=True, linecolor='#cbd5e0',  # 🔥 Mayor separación
        linewidth=2, mirror=True, zeroline=False, automargin=True, fixedrange=False  # 🔥 HABILITAR ZOOM
    ),
    hoverlabel=dict(
        bgcolor="white", font_size=12, font_family="Poppins",  # 🔥 Hover aumentado a 12px
        bordercolor="#cbd5e0", namelength=-1, align="left"
    ),
    margin=dict(t=80, b=90, r=40, l=100, pad=8),  # 🔥 MÁRGENES OPTIMIZADOS para mayor espacio
    shapes=shapes,
    # 🔥 CONFIGURACIÓN DE HERRAMIENTAS DE LA GRÁFICA (MODEBAR)
    modebar=dict(
        orientation='h',  # 🔥 HORIZONTAL (parte superior derecha como original)
        bgcolor='rgba(255,255,255,0.9)',
        color='#1e3a5f',
        activecolor='#2ecc71'
    ),
    # 🔥 MODO PAN (arrastrar) POR DEFECTO - NO ZOOM
    dragmode='pan',  # Pan en lugar de zoom
)

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,  # 🔥 MOSTRAR barra de herramientas SIEMPRE
    'displaylogo': False,  # Ocultar logo de Plotly
    'modeBarButtonsToAdd': [
        'drawline',          # ✏️ Dibujar líneas
        'drawopenpath',      # ✏️ Dibujar líneas libres
        'drawclosedpath',    # ✏️ Dibujar formas cerradas
        'drawcircle',        # ⭕ Dibujar círculos
        'drawrect',          # ▭ Dibujar rectángulos
        'eraseshape',        # 🗑️ Borrar formas
    ],
    'modeBarButtonsToRemove': [
        'select2d',          # Remover selección 2D
        'lasso2d'            # Remover lasso
    ],
    'toImageButtonOptions': {
        'format': 'png',     # Formato de descarga
        'filename': f'{indicador_sel}_{modelo_sel}',
        'height': 1000,      # 🔥 Mayor resolución
        'width': 1800,       # 🔥 Mayor resolución
        'scale': 3           # 🔥 Calidad ultra alta (3x)
    },
    'scrollZoom': True,      # 🔥 Zoom con scroll del mouse
    'doubleClick': 'reset',  # Doble clic para resetear
    'showTips': True,        # Mostrar tips
    'responsive': True,      # Responsive
})

# 🔥 MOSTRAR BOTÓN "VER HISTORIA COMPLETA" DESPUÉS DE LA GRÁFICA
if tiene_datos_antiguos:
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state['mostrar_historia_completa']:
        st.markdown("""
        <style>
            .btn-ver-mas button {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                border: none !important;
                padding: 0.6rem 1.2rem !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3) !important;
                transition: all 0.3s ease !important;
                font-size: 0.95rem !important;
            }
            .btn-ver-mas button:hover {
                background: linear-gradient(135deg, #2980b9 0%, #21618c 100%) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 3.5])
        with col_btn1:
            st.markdown('<div class="btn-ver-mas">', unsafe_allow_html=True)
            if st.button("📅 Ver historia completa", key="btn_ver_mas_below", use_container_width=True):
                st.session_state['mostrar_historia_completa'] = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .btn-ver-menos button {
                background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                border: none !important;
                padding: 0.6rem 1.2rem !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 8px rgba(149, 165, 166, 0.3) !important;
                transition: all 0.3s ease !important;
                font-size: 0.95rem !important;
            }
            .btn-ver-menos button:hover {
                background: linear-gradient(135deg, #7f8c8d 0%, #6c7a7b 100%) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(149, 165, 166, 0.4) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 3.5])
        with col_btn1:
            st.markdown('<div class="btn-ver-menos">', unsafe_allow_html=True)
            if st.button("📅 Vista reciente (2021+)", key="btn_ver_menos_below", use_container_width=True):
                st.session_state['mostrar_historia_completa'] = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# COMPARATIVO DE ESCENARIOS
# ==============================
if not df_proj_sel.empty and len(escenarios_sel) > 0:
    st.markdown(f"### Comparativo de Escenarios (vs Último {BASE_YEAR})")
    num_cols = max(1, len(escenarios_sel))
    cols = st.columns(num_cols)
    base_historico = ultimo_semestre_val(df_hist_sel, target_year=BASE_YEAR)

    for i, escenario in enumerate(escenarios_sel):
        esc_color = colores_escenarios.get(escenario, '#2c5f8d')
        df_e = df_proj_sel[df_proj_sel['Escenario'] == escenario]

        def get_year_value(df, year):
            dfx = df[df['Fecha'].dt.year == year]
            if dfx.empty:
                return np.nan
            return dfx.sort_values('Fecha').iloc[-1]['Proyección']

        v_y1 = get_year_value(df_e, COMP_YEAR_1)
        v_y2 = get_year_value(df_e, COMP_YEAR_2)

        pct_y1 = np.nan
        pct_y2 = np.nan
        if pd.notna(base_historico) and base_historico != 0:
            if pd.notna(v_y1):
                pct_y1 = (v_y1 - base_historico) / abs(base_historico) * 100.0
            if pd.notna(v_y2):
                pct_y2 = (v_y2 - base_historico) / abs(base_historico) * 100.0

        with cols[i]:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: {esc_color};">
                    <div style="background:{esc_color}; color:#ffffff; font-weight:800; font-size:1.1rem; padding:.45rem .7rem; border-radius:8px; margin-bottom:.75rem; letter-spacing:.3px;">{escenario.upper()}</div>
                    <div class="metric-label">Base · Último {BASE_YEAR}</div>
                    <div class="metric-value" style="color: #1e293b;">{format_number(base_historico, decimal_places) if pd.notna(base_historico) else 'N/A'}</div>
                    <div class="metric-label" style="margin-top:0.75rem;">{escenario} · {COMP_YEAR_1}</div>
                    <div class="metric-value" style="color: {esc_color};">{format_number(v_y1, decimal_places) if pd.notna(v_y1) else 'N/A'}</div>
                    <div class="metric-label" style="margin-top:0.25rem;">Δ% vs {BASE_YEAR}</div>
                    <div class="metric-value" style="color: {'#2ecc71' if (pd.notna(pct_y1) and pct_y1>=0) else '#e74c3c'};font-size:1.2rem;">{(f"{pct_y1:,.2f}%" if pd.notna(pct_y1) else 'N/A')}</div>
                    <div class="metric-label" style="margin-top:0.75rem;">{escenario} · {COMP_YEAR_2}</div>
                    <div class="metric-value" style="color: {esc_color};">{format_number(v_y2, decimal_places) if pd.notna(v_y2) else 'N/A'}</div>
                    <div class="metric-label" style="margin-top:0.25rem;">Δ% vs {BASE_YEAR}</div>
                    <div class="metric-value" style="color: {'#2ecc71' if (pd.notna(pct_y2) and pct_y2>=0) else '#e74c3c'};font-size:1.2rem;">{(f"{pct_y2:,.2f}%" if pd.notna(pct_y2) else 'N/A')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ==============================
# TABLA DE DATOS DETALLADOS
# ==============================
st.markdown("---")

# CSS Style
st.markdown("""
    <style>
        /* Target the expander header text with more specific selectors */
        [data-testid="stExpander"] .streamlit-expanderHeader,
        [data-testid="stExpander"] .streamlit-expanderHeader * {
            color: #1e3a5f !important;
            -webkit-text-fill-color: #1e3a5f !important;
            font-weight: 600 !important;
            fill: #1e3a5f !important; /* For SVG icons */
        }
        
        /* Dark mode override */
        @media (prefers-color-scheme: dark) {
            [data-testid="stExpander"] .streamlit-expanderHeader,
            [data-testid="stExpander"] .streamlit-expanderHeader * {
                color: #4a90c8 !important;
                -webkit-text-fill-color: #4a90c8 !important;
                fill: #4a90c8 !important; /* For SVG icons */
            }
        }
    </style>
""", unsafe_allow_html=True)

# Filtrar histrico segn el tipo de visualización seleccionado
with st.expander(" Ver Datos Detallados (Histórico y Proyección)"):
    # Filtrar histrico segn el tipo de visualización seleccionado
    if tipo_visualizacion == "Anual":
        df_hist_display = df_hist_sel[df_hist_sel['Fuente'] == 'Cierre'].copy()
    else:  # Semestral
        df_hist_display = df_hist_sel[df_hist_sel['Fuente'] == 'Semestral'].copy()
    
    # Asegurarse de que la columna Fecha sea datetime
    df_hist_display['Fecha'] = pd.to_datetime(df_hist_display['Fecha'])
    
    # Verificar si la columna 'Ejecución' existe, si no, usar 'Valor' o 'Valor_Historico'
    hist_col = 'Ejecución' if 'Ejecución' in df_hist_display.columns else 'Valor_Historico' if 'Valor_Historico' in df_hist_display.columns else 'Valor'
    df_hist_display = df_hist_display.rename(columns={hist_col: 'Histórico'})
    
    # Seleccionar solo las columnas necesarias
    df_hist_display = df_hist_display[['Fecha', 'Indicador', 'Histórico', 'Fuente']]
    
    # Filtrar proyecciones segn el tipo de visualizacin
    if tipo_visualizacion == "Anual":
        # Para visualizacin anual, solo mostrar proyecciones de fin de año (Diciembre)
        df_proj_filtered = df_proj_sel[df_proj_sel['Fecha'].dt.month == 12].copy()
    else:
        # Para visualizacin semestral, mostrar todas las proyecciones
        df_proj_filtered = df_proj_sel.copy()
    
    # Asegurarse de que la columna Fecha sea datetime
    df_proj_filtered['Fecha'] = pd.to_datetime(df_proj_filtered['Fecha'])
    
    # Crear la tabla pivote para las proyecciones
    df_proj_display = df_proj_filtered.pivot_table(
        index=['Fecha', 'Indicador'], 
        columns='Escenario', 
        values='Proyección'
    ).reset_index()
    
    # Combinar históricos y proyecciones
    df_final_display = pd.merge(
        df_hist_display, 
        df_proj_display, 
        on=['Fecha', 'Indicador'], 
        how='outer'
    )
    
    # Ordenar por fecha
    df_final_display = df_final_display.sort_values('Fecha')
    
    # Convertir fechas a string para visualización
    df_final_display['Fecha'] = df_final_display['Fecha'].apply(
        lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else ''
    )
    
    # Reordenar columnas para mejor presentación
    column_order = ['Fecha', 'Indicador', 'Histórico', 'Fuente'] + \
                 [e for e in escenarios_sel if e in df_proj_display.columns]
    df_final_display = df_final_display[column_order]
    df_final_display = df_final_display.sort_values(by='Fecha').reset_index(drop=True)
    
    df_download = df_final_display.copy()

    for col in df_final_display.columns:
        if df_final_display[col].dtype in [np.float64, np.int64]:
            df_final_display[col] = df_final_display[col].apply(lambda x: format_number(x, decimal_places) if pd.notna(x) else '-')

    # Convertir siempre a datetime, ignorando errores
    df_final_display['Fecha'] = pd.to_datetime(df_final_display['Fecha'], errors='coerce')

    # Formatear sin romper si hay NaT
    df_final_display['Fecha'] = df_final_display['Fecha'].dt.strftime('%Y-%m-%d')
    
    excel_file = convert_df_to_xlsx(df_download)
    
    st.download_button(
        label="📥 Descargar Información Detallada (Excel)",
        data=excel_file,
        file_name=f'{indicador_sel}_{modelo_sel}_Proyecciones.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key='download_excel_button'
    )

    st.dataframe(df_final_display, use_container_width=True, hide_index=True)