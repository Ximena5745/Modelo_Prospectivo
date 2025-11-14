from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import base64
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass

# ==============================
# CONFIGURATION
# ==============================
@dataclass
class AppConfig:
    """Application configuration settings"""
    PAGE_TITLE = "Modelo Prospectivo Poli 2026-2030"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    BASE_DIR = Path(__file__).parent
    LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"
    DATA_DIR = BASE_DIR / "Data"
    DATASET_PATH = DATA_DIR / "Dataset_Unificado.xlsx"
    PROJECTIONS_PATH = DATA_DIR / "Proyecciones_Multimodelo.xlsx"
    SLIDES_DIR = BASE_DIR / "Slides"
    
    # Visualization settings
    CHART_HEIGHT = 900
    CHART_FONT_FAMILY = "Poppins"
    CHART_TITLE_FONT_SIZE = 24
    CHART_AXIS_FONT_SIZE = 16

# ==============================
# DATA MODELS
# ==============================
@dataclass
class ProjectionData:
    """Container for projection data"""
    historical_data: pd.DataFrame
    projections: pd.DataFrame
    indicator: str
    model: str
    scenarios: List[str]

# ==============================
# UTILITY FUNCTIONS
# ==============================
def load_image_as_base64(image_path: Path) -> Optional[str]:
    """Load an image file and return as base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {image_path}: {e}")
        return None

def format_number(value: float, decimals: int = 0) -> str:
    """Format a number with the specified decimal places"""
    if pd.isna(value):
        return "N/A"
    try:
        return f"{float(value):,.{int(decimals)}f}"
    except (ValueError, TypeError):
        return str(value)

def calculate_percentage_change(current: float, previous: float) -> float:
    """Calculate percentage change between two values"""
    if previous == 0:
        return 0
    return ((current - previous) / abs(previous)) * 100.0

# ==============================
# DATA LOADING AND PROCESSING
# ==============================
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load and preprocess historical and projection data"""
    try:
        # Load historical data
        df_hist = pd.read_excel(str(AppConfig.DATASET_PATH))
        df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"], errors='coerce')
        
        # Load projection data
        df_proj = pd.read_excel(str(AppConfig.PROJECTIONS_PATH), sheet_name=None)
        df_proj = pd.concat(df_proj.values(), ignore_index=True)
        
        # Clean and standardize column names
        df_proj.columns = (
            df_proj.columns.str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.normalize('NFKD')
            .str.encode('ascii', errors='ignore')
            .str.decode('utf-8')
        )
        
        # Standardize column names
        column_mapping = {
            'fecha_proyeccion': 'fecha_proyeccion',
            'fecha_proyecccion': 'fecha_proyeccion',
            'fecha': 'fecha_proyeccion',
            'fecha_proyeccion_': 'fecha_proyeccion',
            'indicador': 'indicador',
            'modelo': 'modelo',
            'metodo': 'modelo',
            'modelo_ml': 'modelo',
            'periodicidad': 'periodicidad',
            'escenario_base': 'escenario_base',
            'escenario_pesimista': 'escenario_pesimista',
            'escenario_optimista': 'escenario_optimista',
            'proyeccion': 'escenario_base',
            'ic_inferior': 'escenario_pesimista',
            'ic_superior': 'escenario_optimista'
        }
        
        df_proj = df_proj.rename(columns={k: v for k, v in column_mapping.items() if k in df_proj.columns})
        
        return df_hist, df_proj
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# ==============================
# VISUALIZATION COMPONENTS
# ==============================
def create_metric_card(title: str, value: str, color: str = "#2c5f8d", delta: str = None) -> None:
    """Create a metric card with optional delta indicator"""
    delta_html = f"""
    <div style="color: {'#2ecc71' if delta and delta.startswith('+') else '#e74c3c' if delta and delta.startswith('-') else '#f1c40f'}; 
                 font-size: 0.9rem; margin-top: 0.25rem;">
        {delta if delta else ''}
    </div>
    """ if delta else ""
    
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 1.5rem; 
                border-left: 4px solid {color}; box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
                margin-bottom: 1rem; height: 100%;">
        <div style="color: #64748b; font-size: 0.9rem; font-weight: 600; 
                   margin-bottom: 0.5rem; text-transform: uppercase;">
            {title}
        </div>
        <div style="font-size: 1.8rem; font-weight: 700; color: {color};">
            {value}
        </div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# ==============================
