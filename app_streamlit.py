import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np 
import os
from PIL import Image
import glob
import base64
import re # Agregado: Necesario para la función natural_sort_key al final

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
# FUNCIÓN PARA CARGAR LOGO
# ==============================
def get_base64_image(image_path):
    """Convierte imagen a base64 para embedding en HTML"""
    try:
        # Nota: Asegúrese de que 'Wallpaper-POLI.jpg' exista en el mismo directorio.
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Intentar cargar el logo
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"
logo_base64 = get_base64_image(LOGO_PATH) if LOGO_PATH.exists() else None

# ==============================
# ESTILOS CSS MEJORADOS Y COMPLETOS
# (Error de sintaxis corregido aquí)
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
            background: linear-gradient(180deg, #1e3a5f 0%, #2c5f8d 50%, #4a90c8 100%);
            padding: 1.5rem 1rem; 
        }
        
        [data-testid="stSidebar"] * { 
            color: white !important; 
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 { 
            color: white !important; 
            border-bottom: 2px solid rgba(255,255,255,0.3); 
            padding-bottom: 0.5rem; 
            margin-bottom: 1rem; 
        }
        
        [data-testid="stSidebar"] label {
            color: white !important;
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
        /* Contenedor principal */
        .stSelectbox {
            margin-bottom: 1.2rem;
        }
        
        /* Etiqueta del selectbox */
        .stSelectbox label {
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
            display: block !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        /* Campo del dropdown - FORZAR COLORES */
        .stSelectbox > div > div {
            background-color: white !important;
            color: #1e293b !important;
            border: 2px solid #4a90c8 !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            font-weight: 500 !important;
        }
        
        /* Texto seleccionado */
        .stSelectbox > div > div > div {
            color: #1e293b !important;
            font-weight: 500 !important;
        }
        
        /* Hover state */
        .stSelectbox > div > div:hover {
            background-color: #f8fafc !important;
            border-color: #2c5f8d !important;
            box-shadow: 0 4px 12px rgba(44, 95, 141, 0.2) !important;
        }
        
        /* Focus state */
        .stSelectbox > div > div:focus-within {
            border-color: #1e3a5f !important;
            box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.2) !important;
        }
        
        /* Dropdown expandido - MENÚ DE OPCIONES */
        [data-baseweb="popover"] {
            background-color: white !important;
            border: 2px solid #4a90c8 !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
            margin-top: 4px !important;
        }
        
        /* Opciones individuales */
        [data-baseweb="menu"] > ul > li {
            background-color: white !important;
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
            color: white !important;
            font-weight: 600 !important;
        }
        
        /* Flecha del dropdown */
        .stSelectbox svg {
            fill: #2c5f8d !important;
        }
        
        /* ==================== CHECKBOXES ==================== */
        .stCheckbox {
            margin-bottom: 0.8rem;
        }
        
        .stCheckbox label {
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
        }
        
        .stCheckbox > label > div {
            background-color: white !important;
            border: 2px solid #4a90c8 !important;
        }
        
        .stCheckbox input:checked + div {
            background-color: #2ecc71 !important;
            border-color: #27ae60 !important;
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
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(46, 204, 113, 0.5) !important;
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%) !important;
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
        
        /* ==================== EXPANDER ==================== */
        .streamlit-expanderHeader {
            background-color: white !important;
            border: 2px solid #4a90c8 !important;
            border-radius: 8px !important;
            color: #1e3a5f !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #f0f8ff !important;
            border-color: #2c5f8d !important;
        }
        
        /* ==================== DATAFRAME ==================== */
        .stDataFrame {
            border: 2px solid #4a90c8 !important;
            border-radius: 8px !important;
        }
        
        /* ==================== MODO OSCURO OVERRIDE (FIXED) ==================== */
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
            
            /* Esta sección estaba truncada y causó el SyntaxError: invalid decimal literal */
            [data-baseweb="menu"] > ul > li[aria-selected="true"] {
                background-color: #2c5f8d !important;
                color: white !important;
                font-weight: 600 !important;
            }
        }
    </style>
""", unsafe_allow_html=True) # Cierre correcto del bloque st.markdown

# ==============================
# ENCABEZADO CON LOGO (ÚNICA INSTANCIA)
# (Se eliminaron las repeticiones)
# ==============================
if logo_base64:
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0 2rem 0; background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <img src="data:image/jpeg;base64,{logo_base64}" style="max-width: 250px; height: auto; margin-bottom: 1rem;">
        <h1 class="app-title" style="margin: 0 0 0.5rem 0; font-size: 2.75rem; font-weight: 800; letter-spacing: -0.5px; color: #1e3a5f !important;">Plataforma Prospectiva de Indicadores Institucionales</h1>
        <div style="height: 5px; width: 240px; background: linear-gradient(90deg, #2c5f8d, #4a90c8, #2ecc71); margin: 0 auto 1rem; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
        <p class="app-subtitle" style="font-size: 1.2rem; margin: 0; font-weight: 500; letter-spacing: 0.3px; color: #475569 !important;">Análisis y proyección de indicadores estratégicos 2026-2030</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0 2.5rem 0;">
        <h1 class="app-title" style="margin: 0 0 0.5rem 0; font-size: 2.75rem; font-weight: 800; letter-spacing: -0.5px; color: #1e3a5f !important;">Plataforma Prospectiva de Indicadores Institucionales</h1>
        <div style="height: 5px; width: 240px; background: linear-gradient(90deg, #2c5f8d, #4a90c8, #2ecc71); margin: 0 auto 1rem; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
        <p class="app-subtitle" style="font-size: 1.2rem; margin: 0.5rem 0 0 0; font-weight: 500; letter-spacing: 0.3px; color: #475569 !important;">Análisis y proyección de indicadores estratégicos 2026-2030</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# LECTURA DE DATOS (Contenido Faltante / Lógica Principal)
# ==============================

# Aquí debe ir el código para cargar y procesar los DataFrames (df_hist, df_proj, etc.),
# las funciones de filtrado, la lógica de la barra lateral (sidebar) y el cuerpo principal
# de la aplicación Streamlit.

# Funciones necesarias para el código posterior
def natural_sort_key(text):
    """Clave para ordenar cadenas alfanuméricas de forma natural."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', str(text))]

# ==============================
# VISTA DE MODELOS (SLIDES/MODAL)
# (Se asume que esta lógica va al final de la aplicación)
# ==============================

# Definición del directorio de slides (ajustar la ruta si es necesario)
SLIDES_DIR = BASE_DIR / "slides" 

if 'mostrar_modelos' not in st.session_state:
    st.session_state['mostrar_modelos'] = False # Estado inicial

# Botón de alternar la vista de modelos
if st.sidebar.button("Visualizar Modelos de Machine Learning"):
    st.session_state['mostrar_modelos'] = not st.session_state['mostrar_modelos']

# Lógica para mostrar los slides
if st.session_state['mostrar_modelos']:
    
    # Intenta encontrar los archivos de imagen
    if SLIDES_DIR.exists():
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp', '*.PNG', '*.JPG', '*.JPEG']
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(str(SLIDES_DIR / ext)))
        image_files.sort(key=natural_sort_key)
        
        # Lógica de navegación de slides
        if image_files:
            if 'slide_index' not in st.session_state:
                st.session_state.slide_index = 0
            if st.session_state.slide_index >= len(image_files):
                st.session_state.slide_index = len(image_files) - 1
            if st.session_state.slide_index < 0:
                st.session_state.slide_index = 0

            # Estilos CSS para el modal de slides
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
                } 
                .slide-image { 
                    max-width: 100%; 
                    height: auto; 
                    border-radius: 8px; 
                } 
                .slide-controls { 
                    margin: 1.5rem 0; 
                } 
            </style> 
            """, unsafe_allow_html=True)

            # Contenido del modal/slides
            with st.container():
                st.markdown("""
                <div class="modal-header">
                    <h1 style="color: white; font-size: 2.2rem; font-weight: 700; margin: 0;">📊 Modelos de Machine Learning</h1>
                    <div style="height: 4px; width: 200px; background: linear-gradient(90deg, #2ecc71, #f1c40f); margin: 0.75rem auto 0.5rem; border-radius: 3px;"></div>
                    <p style="font-size: 1rem; color: rgba(255,255,255,0.95); margin: 0;">Visualización de los modelos utilizados en las proyecciones</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Visualización del slide
                st.markdown(f"**Slide {st.session_state.slide_index + 1} de {len(image_files)}**")
                
                current_slide_path = image_files[st.session_state.slide_index]
                st.image(str(current_slide_path), caption=Path(current_slide_path).name, use_column_width=True)

                # Controles de navegación
                col_prev, col_idx, col_next = st.columns([1, 2, 1])
                
                with col_prev:
                    if st.button("⬅️ Anterior", disabled=(st.session_state.slide_index == 0), use_container_width=True):
                        st.session_state.slide_index -= 1
                        st.rerun()
                
                with col_idx:
                    st.write(f"") # Espacio para centrar
                
                with col_next:
                    if st.button("Siguiente ➡️", disabled=(st.session_state.slide_index == len(image_files) - 1), use_container_width=True):
                        st.session_state.slide_index += 1
                        st.rerun()
        else:
            st.warning("No se encontraron archivos de imágenes de modelos en la carpeta `slides`.")
    else:
        st.error("El directorio de slides (`slides/`) no existe.")