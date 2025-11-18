"""
PLATAFORMA PROSPECTIVA POLI 2026-2030
PARTE 1: IMPORTS Y CONFIGURACIÓN INICIAL
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np 
import os
from PIL import Image
import glob
import base64
import time
import re

# ==============================
# FUNCIÓN PARA CARGAR LOGO
# ==============================
def get_base64_image(image_path):
    """Convierte imagen a base64 para embedding en HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# ==============================
# CONFIGURACIÓN DE STREAMLIT
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
splash_placeholder = st.empty()

with splash_placeholder.container():
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        .splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 50%, #3d7ab8 100%);
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
        
        .splash-logo {
            width: 280px;
            height: auto;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            animation: pulse 2s ease-in-out infinite;
            margin-bottom: 2rem;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
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
        
        .splash-subtitle {
            color: rgba(255,255,255,0.9);
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            font-weight: 400;
            margin-bottom: 2.5rem;
            text-align: center;
            animation: slideUp 1s ease-out;
        }
        
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
        
        .splash-version {
            position: absolute;
            bottom: 30px;
            color: rgba(255,255,255,0.6);
            font-family: 'Poppins', sans-serif;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    time.sleep(2.5)

splash_placeholder.empty()

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"
logo_base64 = get_base64_image(LOGO_PATH) if LOGO_PATH.exists() else None

"""
PARTE 2: ESTILOS CSS MEJORADOS - ADAPTABLES A MODO CLARO/OSCURO
"""

CSS_STYLES = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        /* ==================== RESET Y BASE ==================== */
        * { 
            font-family: 'Poppins', sans-serif;
        }
        
        /* MODO CLARO (por defecto) */
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
            background: linear-gradient(180deg, #1e3a5f 0%, #2c5f8d 50%, #3d7ab8 100%);
            padding: 1.5rem 1rem;
            overflow-y: auto !important;
            max-height: 100vh !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            overflow-y: auto !important;
            max-height: calc(100vh - 2rem) !important;
            padding-bottom: 2rem !important;
        }
        
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
            margin-bottom: 0.8rem;
        }
        
        .stSelectbox label {
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.4rem !important;
            display: block !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        .stSelectbox > div > div {
            background-color: #f8fafc !important;
            color: #1e293b !important;
            border: 2px solid rgba(255,255,255,0.4) !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
            font-weight: 500 !important;
        }
        
        .stSelectbox > div > div > div {
            color: #1e293b !important;
            font-weight: 500 !important;
        }
        
        .stSelectbox > div > div:hover {
            background-color: #ffffff !important;
            border-color: rgba(255,255,255,0.6) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: #ffffff !important;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3) !important;
        }
        
        [data-baseweb="popover"] {
            background-color: #ffffff !important;
            border: 2px solid #cbd5e0 !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
            margin-top: 4px !important;
        }
        
        [data-baseweb="menu"] > ul > li {
            background-color: #ffffff !important;
            color: #1e293b !important;
            padding: 12px 16px !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
        }
        
        [data-baseweb="menu"] > ul > li:hover {
            background-color: #e3f2fd !important;
            color: #1e3a5f !important;
            font-weight: 600 !important;
        }
        
        [data-baseweb="menu"] > ul > li[aria-selected="true"] {
            background-color: #2c5f8d !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        .stSelectbox svg {
            fill: #1e293b !important;
        }
        
        /* ==================== CHECKBOXES MEJORADOS ==================== */
        .stCheckbox {
            margin-bottom: 0.5rem;
        }
        
        .stCheckbox label {
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
        }
        
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
        
        .stCheckbox > label > div[data-testid="stCheckbox"],
        .stCheckbox > label > div > div[role="checkbox"] {
            background-color: transparent !important;
            background: transparent !important;
            border: 2px solid rgba(255,255,255,0.8) !important;
            border-radius: 4px !important;
        }
        
        .stCheckbox input:checked ~ div[data-testid="stCheckbox"],
        .stCheckbox input:checked ~ div > div[role="checkbox"] {
            background-color: #5DADE2 !important;
            background: #5DADE2 !important;
            border: 2px solid #3498db !important;
        }
        
        .stCheckbox input:checked ~ div svg,
        .stCheckbox input:checked ~ div > div svg {
            fill: white !important;
            color: white !important;
        }
        
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
        
        /* ==================== EXPANDER - CORREGIDO PARA MODO CLARO/OSCURO ===================== */
        /* MODO CLARO */
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
        
        /* FORZAR COLOR DEL TEXTO Y TODOS SUS HIJOS */
        .streamlit-expanderHeader,
        .streamlit-expanderHeader *,
        .streamlit-expanderHeader p,
        .streamlit-expanderHeader span,
        .streamlit-expanderHeader div {
            color: #1e3a5f !important;
            font-weight: 700 !important;
        }
        
        /* ÍCONO DEL EXPANDER */
        .streamlit-expanderHeader svg {
            color: #1e3a5f !important;
            stroke: #1e3a5f !important;
            fill: #1e3a5f !important;
            stroke-width: 2.5px;
        }
        
        .stExpander {
            margin: 1.5rem 0 !important;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 8px 8px !important;
            padding: 1.5rem !important;
            margin-top: -8px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        }
        
        /* ==================== DATAFRAME ==================== */
        .stDataFrame {
            border: 2px solid #4a90c8 !important;
            border-radius: 8px !important;
        }
        
        /* ==================== MODO OSCURO ==================== */
        @media (prefers-color-scheme: dark) {
            /* FONDO PRINCIPAL */
            .main {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            
            .stApp {
                background-color: #0e1117 !important;
            }
            
            /* TIPOGRAFÍA */
            h1, h2, h3, h4, h5, h6 {
                color: #fafafa !important;
            }
            
            h2 {
                border-bottom-color: #4a90c8 !important;
            }
            
            /* SELECTBOX EN MODO OSCURO */
            .stSelectbox > div > div {
                background-color: #262730 !important;
                color: #fafafa !important;
                border-color: rgba(255,255,255,0.2) !important;
            }
            
            .stSelectbox > div > div > div {
                color: #fafafa !important;
            }
            
            .stSelectbox > div > div:hover {
                background-color: #31313c !important;
            }
            
            .stSelectbox svg {
                fill: #fafafa !important;
            }
            
            [data-baseweb="popover"] {
                background-color: #262730 !important;
                border-color: #4a4a5a !important;
            }
            
            [data-baseweb="menu"] > ul > li {
                background-color: #262730 !important;
                color: #fafafa !important;
            }
            
            [data-baseweb="menu"] > ul > li:hover {
                background-color: #31313c !important;
                color: #ffffff !important;
            }
            
            [data-baseweb="menu"] > ul > li[aria-selected="true"] {
                background-color: #2c5f8d !important;
                color: #ffffff !important;
            }
            
            /* MÉTRICAS EN MODO OSCURO */
            .metric-card {
                background-color: #262730 !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
            }
            
            .metric-card:hover {
                box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
            }
            
            .metric-label {
                color: #a0aec0 !important;
            }
            
            .metric-value {
                color: #fafafa !important;
            }
            
            /* GRÁFICOS EN MODO OSCURO */
            .stPlotlyChart {
                background-color: #262730 !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
            }
            
            /* ======== EXPANDER EN MODO OSCURO - CRÍTICO ======== */
            .streamlit-expanderHeader {
                background-color: #1e3a5f !important;
                border-color: #3d7ab8 !important;
            }
            
            .streamlit-expanderHeader:hover {
                background-color: #2c5f8d !important;
                border-color: #4a90c8 !important;
            }
            
            /* FORZAR COLOR BLANCO EN MODO OSCURO */
            .streamlit-expanderHeader,
            .streamlit-expanderHeader *,
            .streamlit-expanderHeader p,
            .streamlit-expanderHeader span,
            .streamlit-expanderHeader div {
                color: #ffffff !important;
            }
            
            /* ÍCONO BLANCO EN MODO OSCURO */
            .streamlit-expanderHeader svg {
                color: #ffffff !important;
                stroke: #ffffff !important;
                fill: #ffffff !important;
            }
            
            /* CONTENIDO DEL EXPANDER EN MODO OSCURO */
            .streamlit-expanderContent {
                background-color: #262730 !important;
                border-color: #4a4a5a !important;
                color: #fafafa !important;
            }
            
            /* DATAFRAME EN MODO OSCURO */
            .stDataFrame {
                border-color: #4a90c8 !important;
            }
            
            /* TEXTO GENERAL EN MODO OSCURO */
            p, span, div {
                color: #fafafa !important;
            }
        }
    </style>
"""


"""
PARTE 3: HEADER Y LECTURA DE DATOS
"""

# Aplicar estilos CSS
# st.markdown(CSS_STYLES, unsafe_allow_html=True)  # Descomentar cuando se integre

# ==============================
# HEADER CON LOGO INTEGRADO
# ==============================
def create_header(logo_base64):
    if logo_base64:
        return f"""
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 50%, #3d7ab8 100%); padding: 2.5rem 2rem; border-radius: 0 0 20px 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin: -1rem -3rem 2rem -3rem;">
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
        """
    else:
        return """
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8d 50%, #3d7ab8 100%); padding: 2.5rem 2rem; border-radius: 0 0 20px 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin: -1rem -3rem 2rem -3rem; text-align: center;">
            <h1 style="color: #FFFFFF !important; font-size: 2.6rem; font-weight: 800; margin: 0 0 0.75rem 0; letter-spacing: -0.5px; -webkit-text-fill-color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                Plataforma Prospectiva de Indicadores Institucionales
            </h1>
            <div style="height: 5px; width: 300px; background: linear-gradient(90deg, #2ecc71, #3498db, #f1c40f); border-radius: 3px; margin: 0 auto 0.75rem; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"></div>
            <p style="color: #FFFFFF !important; font-size: 1.2rem; margin: 0; font-weight: 500; letter-spacing: 0.3px; -webkit-text-fill-color: #FFFFFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                📊 Análisis y proyección de indicadores estratégicos 2026-2030
            </p>
        </div>
        """

# ==============================
# LECTURA DE DATOS
# ==============================
def leer_datos(BASE_DIR):
    """
    Lee y procesa los archivos de datos históricos y proyecciones
    
    Returns:
        tuple: (df_hist, df_proj) DataFrames procesados
    """
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
        # Leer datos históricos
        df_hist = pd.read_excel(str(RUTA_DATASET))
        if 'Fecha' not in df_hist.columns:
            posibles_fechas = [c for c in df_hist.columns if str(c).strip().lower().replace(' ', '_') in [
                'fecha', 'periodo', 'periodo_fecha']]
            if posibles_fechas:
                df_hist = df_hist.rename(columns={posibles_fechas[0]: 'Fecha'})
        df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"], errors='coerce')
        
        # Leer proyecciones
        _sheets = pd.read_excel(str(RUTA_PROYECCIONES), sheet_name=None)
        if isinstance(_sheets, dict):
            df_proj_raw = pd.concat(_sheets.values(), ignore_index=True)
        else:
            df_proj_raw = _sheets
        
        # Normalizar nombres de columnas
        colmap = {str(c): str(c).strip().lower().replace(' ', '_').replace('ó', 'o').replace('é', 'e').replace('á', 'a').replace('í','i').replace('ú','u') for c in df_proj_raw.columns}
        df_proj_raw.columns = list(colmap.values())
        
        # Mapeo de columnas
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
        if 'escenario_base' in df_proj_raw.columns: rename_rules['escenario_base'] = 'Escenario_Base'
        if 'escenario_pesimista' in df_proj_raw.columns: rename_rules['escenario_pesimista'] = 'Escenario_Pesimista'
        if 'escenario_optimista' in df_proj_raw.columns: rename_rules['escenario_optimista'] = 'Escenario_Optimista'
        if 'proyeccion' in df_proj_raw.columns: rename_rules['proyeccion'] = 'Escenario_Base'
        if 'ic_inferior' in df_proj_raw.columns: rename_rules['ic_inferior'] = 'Escenario_Pesimista'
        if 'ic_superior' in df_proj_raw.columns: rename_rules['ic_superior'] = 'Escenario_Optimista'
        
        if rename_rules:
            df_proj_raw = df_proj_raw.rename(columns=rename_rules)
        
        # Validar columnas requeridas
        required = {'Indicador', 'Modelo', 'Fecha_Proyeccion', 'Escenario_Base', 'Escenario_Pesimista', 'Escenario_Optimista'}
        missing = [c for c in required if c not in df_proj_raw.columns]
        if missing:
            st.error(f"❌ Faltan columnas requeridas: {missing}")
            st.stop()
        
        df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"], errors='coerce')
        if df_proj_raw["Fecha_Proyeccion"].isna().all():
            st.error("❌ No se pudieron parsear las fechas en 'Fecha_Proyeccion'")
            st.stop()
        
        # Transformar proyecciones a formato largo
        df_proj_list = []
        if not df_proj_raw.empty:
            for _, row in df_proj_raw.iterrows():
                base_data = {
                    'Indicador': row['Indicador'], 
                    'Periodicidad': row.get('Periodicidad', 'Semestral'), 
                    'Fecha': row['Fecha_Proyeccion'], 
                    'Modelo': row['Modelo']
                }
                if pd.notna(row.get('Escenario_Base')): 
                    df_proj_list.append({**base_data, 'Escenario': 'Base', 'Proyección': row['Escenario_Base']})
                if pd.notna(row.get('Escenario_Pesimista')): 
                    df_proj_list.append({**base_data, 'Escenario': 'Pesimista', 'Proyección': row['Escenario_Pesimista']})
                if pd.notna(row.get('Escenario_Optimista')): 
                    df_proj_list.append({**base_data, 'Escenario': 'Optimista', 'Proyección': row['Escenario_Optimista']})
        
        df_proj = pd.DataFrame(df_proj_list) if df_proj_list else pd.DataFrame()
        expected_proj_cols = ['Indicador', 'Periodicidad', 'Fecha', 'Modelo', 'Escenario', 'Proyección']
        for c in expected_proj_cols:
            if c not in df_proj.columns:
                df_proj[c] = pd.Series(dtype='object')
        
        return df_hist, df_proj
        
    except Exception as e:
        st.exception(e)
        st.stop()

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

"""
PARTE 4: FUNCIONES AUXILIARES
"""

# ==============================
# FUNCIONES AUXILIARES
# ==============================

@st.cache_data
def convert_df_to_csv(df):
    """Convierte DataFrame a CSV"""
    return df.to_csv(index=False, sep=';').encode('utf-8')

def format_number(value, decimals):
    """Formatea números con decimales específicos"""
    if pd.isna(value): 
        return ''
    try:
        decimals = int(decimals) if pd.notna(decimals) else 0
        return f"{float(value):,.{decimals}f}"
    except:
        return str(value)

def ultimo_semestre_val(df_hist_source: pd.DataFrame, target_year: int = 2025):
    """Obtiene el valor del último semestre disponible"""
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
    """Genera etiqueta de periodo según el tipo"""
    if pd.isna(fecha):
        return ''
    f = pd.to_datetime(fecha)
    y = int(f.year)
    if tipo == "Semestral":
        return f"{y}-01 a {y}-06" if f.month <= 6 else f"{y}-07 a {y}-12"
    return f"{y}-01 a {y}-12"

def periodos_rango_por_ano(year: int, tipo: str):
    """Genera rangos de periodos por año"""
    if tipo == "Semestral":
        return [
            (pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year, month=6, day=30)),
            (pd.Timestamp(year=year, month=7, day=1), pd.Timestamp(year=year, month=12, day=31)),
        ]
    return [
        (pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year, month=12, day=31)),
    ]

def calcular_config_etiquetas(num_puntos: int, tipo_visualizacion: str) -> dict:
    """
    Calcula la configuración de etiquetas basado en el número de puntos de datos.
    
    Args:
        num_puntos: Número de puntos de datos históricos
        tipo_visualizacion: "Semestral" o "Anual"
    
    Returns:
        dict con: size (tamaño), show (mostrar o no), angle (ángulo), skip (cada cuántos mostrar)
    """
    if tipo_visualizacion == "Semestral":
        if num_puntos <= 8:
            return {'size': 16, 'show': True, 'angle': 0, 'skip': 1}
        elif num_puntos <= 12:
            return {'size': 15, 'show': True, 'angle': 0, 'skip': 1}
        elif num_puntos <= 18:
            return {'size': 14, 'show': True, 'angle': 0, 'skip': 1}
        elif num_puntos <= 25:
            return {'size': 13, 'show': True, 'angle': 0, 'skip': 2}
        elif num_puntos <= 35:
            return {'size': 12, 'show': True, 'angle': 0, 'skip': 2}
        else:
            return {'size': 11, 'show': True, 'angle': 0, 'skip': 3}
    else:
        if num_puntos <= 5:
            return {'size': 18, 'show': True, 'angle': 0, 'skip': 1}
        elif num_puntos <= 8:
            return {'size': 17, 'show': True, 'angle': 0, 'skip': 1}
        elif num_puntos <= 12:
            return {'size': 16, 'show': True, 'angle': 0, 'skip': 1}
        elif num_puntos <= 15:
            return {'size': 15, 'show': True, 'angle': 0, 'skip': 1}
        else:
            return {'size': 14, 'show': True, 'angle': 0, 'skip': 1}

def natural_sort_key(text):
    """Ordenamiento natural para nombres de archivo"""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', str(text))]

# ==============================
# COLORES DE ESCENARIOS
# ==============================
COLORES_ESCENARIOS = {
    'Optimista': '#2ecc71',
    'Base': '#2c5f8d',
    'Pesimista': '#e74c3c',
    'Histórico Semestral': '#D4A017',
    'Histórico Anual': '#D4A017'
}

# ==============================
# MODELOS ML - NOMBRES DISPLAY
# ==============================
MODELO_DISPLAY_NAMES = {
    'ARIMA': '📊 ARIMA',
    'ETS': '📈 ETS',
    'Holt_Winters': '📉 Holt-Winters',
    'Random_Forest': '🌳 Random Forest',
    'SVR': '🎯 SVR',
    'Linear_Regression': '📈 Regresión Lineal',
    'Regresion_Lineal': '📈 Regresión Lineal',
    'Prophet': '🔮 Prophet',
    'Tendencia_Historica': '📜 Tendencia Histórica',
    'Crecimiento_Historico': '📜 Crecimiento Histórico',
    'Ensemble_Ponderado': '🤝 Ensemble Ponderado',
    'Promedio_Modelos': '➗ Promedio de Modelos'
}

# ==============================
# LÍNEAS ESTRATÉGICAS
# ==============================
LINEAS_ESTRATEGICAS = {
    "Expansión": ("Expansión", "#2c5f8d"), 
    "Transformación Organizacional": ("Transformación_Organizacional", "#1e3a5f"), 
    "Calidad": ("Calidad", "#4a90c8"), 
    "Experiencia": ("Experiencia", "#5ca3d6"), 
    "Sostenibilidad": ("Sostenibilidad", "#2ecc71"), 
    "Educación para la vida": ("Educación_para_toda_la_vida", "#3498db")
}

# ==============================
# ICONOS DE ESCENARIOS
# ==============================
ESCENARIO_ICONS = {
    'Base': '⚖️', 
    'Pesimista': '📉', 
    'Optimista': '📈'
}



"""
PARTE 5: SIDEBAR Y CONTROLES
Nota: Este código debe ejecutarse después de cargar los datos
"""

def crear_sidebar(df_hist, df_proj, ORDEN_INDICADORES, LINEAS_ESTRATEGICAS, MODELO_DISPLAY_NAMES, ESCENARIO_ICONS):
    """
    Crea el sidebar con todos los controles de la aplicación
    
    Returns:
        dict: Diccionario con todos los valores seleccionados
    """
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem; padding: 1rem 0.5rem; background: rgba(255,255,255,0.1); border-radius: 12px; border: 2px solid rgba(255,255,255,0.2);">
            <h2 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 700; letter-spacing: 1px;">⚙️ CONTROLES</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # LÍNEA ESTRATÉGICA
        linea_sel = st.selectbox("🎯 Línea Estratégica", list(LINEAS_ESTRATEGICAS.keys()))
        display_name, color_linea = LINEAS_ESTRATEGICAS[linea_sel]
        
        # FILTRADO DE INDICADORES
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
        
        # SELECTOR DE INDICADOR
        indicador_sel = st.selectbox("📊 Indicador", indicadores)
        
        # MODELOS ML
        modelos = []
        if isinstance(df_proj, pd.DataFrame) and not df_proj.empty and {'Modelo','Indicador'}.issubset(df_proj.columns):
            modelos = sorted(
                df_proj[df_proj['Indicador'] == indicador_sel]['Modelo']
                .dropna().astype(str).unique()
            )
        
        if modelos:
            modelo_options = [MODELO_DISPLAY_NAMES.get(m, m) for m in modelos]
            modelo_display_sel = st.selectbox("🧠 Modelo ML", modelo_options)
            inv_map = {v: k for k, v in MODELO_DISPLAY_NAMES.items()}
            modelo_sel = inv_map.get(modelo_display_sel, modelo_display_sel)
        else:
            st.warning("⚠️ No hay proyecciones para este indicador")
            modelo_sel = ""
        
        # ESCENARIOS
        escenarios_disponibles = ['Base', 'Pesimista', 'Optimista']
        if modelo_sel and not df_proj.empty and modelo_sel in df_proj["Modelo"].unique():
            escenarios_modelo = df_proj[(df_proj["Modelo"] == modelo_sel) & (df_proj["Indicador"] == indicador_sel)]["Escenario"].unique()
            escenarios_disponibles = [e for e in escenarios_disponibles if e in escenarios_modelo]
        
        st.markdown("**🌍 Escenarios:**")
        escenarios_sel = []
        for escenario in escenarios_disponibles:
            icon = ESCENARIO_ICONS.get(escenario, '🌍')
            if st.checkbox(f"{icon} {escenario}", value=True, key=f"esc_{escenario}"):
                escenarios_sel.append(escenario)
        
        if not escenarios_sel:
            escenarios_sel = escenarios_disponibles[:]
        
        # VISUALIZACIÓN
        st.markdown("<hr style='margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        st.markdown("**📊 Visualización:**")
        tipo_visualizacion = st.selectbox("Periodo", ["Semestral", "Anual"], label_visibility="collapsed")
        mostrar_numeros = st.checkbox("Mostrar valores", value=True)
        mostrar_linea_divisoria = st.checkbox("Línea divisoria", value=True)
        
        # BOTONES
        st.markdown("<hr style='margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        if st.button("🔄 REFRESCAR"): 
            st.rerun()
        
        st.markdown("<hr style='margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        if st.button("📊 MODELOS", use_container_width=True, key="btn_modelos"):
            st.session_state['mostrar_modelos'] = True
            st.rerun()
    
    return {
        'linea_sel': linea_sel,
        'display_name': display_name,
        'color_linea': color_linea,
        'indicador_sel': indicador_sel,
        'modelo_sel': modelo_sel,
        'escenarios_sel': escenarios_sel,
        'tipo_visualizacion': tipo_visualizacion,
        'mostrar_numeros': mostrar_numeros,
        'mostrar_linea_divisoria': mostrar_linea_divisoria
    }

# ==============================
# INICIALIZAR SESSION STATE
# ==============================
def inicializar_session_state():
    """Inicializa las variables de estado de la sesión"""
    if 'mostrar_modelos' not in st.session_state:
        st.session_state['mostrar_modelos'] = False
    
    if 'mostrar_historia_completa' not in st.session_state:
        st.session_state['mostrar_historia_completa'] = False


        