# MAIN APP
# ==============================
def main():
    # Initialize session state
    if 'mostrar_modelos' not in st.session_state:
        st.session_state['mostrar_modelos'] = False
    
    # Page configuration
    st.set_page_config(
        page_title=AppConfig.PAGE_TITLE,
        page_icon=AppConfig.PAGE_ICON,
        layout=AppConfig.LAYOUT,
        initial_sidebar_state=AppConfig.INITIAL_SIDEBAR_STATE
    )
    
    # Load data
    df_hist, df_proj = load_data()
    logo_base64 = load_image_as_base64(AppConfig.LOGO_PATH)
    
    # Render header
    render_header(logo_base64)
    
    # Render sidebar
    selected_indicator, selected_model, selected_scenarios = render_sidebar(df_hist, df_proj)
    
    # Main content
    if selected_indicator and selected_model and selected_scenarios:
        render_main_content(df_hist, df_proj, selected_indicator, selected_model, selected_scenarios)

# ==============================
# RENDER FUNCTIONS
# ==============================
def render_header(logo_base64: Optional[str] = None) -> None:
    """Render the application header"""
    st.markdown("""
        <style>
            /* Add your CSS styles here */
            .app-header {
                text-align: center;
                margin: 1rem 0 2rem;
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            .app-title {
                margin: 0 0 0.5rem 0;
                font-size: 2.75rem;
                font-weight: 800;
                letter-spacing: -0.5px;
                color: #1e3a5f !important;
            }
            .app-subtitle {
                font-size: 1.2rem;
                margin: 0;
                font-weight: 500;
                letter-spacing: 0.3px;
                color: #475569 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="app-header">
        {f'<img src="data:image/jpeg;base64,{logo_base64}" style="max-width: 250px; height: auto; margin-bottom: 1rem;">' if logo_base64 else ''}
        <h1 class="app-title">Plataforma Prospectiva de Indicadores Institucionales</h1>
        <div style="height: 5px; width: 240px; background: linear-gradient(90deg, #2c5f8d, #4a90c8, #2ecc71); 
             margin: 0 auto 1rem; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
        <p class="app-subtitle">Análisis y proyección de indicadores estratégicos 2026-2030</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(df_hist: pd.DataFrame, df_proj: pd.DataFrame) -> Tuple[str, str, List[str]]:
    """Render the sidebar and return selected options"""
    with st.sidebar:
        st.markdown('<div style="text-align: center; margin-bottom: 1.5rem;"><h2>⚙️ CONTROLES</h2></div>', 
                   unsafe_allow_html=True)
        
        # Linea Estrategica selection
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
        
        # Filter indicators based on selected line
        indicators = get_available_indicators(df_hist, display_name, linea_sel)
        selected_indicator = st.selectbox("📊 Indicador", indicators)
        
        # Model selection
        selected_model = render_model_selection(df_proj, selected_indicator)
        
        # Scenario selection
        selected_scenarios = render_scenario_selection(df_proj, selected_indicator, selected_model)
        
        # Visualization options
        st.markdown("---")
        st.markdown("**📊 Visualización:**")
        tipo_visualizacion = st.selectbox("Periodo", ["Semestral", "Anual"], label_visibility="collapsed")
        mostrar_numeros = st.checkbox("Mostrar valores", value=True)
        mostrar_linea_divisoria = st.checkbox("Línea divisoria", value=True)
        
        # Action buttons
        st.markdown("---")
        if st.button("🔄 REFRESCAR"): 
            st.rerun()
            
        if st.button("📊 MODELOS", use_container_width=True, key="btn_modelos"):
            st.session_state['mostrar_modelos'] = True
            st.rerun()
            
        return selected_indicator, selected_model, selected_scenarios

def render_main_content(df_hist: pd.DataFrame, df_proj: pd.DataFrame, 
                       indicator: str, model: str, scenarios: List[str]) -> None:
    """Render the main content area"""
    # Filter data
    df_hist_sel = filter_historical_data(df_hist, indicator)
    df_proj_sel = filter_projection_data(df_proj, indicator, model, scenarios)
    
    # Calculate metrics
    metrics = calculate_metrics(df_hist_sel, df_proj_sel)
    
    # Display metrics
    display_metrics(metrics)
    
    # Create and display chart
    fig = create_chart(df_hist_sel, df_proj_sel, indicator, model, scenarios)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table
    display_data_table(df_hist_sel, df_proj_sel, indicator, model)

if __name__ == "__main__":
    main()