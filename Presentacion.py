"""
📊 VISUALIZADOR DE PRESENTACIÓN PPTX - MODO PRESENTACIÓN PROFESIONAL
Versión: 1.0 - Opción 4 Full-Screen
Funcionalidad: Experiencia de presentación profesional con controles avanzados
"""

import streamlit as st
from pdf2image import convert_from_path
import subprocess
from pathlib import Path
from PIL import Image
import time

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="Modelos de Pronóstico v7.1",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CSS PERSONALIZADO PARA MODO PRESENTACIÓN
# ============================================================================

st.markdown("""
<style>
    /* Ocultar elementos de Streamlit en modo presentación */
    .presentation-mode .stApp > header {
        display: none;
    }
    
    /* Estilo para el contenedor de slides */
    .slide-container {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Estilo para controles de navegación */
    .nav-controls {
        background: linear-gradient(135deg, #1C2833 0%, #2E4053 100%);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Estilo para botones */
    .stButton > button {
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Estilo para el contador de slides */
    .slide-counter {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #FFFFFF;
        background: linear-gradient(135deg, #F39C12 0%, #E74C3C 100%);
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        margin: 10px 0;
    }
    
    /* Estilo para la barra de progreso */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #F39C12 0%, #E74C3C 100%);
    }
    
    /* Título principal */
    .main-title {
        text-align: center;
        color: #1C2833;
        font-size: 2.8em;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #5D6D7E;
        font-size: 1.3em;
        margin-bottom: 20px;
    }
    
    /* Pantalla de inicio */
    .start-screen {
        background: linear-gradient(135deg, #ECF0F1 0%, #BDC3C7 100%);
        padding: 60px 40px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        text-align: center;
    }
    
    /* Información de slides */
    .slide-info-box {
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Mini-mapa de navegación */
    .mini-map {
        background: #F8F9FA;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #E0E0E0;
    }
    
    /* Animación de slide */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .slide-image {
        animation: slideIn 0.4s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_data(show_spinner=False)
def convert_pptx_to_images(pptx_path):
    """
    Convierte archivo PPTX a lista de imágenes PIL
    
    Args:
        pptx_path (str): Ruta al archivo PPTX
    
    Returns:
        list: Lista de objetos PIL Image
    """
    try:
        # Convertir PPTX a PDF usando LibreOffice
        pdf_path = pptx_path.replace('.pptx', '.pdf')
        
        if not Path(pdf_path).exists():
            result = subprocess.run(
                ['soffice', '--headless', '--convert-to', 'pdf', 
                 '--outdir', str(Path(pptx_path).parent), pptx_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise Exception(f"Error al convertir PPTX: {result.stderr}")
        
        # Convertir PDF a imágenes (alta calidad)
        images = convert_from_path(pdf_path, dpi=200)
        
        return images
        
    except subprocess.TimeoutExpired:
        st.error("❌ Tiempo de conversión excedido")
        return None
    except FileNotFoundError:
        st.error("❌ LibreOffice no instalado. Ejecuta: sudo apt-get install libreoffice")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def get_slide_info(slide_number):
    """
    Obtiene información detallada de cada slide
    
    Args:
        slide_number (int): Número de slide (0-indexed)
    
    Returns:
        dict: Información del slide (título, descripción, categoría)
    """
    slide_data = {
        0: {
            "title": "Portada",
            "description": "Presentación del sistema v7.1",
            "category": "Introducción",
            "icon": "🏠"
        },
        1: {
            "title": "Clasificación de Modelos",
            "description": "Organización de los 9 modelos por tipo",
            "category": "Introducción",
            "icon": "📋"
        },
        2: {
            "title": "Regresión Lineal",
            "description": "Modelo básico de tendencia lineal",
            "category": "Regresión",
            "icon": "📈"
        },
        3: {
            "title": "Polinomial Grado 2",
            "description": "Captura relaciones cuadráticas",
            "category": "Regresión",
            "icon": "📈"
        },
        4: {
            "title": "Polinomial Grado 3",
            "description": "Relaciones cúbicas complejas",
            "category": "Regresión",
            "icon": "📈"
        },
        5: {
            "title": "Random Forest",
            "description": "Ensemble de árboles de decisión",
            "category": "Machine Learning",
            "icon": "🤖"
        },
        6: {
            "title": "Gradient Boosting",
            "description": "Corrección iterativa de errores",
            "category": "Machine Learning",
            "icon": "🤖"
        },
        7: {
            "title": "ARIMA/SARIMAX",
            "description": "Auto-Regressive Integrated Moving Average",
            "category": "Series Temporales",
            "icon": "📊"
        },
        8: {
            "title": "Suavizado Exponencial",
            "description": "Método Holt con tendencia",
            "category": "Series Temporales",
            "icon": "📊"
        },
        9: {
            "title": "Proyección CAGR",
            "description": "Tasa de crecimiento compuesta",
            "category": "Series Temporales",
            "icon": "📊"
        },
        10: {
            "title": "Media Móvil con Tendencia",
            "description": "Promedio móvil + ajuste lineal",
            "category": "Series Temporales",
            "icon": "📊"
        },
        11: {
            "title": "Modelo Ensemble",
            "description": "Promedio de todos los modelos",
            "category": "Ensemble",
            "icon": "🎯"
        },
        12: {
            "title": "Parámetros del Código",
            "description": "Configuración técnica del sistema",
            "category": "Configuración",
            "icon": "⚙️"
        },
        13: {
            "title": "Criterios de Selección",
            "description": "Score multivariado de evaluación",
            "category": "Configuración",
            "icon": "⚙️"
        },
        14: {
            "title": "Resumen Ejecutivo",
            "description": "Síntesis del sistema completo",
            "category": "Conclusión",
            "icon": "✅"
        }
    }
    
    return slide_data.get(slide_number, {
        "title": f"Slide {slide_number + 1}",
        "description": "",
        "category": "General",
        "icon": "📄"
    })

# ============================================================================
# INICIALIZACIÓN DE SESSION STATE
# ============================================================================

if 'presentation_mode' not in st.session_state:
    st.session_state.presentation_mode = False

if 'current_slide' not in st.session_state:
    st.session_state.current_slide = 0

if 'slides' not in st.session_state:
    st.session_state.slides = None

if 'show_minimap' not in st.session_state:
    st.session_state.show_minimap = False

if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

PPTX_PATH = "Modelos_Pronostico_v7.1.pptx"

# Verificar archivo
if not Path(PPTX_PATH).exists():
    st.error(f"❌ Archivo no encontrado: {PPTX_PATH}")
    st.stop()

# ============================================================================
# PANTALLA DE INICIO
# ============================================================================

if not st.session_state.presentation_mode:
    
    # Título principal
    st.markdown('<p class="main-title">📊 Modelos de Pronóstico Multivariable</p>', 
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Versión 7.1 Definitivo - Modo Presentación Profesional</p>', 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contenedor de inicio
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div class="start-screen">
            <h2 style="color: #1C2833; margin-bottom: 30px;">🎯 Presentación Interactiva</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("📑 Total Slides", "15", help="15 slides profesionales")
        
        with metric_col2:
            st.metric("📊 Modelos", "9", help="9 modelos de pronóstico")
        
        with metric_col3:
            file_size = Path(PPTX_PATH).stat().st_size / 1024
            st.metric("💾 Tamaño", f"{file_size:.0f} KB", help="Archivo optimizado")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Contenido
        st.markdown("""
        ### 📋 Contenido de la Presentación
        
        **🎯 Estructura:**
        - **Clasificación:** 4 tipos de modelos
        - **Regresión:** 3 modelos lineales y polinomiales
        - **Machine Learning:** 2 modelos avanzados (RF, GB)
        - **Series Temporales:** 4 modelos especializados
        - **Configuración:** Parámetros y criterios técnicos
        
        **✨ Funcionalidades:**
        - 📱 Navegación intuitiva con controles profesionales
        - 🎯 Acceso rápido con mini-mapa
        - 📊 Indicador visual de progreso
        - ⌨️ Atajos de teclado (flechas ← →)
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón de inicio
        if st.button(
            "▶️ INICIAR PRESENTACIÓN",
            type="primary",
            use_container_width=True,
            key="start_presentation"
        ):
            st.session_state.presentation_mode = True
            st.session_state.current_slide = 0
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Tip:** Usa las flechas ← → del teclado para navegar entre slides")

# ============================================================================
# MODO PRESENTACIÓN
# ============================================================================

else:
    
    # Cargar slides si no están en cache
    if st.session_state.slides is None:
        with st.spinner("🔄 Preparando presentación... Por favor espera"):
            st.session_state.slides = convert_pptx_to_images(PPTX_PATH)
            
            if st.session_state.slides is None:
                st.error("❌ No se pudo cargar la presentación")
                st.stop()
    
    slides = st.session_state.slides
    total_slides = len(slides)
    current = st.session_state.current_slide
    
    # Información del slide actual
    slide_info = get_slide_info(current)
    progress = (current + 1) / total_slides
    
    # ========================================================================
    # BARRA SUPERIOR DE CONTROLES
    # ========================================================================
    
    st.markdown('<div class="nav-controls">', unsafe_allow_html=True)
    
    control_col1, control_col2, control_col3, control_col4, control_col5, control_col6, control_col7 = st.columns([1, 1, 3, 1, 1, 1, 1])
    
    with control_col1:
        if st.button("⏮️", help="Primer slide", key="first", use_container_width=True):
            st.session_state.current_slide = 0
            st.rerun()
    
    with control_col2:
        if st.button("◀️", help="Anterior", key="prev", use_container_width=True):
            if current > 0:
                st.session_state.current_slide -= 1
                st.rerun()
    
    with control_col3:
        # Barra de progreso con información
        st.progress(progress)
        st.markdown(f"""
        <div class="slide-counter">
            {slide_info['icon']} Slide {current + 1} de {total_slides} | {slide_info['category']}
        </div>
        """, unsafe_allow_html=True)
    
    with control_col4:
        if st.button("▶️", help="Siguiente", key="next", use_container_width=True):
            if current < total_slides - 1:
                st.session_state.current_slide += 1
                st.rerun()
    
    with control_col5:
        if st.button("⏭️", help="Último slide", key="last", use_container_width=True):
            st.session_state.current_slide = total_slides - 1
            st.rerun()
    
    with control_col6:
        minimap_label = "🗺️" if not st.session_state.show_minimap else "📄"
        minimap_help = "Mostrar mini-mapa" if not st.session_state.show_minimap else "Ocultar mini-mapa"
        if st.button(minimap_label, help=minimap_help, key="minimap", use_container_width=True):
            st.session_state.show_minimap = not st.session_state.show_minimap
            st.rerun()
    
    with control_col7:
        if st.button("❌", help="Salir", key="exit", use_container_width=True):
            st.session_state.presentation_mode = False
            st.session_state.current_slide = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # INFORMACIÓN DEL SLIDE
    # ========================================================================
    
    st.markdown(f"""
    <div class="slide-info-box">
        <h3 style="margin: 0; color: white;">
            {slide_info['icon']} {slide_info['title']}
        </h3>
        <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.95em;">
            {slide_info['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # MOSTRAR SLIDE ACTUAL
    # ========================================================================
    
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown('<div class="slide-image">', unsafe_allow_html=True)
    st.image(slides[current], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # MINI-MAPA DE NAVEGACIÓN
    # ========================================================================
    
    if st.session_state.show_minimap:
        st.markdown("---")
        st.markdown('<div class="mini-map">', unsafe_allow_html=True)
        st.subheader("🗺️ Navegación Rápida")
        
        # Organizar en filas de 5 columnas
        for row_start in range(0, total_slides, 5):
            cols = st.columns(5)
            
            for col_idx, col in enumerate(cols):
                slide_idx = row_start + col_idx
                
                if slide_idx < total_slides:
                    with col:
                        info = get_slide_info(slide_idx)
                        is_current = (slide_idx == current)
                        
                        # Botón con indicador visual
                        button_label = f"{info['icon']} {slide_idx + 1}"
                        if is_current:
                            button_label = f"▶️ {slide_idx + 1}"
                        
                        button_type = "primary" if is_current else "secondary"
                        
                        if st.button(
                            button_label,
                            key=f"nav_{slide_idx}",
                            type=button_type,
                            use_container_width=True,
                            help=info['title']
                        ):
                            st.session_state.current_slide = slide_idx
                            st.rerun()
                        
                        # Miniatura
                        thumb = slides[slide_idx].copy()
                        thumb.thumbnail((150, 100))
                        st.image(thumb, use_container_width=True)
                        
                        # Título pequeño
                        st.caption(f"**{info['title']}**")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # NAVEGACIÓN CON TECLADO (JavaScript)
    # ========================================================================
    
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(event) {
        // Prevenir comportamiento por defecto de las flechas
        if(['ArrowLeft', 'ArrowRight'].includes(event.key)) {
            event.preventDefault();
        }
        
        if (event.key === 'ArrowRight') {
            // Simular clic en botón siguiente
            const nextButton = window.parent.document.querySelector('[data-testid="stButton"]:has([key="next"])');
            if(nextButton) nextButton.click();
        } else if (event.key === 'ArrowLeft') {
            // Simular clic en botón anterior
            const prevButton = window.parent.document.querySelector('[data-testid="stButton"]:has([key="prev"])');
            if(prevButton) prevButton.click();
        } else if (event.key === 'Escape') {
            // Salir con ESC
            const exitButton = window.parent.document.querySelector('[data-testid="stButton"]:has([key="exit"])');
            if(exitButton) exitButton.click();
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # INSTRUCCIONES DE NAVEGACIÓN
    # ========================================================================
    
    st.markdown("---")
    
    help_col1, help_col2, help_col3 = st.columns(3)
    
    with help_col1:
        st.info("⌨️ **Atajos:** ← Anterior | → Siguiente | ESC Salir")
    
    with help_col2:
        st.success(f"📊 **Progreso:** {(progress*100):.0f}% completado")
    
    with help_col3:
        remaining = total_slides - current - 1
        st.warning(f"📑 **Restantes:** {remaining} slides")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #95A5A6; font-size: 0.9em; padding: 10px;'>
    📊 Sistema de Pronóstico v7.1 | Modo Presentación Profesional | Noviembre 2025
</div>
""", unsafe_allow_html=True)