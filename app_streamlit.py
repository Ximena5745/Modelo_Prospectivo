import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np 
import os 

# ==============================
# CONFIGURACIÓN STREAMLIT
# ==============================
st.set_page_config(
    page_title="Modelo Prospectivo Poli 2026-2030",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# ESTILOS CSS
# ==============================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #f8fafc; color: #1e293b; }
        .stApp { background-color: #f8fafc; }
        .main .block-container { padding: 2rem 3rem; max-width: 1800px; }
        h1 { color: #0d47a1; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
        h2 { color: #1a73e8; font-size: 1.75rem; font-weight: 600; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 3px solid #e3f2fd; }
        h3 { color: #1557b0; font-size: 1.25rem; font-weight: 600; margin: 1.5rem 0 0.75rem 0; }
        /* Estilos del Sidebar */
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%); padding: 1.5rem 1rem; }
        [data-testid="stSidebar"] * { color: white !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: white !important; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem; margin-bottom: 1rem; }
        /* Estilos de Botones y Selectores */
        .stButton > button { background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%); color: white !important; border: none; border-radius: 8px; padding: 0.75rem 1.5rem; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3); transition: all 0.3s ease; width: 100%; }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(26, 115, 232, 0.4); }
        .stSelectbox label, .stCheckbox label { font-weight: 500; font-size: 0.9rem; color: #475569; }
        [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stCheckbox label { color: white !important; }
        .stSelectbox > div { border-radius: 8px; border: 1px solid #cbd5e0; background: white; transition: all 0.2s ease; }
        .stSelectbox > div:focus-within { border-color: #1a73e8; box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.1); }
        .metric-card { background: white; border-radius: 10px; padding: 1.5rem; border-left: 4px solid #1a73e8; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; }
        .metric-card:hover { transform: translateY(-4px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
        .metric-label { color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
        .metric-value { color: #0d47a1; font-size: 2rem; font-weight: 700; line-height: 1; }
        .stPlotlyChart { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow: hidden; margin: 1.5rem 0; }
        /* Estilos específicos para el botón de descarga */
        [data-testid="stDownloadButton"] > button {
            background-color: #2ecc71; 
            border-left: 4px solid #27ae60;
            color: white !important;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3) !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 1.5rem 0 2.5rem 0;">
    <h1 style="margin: 0 0 0.5rem 0; color: #0d47a1 !important; font-size: 2.75rem; font-weight: 800; letter-spacing: -0.5px;">MODELO DE PROSPECTIVA POLI</h1>
    <div style="height: 5px; width: 240px; background: linear-gradient(90deg, #1a73e8, #2ecc71); margin: 0 auto 1rem; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
    <p style="color: #475569; font-size: 1.2rem; margin: 0.5rem 0 0 0; font-weight: 500; letter-spacing: 0.3px;">Plataforma de análisis y proyección de indicadores estratégicos 2026-2030</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# LECTURA DE DATOS (Con simulación de fallback)
# ==============================
BASE_DIR = Path(__file__).parent
RUTA_DATASET = BASE_DIR / "Data" / "Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx"

# Validar existencia de archivos y leer con manejo de errores explícito
if not RUTA_DATASET.exists():
    st.error(f"No se encontró el archivo histórico: {RUTA_DATASET}")
    st.stop()
if not RUTA_PROYECCIONES.exists():
    st.error(f"No se encontró el archivo de proyecciones: {RUTA_PROYECCIONES}")
    st.stop()

try:
    df_hist = pd.read_excel(str(RUTA_DATASET))
    # Normalizar columna de fecha histórica
    if 'Fecha' not in df_hist.columns:
        posibles_fechas = [c for c in df_hist.columns if str(c).strip().lower().replace(' ', '_') in [
            'fecha', 'periodo', 'periodo_fecha']]
        if posibles_fechas:
            df_hist = df_hist.rename(columns={posibles_fechas[0]: 'Fecha'})
    df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"], errors='coerce')

    # Leer todas las hojas del archivo de proyecciones y concatenar
    _sheets = pd.read_excel(str(RUTA_PROYECCIONES), sheet_name=None)
    if isinstance(_sheets, dict):
        df_proj_raw = pd.concat(_sheets.values(), ignore_index=True)
    else:
        df_proj_raw = _sheets
    # Normalización de nombres de columnas (case-insensitive y con/ sin acentos)
    colmap = {str(c): str(c).strip().lower().replace(' ', '_').replace('ó', 'o').replace('é', 'e').replace('á', 'a').replace('í','i').replace('ú','u') for c in df_proj_raw.columns}
    df_proj_raw.columns = list(colmap.values())

    # Mapear a nombres esperados
    rename_rules = {}
    # fecha proyeccion
    for cand in ['fecha_proyeccion', 'fecha_proyecccion', 'fecha', 'fecha_proyeccion_']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Fecha_Proyeccion'
            break
    # indicador
    for cand in ['indicador']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Indicador'
            break
    # modelo
    for cand in ['modelo', 'metodo', 'modelo_ml']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Modelo'
            break
    # periodicidad
    for cand in ['periodicidad']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Periodicidad'
            break
    # escenarios
    # Compatibilidad con estructura anterior
    if 'escenario_base' in df_proj_raw.columns: rename_rules['escenario_base'] = 'Escenario_Base'
    if 'escenario_pesimista' in df_proj_raw.columns: rename_rules['escenario_pesimista'] = 'Escenario_Pesimista'
    if 'escenario_optimista' in df_proj_raw.columns: rename_rules['escenario_optimista'] = 'Escenario_Optimista'
    # Nueva estructura: Proyeccion, IC_Inferior, IC_Superior
    if 'proyeccion' in df_proj_raw.columns: rename_rules['proyeccion'] = 'Escenario_Base'
    if 'ic_inferior' in df_proj_raw.columns: rename_rules['ic_inferior'] = 'Escenario_Pesimista'
    if 'ic_superior' in df_proj_raw.columns: rename_rules['ic_superior'] = 'Escenario_Optimista'

    if rename_rules:
        df_proj_raw = df_proj_raw.rename(columns=rename_rules)

    # Validar columnas requeridas
    required = {'Indicador', 'Modelo', 'Fecha_Proyeccion', 'Escenario_Base', 'Escenario_Pesimista', 'Escenario_Optimista'}
    missing = [c for c in required if c not in df_proj_raw.columns]
    if missing:
        st.error(f"Faltan columnas requeridas en Proyecciones_Multimodelo.xlsx: {missing}. Verifique nombres.")
        st.stop()

    df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"], errors='coerce')
    if df_proj_raw["Fecha_Proyeccion"].isna().all():
        st.error("No se pudieron parsear las fechas en 'Fecha_Proyeccion'. Revise el formato de la columna en Proyecciones_Multimodelo.xlsx")
        st.stop()
except Exception as e:
    st.exception(e)
    st.stop()


df_proj_list = []
if not df_proj_raw.empty:
    for _, row in df_proj_raw.iterrows():
        base_data = {'Indicador': row['Indicador'], 'Periodicidad': row.get('Periodicidad', 'Semestral'), 'Fecha': row['Fecha_Proyeccion'], 'Modelo': row['Modelo']}
        if pd.notna(row.get('Escenario_Base')): df_proj_list.append({**base_data, 'Escenario': 'Base', 'Proyección': row['Escenario_Base']})
        if pd.notna(row.get('Escenario_Pesimista')): df_proj_list.append({**base_data, 'Escenario': 'Pesimista', 'Proyección': row['Escenario_Pesimista']})
        if pd.notna(row.get('Escenario_Optimista')): df_proj_list.append({**base_data, 'Escenario': 'Optimista', 'Proyección': row['Escenario_Optimista']})

df_proj = pd.DataFrame(df_proj_list) if df_proj_list else pd.DataFrame()
# Garantizar columnas esperadas aunque esté vacío
expected_proj_cols = ['Indicador', 'Periodicidad', 'Fecha', 'Modelo', 'Escenario', 'Proyección']
for c in expected_proj_cols:
    if c not in df_proj.columns:
        df_proj[c] = pd.Series(dtype='object')

# ==============================
# SIDEBAR
# ==============================
# ==============================
# ORDEN MANUAL DE INDICADORES POR LÍNEA ESTRATÉGICA
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
        "Nivel de Satisfacción Servicios Prestados - Comunicaciones Internas"    ]
}

with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 1.5rem;"><h2>⚙️ CONTROLES</h2></div>', unsafe_allow_html=True)
    
    lineas_estrategicas = {"Expansión": ("Expansión", "#1a73e8"), "Transformación Organizacional": ("Transformación_Organizacional", "#1557b0"), "Calidad": ("Calidad", "#0d47a1"), "Experiencia": ("Experiencia", "#1976d2"), "Sostenibilidad": ("Sostenibilidad", "#2196f3"), "Educación para la vida": ("Educación_para_toda_la_vida", "#1565c0")}
    
    linea_sel = st.selectbox("🎯 Línea Estratégica", list(lineas_estrategicas.keys()))
    display_name, color_linea = lineas_estrategicas[linea_sel]
    
    # Lógica de filtrado de indicadores 
    if 'Linea' in df_hist.columns:
        df_hist_filtrado = df_hist[df_hist["Linea"] == display_name]
        if df_hist_filtrado.empty: df_hist_filtrado = df_hist[df_hist["Linea"].str.replace('_', ' ') == linea_sel]
        if df_hist_filtrado.empty: df_hist_filtrado = df_hist
        
        # Obtener indicadores disponibles en los datos
        indicadores_disponibles = set(df_hist_filtrado["Indicador"].unique())
        
        # Usar el orden manual si está definido para esta línea
        orden_manual = ORDEN_INDICADORES.get(display_name, [])
        if orden_manual:
            # Filtrar solo los indicadores que existen en los datos y mantener el orden
            indicadores = [ind for ind in orden_manual if ind in indicadores_disponibles]
            # Agregar cualquier indicador que esté en los datos pero no en el orden manual
            indicadores_faltantes = sorted(indicadores_disponibles - set(indicadores))
            indicadores.extend(indicadores_faltantes)
        else:
            indicadores = sorted(indicadores_disponibles)
    else:
        indicadores = sorted(df_hist["Indicador"].unique())
    
    indicador_sel = st.selectbox("📊 Indicador", indicadores)
    
    # Modelos ML: mostrar solo los que tengan datos para el indicador seleccionado
    modelos = []
    if isinstance(df_proj, pd.DataFrame) and not df_proj.empty and {'Modelo','Indicador'}.issubset(df_proj.columns):
        modelos = sorted(
            df_proj[df_proj['Indicador'] == indicador_sel]['Modelo']
            .dropna().astype(str).unique()
        )
    # Mapas de nombres bonitos (se amplía automáticamente con fallback al nombre original)
    modelo_display_names = {
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
    if modelos:
        modelo_options = [modelo_display_names.get(m, m) for m in modelos]
        modelo_display_sel = st.selectbox("🧠 Modelo ML", modelo_options)
        # Resolver a la clave original si el usuario eligió un alias bonito
        inv_map = {v: k for k, v in modelo_display_names.items()}
        modelo_sel = inv_map.get(modelo_display_sel, modelo_display_sel)
    else:
        st.warning("No hay proyecciones disponibles para este indicador en el archivo de proyecciones.")
        modelo_sel = ""
    
    # Escenarios 
    escenarios_disponibles = ['Base', 'Pesimista', 'Optimista']
    if modelo_sel and not df_proj.empty and modelo_sel in df_proj["Modelo"].unique():
        escenarios_modelo = df_proj[(df_proj["Modelo"] == modelo_sel) & (df_proj["Indicador"] == indicador_sel)]["Escenario"].unique()
        escenarios_disponibles = [e for e in escenarios_disponibles if e in escenarios_modelo]
    
    st.markdown("**🌍 Escenarios:**")
    escenarios_sel = []
    escenario_icons = {'Base': '⚖️', 'Pesimista': '📉', 'Optimista': '📈'}
    for escenario in escenarios_disponibles:
        icon = escenario_icons.get(escenario, '🌍')
        # Seleccionar TODOS por defecto para asegurar visualización
        default_value = True
        if st.checkbox(f"{icon} {escenario}", value=default_value, key=f"esc_{escenario}"):
            escenarios_sel.append(escenario)
    # Si el usuario desmarca todo, usar todos por defecto para no dejar la gráfica vacía
    if not escenarios_sel:
        escenarios_sel = escenarios_disponibles[:]
    
    st.markdown("---")
    st.markdown("**📊 Visualización:**")
    tipo_visualizacion = st.selectbox("Periodo", ["Semestral", "Anual"], label_visibility="collapsed")
    mostrar_numeros = st.checkbox("Mostrar valores", value=True)
    mostrar_linea_divisoria = st.checkbox("Línea divisoria", value=True)
    st.markdown("---")
    if st.button("🔄 REFRESCAR"): st.rerun()

# ==============================
# FILTRAR DATOS
# ==============================
if 'Linea' in df_hist.columns:
    df_hist_sel = df_hist[(df_hist["Indicador"] == indicador_sel) & (df_hist["Linea"] == display_name)]
    if df_hist_sel.empty: df_hist_sel = df_hist[(df_hist["Indicador"] == indicador_sel) & (df_hist["Linea"].str.replace('_', ' ') == linea_sel)]
else:
    df_hist_sel = df_hist[df_hist["Indicador"] == indicador_sel]

# No filtrar los datos históricos por fecha para mantener todos los datos disponibles
# Filtrar solo por indicador y línea estratégica

# Filtrar proyecciones sin restricción de fecha para asegurar que se muestren todas las disponibles
df_proj_sel = df_proj[
    (df_proj["Indicador"] == indicador_sel) & 
    (df_proj["Modelo"] == modelo_sel) & 
    (df_proj["Escenario"].isin(escenarios_sel))
].copy()  # Usar copy() para evitar SettingWithCopyWarning

# Asegurarse de que las fechas sean datetime
df_proj_sel['Fecha'] = pd.to_datetime(df_proj_sel['Fecha'])

# Ordenar por fecha para asegurar el orden correcto
df_proj_sel = df_proj_sel.sort_values('Fecha')

# ==============================
# FUNCIONES AUXILIARES
# ==============================
@st.cache_data
def convert_df_to_csv(df):
    """Convierte el DataFrame a una cadena CSV para descarga."""
    # Usamos punto y coma como separador y codificación utf-8 para manejar caracteres especiales.
    return df.to_csv(index=False, sep=';').encode('utf-8')

def format_number(value, decimals):
    if pd.isna(value): return ''
    try:
        decimals = int(decimals) if pd.notna(decimals) else 0
        return f"{float(value):,.{decimals}f}"
    except:
        return str(value)

# --- Utilidades para etiquetas y rangos de período ---
def periodo_label(fecha, tipo: str) -> str:
    """Genera etiqueta de rango para un período.
    Semestral: 'YYYY-01 a YYYY-06' o 'YYYY-07 a YYYY-12'
    Anual: 'YYYY-01 a YYYY-12'
    """
    if pd.isna(fecha):
        return ''
    f = pd.to_datetime(fecha)
    y = int(f.year)
    if tipo == "Semestral":
        return f"{y}-01 a {y}-06" if f.month <= 6 else f"{y}-07 a {y}-12"
    return f"{y}-01 a {y}-12"

def periodos_rango_por_ano(year: int, tipo: str):
    """Devuelve lista de tuplas (x0, x1) para bandas de fondo por año."""
    if tipo == "Semestral":
        return [
            (pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year, month=6, day=30)),
            (pd.Timestamp(year=year, month=7, day=1), pd.Timestamp(year=year, month=12, day=31)),
        ]
    return [
        (pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year, month=12, day=31)),
    ]

decimal_places = 0
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

# Determinar si el indicador tiene sentido negativo usando la columna 'Sentido' del dataset
if 'Sentido' in df_hist_sel.columns and not df_hist_sel.empty:
    # Verificar si el indicador tiene sentido negativo según la columna 'Sentido'
    sentido = df_hist_sel['Sentido'].iloc[0] if not df_hist_sel.empty else 'Positivo'
    indicador_negativo = str(sentido).strip().lower() == 'negativo'
else:
    # Si no existe la columna 'Sentido', asumir que es positivo por defecto
    indicador_negativo = False
    print("Advertencia: No se encontró la columna 'Sentido' en los datos históricos")

# Para depuración: mostrar el sentido del indicador
print(f"Indicador: {indicador_sel}")
print(f"Sentido del indicador: {'Negativo' if indicador_negativo else 'Positivo'}")

# Determinar colores de los escenarios basados en el sentido del indicador
if indicador_negativo:
    print("Usando colores para indicador con sentido negativo (menor es mejor)")
    # Para indicadores negativos: Optimista (valores bajos) = Verde, Pesimista (valores altos) = Rojo
    colores_escenarios = {
        'Optimista': '#2ecc71',  # Verde (mejor escenario: valores más bajos)
        'Base': '#1a73e8',       # Azul (neutral)
        'Pesimista': '#e74c3c',  # Rojo (peor escenario: valores más altos)
        'Histórico Semestral': '#5c8bf2',
        'Histórico Anual': '#5c8bf2'
    }
else:
    print("Usando colores estándar para indicador con sentido positivo (mayor es mejor)")
    # Colores estándar para indicadores donde mayor es mejor
    colores_escenarios = {
        'Optimista': '#2ecc71',  # Verde (mejor escenario)
        'Base': '#1a73e8',       # Azul (neutral)
        'Pesimista': '#e74c3c',  # Rojo (peor escenario)
        'Histórico Semestral': '#5c8bf2',
        'Histórico Anual': '#5c8bf2'
    }

# ==============================
# TARJETAS DE RESUMEN
# ==============================

# Se busca el escenario base directamente para el modelo e indicador,
# sin depender del filtro 'escenarios_sel' del usuario, asegurando que se muestre el resumen si el dato existe.
df_base = df_proj[(df_proj["Indicador"] == indicador_sel) & (df_proj["Modelo"] == modelo_sel) & (df_proj["Escenario"] == 'Base')]

if not df_base.empty:
    # Obtener el valor de proyección para 2026 y 2030 (el último registro de ese año)
    valor_2026 = df_base[df_base['Fecha'].dt.year == 2026]['Proyección'].max()
    valor_2030 = df_base[df_base['Fecha'].dt.year == 2030]['Proyección'].max()
    ultimo_historico = df_hist_sel['Ejecución'].max() if not df_hist_sel.empty else np.nan
    
    variacion_periodo = valor_2030 - valor_2026 if pd.notna(valor_2030) and pd.notna(valor_2026) else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="metric-card" style="border-left-color: #2ecc71;"><div class="metric-label">📈 ÚLTIMO HISTÓRICO</div><div class="metric-value" style="color: #1e293b;">{format_number(ultimo_historico, decimal_places)}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #1a73e8;"><div class="metric-label">🎯 PROYECCIÓN (2026)</div><div class="metric-value" style="color: #1a73e8;">{format_number(valor_2026, decimal_places)}</div></div>', unsafe_allow_html=True)
    with col3:
        delta_color = "#2ecc71" if variacion_periodo > 0 else ("#e74c3c" if variacion_periodo < 0 else "#f1c40f")
        st.markdown(f'<div class="metric-card" style="border-left-color: #f39c12;"><div class="metric-label">⭐ PROYECCIÓN (2030)</div><div class="metric-value" style="color: #f39c12; margin-bottom: 0.25rem;">{format_number(valor_2030, decimal_places)}</div><div style="color: {delta_color}; font-size: 1rem; font-weight: 600; margin-top: 0.25rem;">Δ {valor_2030 - valor_2026:+,.{int(decimal_places)}f}</div></div>', unsafe_allow_html=True)
    with col4:
        if variacion_periodo > 0: tendencia, icon_tend, color_tend = "Creciente", "🟢", "#2ecc71"
        elif variacion_periodo < 0: tendencia, icon_tend, color_tend = "Decreciente", "🔴", "#e74c3c"
        else: tendencia, icon_tend, color_tend = "Estable", "🟡", "#f1c40f"
        st.markdown(f'<div class="metric-card" style="border-left-color: {color_tend};"><div class="metric-label">📊 TENDENCIA PERIODO</div><div style="font-size: 2rem; margin: 0.5rem 0;">{icon_tend}</div><div style="color: {color_tend}; font-size: 1.1rem; font-weight: 700;">{tendencia}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
else:
    # Mensaje de advertencia si no se encuentran datos para el Escenario Base
    st.warning(f"⚠️ Las tarjetas de resumen están ocultas: No se encontraron datos para el **Escenario Base** del indicador **{indicador_sel}** usando el modelo **{modelo_sel}** en su archivo de proyecciones.")
    st.markdown("<br>", unsafe_allow_html=True)


# ==============================
# GRÁFICO (CON CORRECCIÓN DE FILTRO ANUAL)
# ==============================
st.subheader("Evolución Histórica y Proyección Detallada")

df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"].copy()
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"].copy()

# Ajustar fechas históricas al punto medio del período
if tipo_visualizacion == "Semestral" and not df_hist_semestral.empty:
    df_hist_semestral['Fecha'] = df_hist_semestral['Fecha'].apply(
        lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
    )
if tipo_visualizacion == "Anual" and not df_hist_anual.empty:
    df_hist_anual['Fecha'] = df_hist_anual['Fecha'].apply(
        lambda x: pd.Timestamp(year=x.year, month=6, day=30)
    )

fig = go.Figure()

# Agregar históricos (Lógica simplificada por periodicidad)
df_hist_trace = df_hist_semestral if tipo_visualizacion == "Semestral" else df_hist_anual
# Fallback: si no hay datos en la periodicidad elegida, usar cualquier histórico disponible
if df_hist_trace.empty:
    df_hist_trace = df_hist_anual if not df_hist_anual.empty else df_hist_semestral
if df_hist_trace.empty:
    df_hist_trace = df_hist_sel.copy()
    # Ajustar fechas del fallback
    if tipo_visualizacion == "Semestral":
        df_hist_trace['Fecha'] = df_hist_trace['Fecha'].apply(
            lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
        )
    else:
        df_hist_trace['Fecha'] = df_hist_trace['Fecha'].apply(
            lambda x: pd.Timestamp(year=x.year, month=6, day=30)
        )
trace_name = "Histórico Semestral" if tipo_visualizacion == "Semestral" else "Histórico Anual"

if not df_hist_trace.empty:
    fig.add_trace(go.Scatter(x=df_hist_trace["Fecha"], y=df_hist_trace["Ejecución"], name=trace_name, line=dict(color='#D4A017', width=2.5), marker=dict(size=8, color='#D4A017', line=dict(width=1, color='white')), mode='lines+markers', hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'))
    
    # Añadir anotación para explicar la inversión de colores si es un indicador negativo
    if 'indicador_negativo' in locals() and indicador_negativo:
        fig.add_annotation(
            x=0.98,
            y=0.92,
            xref='paper',
            yref='paper',
            text="<i>Nota: Los colores están invertidos (menor = mejor)</i>",
            showarrow=False,
            font=dict(size=12, color="#666666"),
            align="right"
        )
    if mostrar_numeros:
        text_values = df_hist_trace["Ejecución"].apply(lambda x: format_number(x, decimal_places))
        fig.add_trace(go.Scatter(
            x=df_hist_trace["Fecha"], 
            y=df_hist_trace["Ejecución"], 
            mode="text", 
            text=text_values, 
            textposition="top center", 
            textfont=dict(
                size=14, 
                color='#D4A017', 
                family="Poppins",
                weight="bold"
            ),
            showlegend=False, 
            hoverinfo='skip',
            texttemplate='%{text}',
            cliponaxis=False
        ))

# Agregar proyecciones
for escenario in escenarios_sel:
    df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    if not df_esc.empty:
        color = colores_escenarios.get(escenario, '#1a73e8')
        
        df_plot = df_esc.copy()
        
        # Ajustar fechas de proyección al punto medio del período
        if tipo_visualizacion == "Semestral":
            df_plot['Fecha'] = df_plot['Fecha'].apply(
                lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
            )
        else:  # Anual
            # Agrupar por año y tomar el último valor
            df_plot['Año'] = df_plot['Fecha'].dt.year
            df_plot = df_plot.sort_values('Fecha').groupby('Año').last().reset_index()
            # Ajustar al punto medio del año
            df_plot['Fecha'] = df_plot['Año'].apply(lambda y: pd.Timestamp(year=y, month=6, day=30))
        
        df_plot = df_plot.sort_values('Fecha')
        
        if not df_plot.empty:
            fig.add_trace(go.Scatter(x=df_plot["Fecha"], y=df_plot["Proyección"], name=escenario + (" (Anual)" if tipo_visualizacion == "Anual" else ""), line=dict(color=color, width=2.5, dash='dot'), marker=dict(size=8, color=color, line=dict(width=1, color='white')), mode='lines+markers', hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'))
            if mostrar_numeros:
                text_values = df_plot["Proyección"].apply(lambda x: format_number(x, decimal_places))
                fig.add_trace(go.Scatter(
                    x=df_plot["Fecha"], 
                    y=df_plot["Proyección"], 
                    mode="text", 
                    text=text_values, 
                    textposition="top center", 
                    textfont=dict(
                        size=14, 
                        color=color, 
                        family="Poppins",
                        weight="bold"
                    ),
                    showlegend=False, 
                    hoverinfo='skip',
                    texttemplate='%{text}',
                    cliponaxis=False
                ))

# Línea divisoria (Separada para evitar TypeError)
if mostrar_linea_divisoria:
    # Posicionar la línea exactamente entre 2025-S2 y 2026-S1 (31 de diciembre de 2025)
    fecha_corte = pd.Timestamp(year=2025, month=12, day=31)
    fecha_corte_str = fecha_corte.strftime('%Y-%m-%d')

    # 1. Añadir la línea vertical (SOLO LA LÍNEA)
    fig.add_vline(
        x=fecha_corte_str, 
        line_width=2, 
        line_dash="dash", 
        line_color="#808080"
    )
    
    # 2. Añadir la anotación por separado
    fig.add_annotation(
        x=fecha_corte_str, 
        y=1,               
        xref="x",          
        yref="paper",      
        text="Inicio Proyección",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        font=dict(color="#808080", size=12, weight="bold"),
        yshift=-10 
    )


# Configuración del formato de fechas para el eje X (YYYY-S#)
tickvals = []
ticktext = []
years = []

# Obtener el rango de años de los datos históricos y de proyección
hist_years = sorted(df_hist_sel['Fecha'].dt.year.unique()) if not df_hist_sel.empty else []
proj_years = sorted(df_proj_sel['Fecha'].dt.year.unique()) if not df_proj_sel.empty else []
all_years = sorted(set(hist_years + proj_years))

# Asegurar que tenemos al menos desde 2022 hasta 2030
if all_years:
    min_year = min(min(all_years), 2022)
    max_year = max(max(all_years), 2030)
    all_years = list(range(min_year, max_year + 1))
else:
    all_years = list(range(2022, 2031))

if tipo_visualizacion == "Semestral":
    # Para vista semestral, generamos etiquetas S1 (ene-jun) y S2 (jul-dic)
    for year in all_years:
        # S1: enero a junio (punto medio 15 de marzo)
        tickvals.append(f"{year}-03-15")
        ticktext.append(f"{year}-S1")
        
        # S2: julio a diciembre (punto medio 15 de septiembre)
        tickvals.append(f"{year}-09-15")
        ticktext.append(f"{year}-S2")
        
elif tipo_visualizacion == "Anual":
    # Para vista anual, mostramos el año centrado
    for year in all_years:
        tickvals.append(f"{year}-06-30")  # Punto medio del año
        ticktext.append(str(year))


# Bandas de fondo alternadas por período
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

# Actualizar el layout del gráfico
fig.update_layout(
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    height=900,
    font=dict(family="Poppins", size=22, color="#1e293b"),
    
    # Título principal (nombre del indicador)
    title=dict(
        text=f"<b>{indicador_sel}</b>",
        x=0.5,   # Centrado
        y=0.98,  # Cerca del borde superior
        xanchor='center',
        yanchor='top',
        font=dict(size=24, color="#0d47a1", family="Poppins", weight="bold")
    ),
    # Subtítulo (Evolución Histórica y Proyección)
    annotations=[
        dict(
            text="Evolución Histórica y Proyección",
            x=0.02,  # Alineado a la izquierda
            y=0.93,  # Debajo del título principal
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=18, color="#4a5568", family="Poppins")
        ),
        # Modelo en la parte superior derecha, fuera del área del gráfico
        dict(
            text=f"Modelo: {modelo_sel}",
            x=1.02,  # Fuera del área del gráfico (más de 1.0)
            y=1.0,   # Parte superior
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=14, color="#718096", family="Poppins", style="italic"),
            align="left",
            xanchor="left",
            yanchor="top"
        )
    ],
    hovermode='x unified',
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.95)", bordercolor="#cbd5e0", borderwidth=1.5,
        font=dict(size=16, family="Poppins", color="#1e293b", weight=500),
        itemsizing='constant', itemclick=False, itemdoubleclick=False
    ),
    # Ajustar el espaciado para las etiquetas
    
    # ETIQUETAS EJE X: Formato YYYY-S# y Rotación
    xaxis=dict(
        title=dict(
            text="<b>PERIODO</b>",
            font=dict(size=20, weight=600, family="Poppins", color="#1e293b"),
            standoff=15
        ),
        showgrid=True, 
        gridcolor='rgba(0,0,0,0.05)', 
        gridwidth=1,
        tickvals=tickvals,
        ticktext=ticktext, 
        tickfont=dict(size=16, family="Poppins", color="#4a5568", weight=500),
        linecolor='#cbd5e0', 
        linewidth=2, 
        mirror=True, 
        showline=True, 
        automargin=True,
        tickangle=45 if tipo_visualizacion == "Semestral" else 0,
        title_standoff=20,
        fixedrange=True,
        # Ajustar márgenes para etiquetas rotadas
        ticklabeloverflow='allow',
        ticklabelposition='outside',
        ticklabelstep=1 if tipo_visualizacion == "Anual" else 2,
        range=["2021-07-01", "2030-12-31"]
    ),
    
    # ETIQUETAS EJE Y
    yaxis=dict(
        title=dict(
            text=f"<b>{indicador_sel.upper()}</b>",
            font=dict(size=20, weight=600, family="Poppins", color="#1e293b"),
            standoff=15
        ),
        showgrid=True, 
        gridcolor='rgba(0,0,0,0.05)', 
        gridwidth=1,
        tickformat=f",.{int(decimal_places)}f",
        tickfont=dict(size=16, family="Poppins", color="#4a5568"),
        title_standoff=20,
        showline=True,
        linecolor='#cbd5e0',
        linewidth=2,
        mirror=True,
        zeroline=False, 
        automargin=True
    ),
    hoverlabel=dict(
        bgcolor="white", 
        font_size=22, 
        font_family="Poppins", 
        bordercolor="#cbd5e0", 
        namelength=-1,
        align="left"
    ),
    # Ajustar el espaciado para las etiquetas
    margin=dict(t=100, b=100, l=140, r=250, pad=15),  # Aumentado el margen derecho para el modelo
    shapes=shapes
)  # Cierre de update_layout

# Mostrar la gráfica
st.plotly_chart(fig, use_container_width=True)

# ==============================
# COMPARATIVO DE ESCENARIOS (2026 vs 2030)
# ==============================
if not df_proj_sel.empty and len(escenarios_sel) > 0:
    st.markdown("### Comparativo de Escenarios (vs Último 2025)")

    # Preparar columnas dinámicas según escenarios seleccionados
    num_cols = max(1, len(escenarios_sel))
    cols = st.columns(num_cols)

    # Baseline: último histórico de 2025; si no hay, usar último de 2024; si tampoco hay, último <= 2025
    base_2025 = np.nan
    if not df_hist_sel.empty:
        hist_2025 = df_hist_sel[df_hist_sel['Fecha'].dt.year == 2025]
        if not hist_2025.empty:
            base_2025 = hist_2025.sort_values('Fecha').iloc[-1]['Ejecución']
        else:
            hist_2024 = df_hist_sel[df_hist_sel['Fecha'].dt.year == 2024]
            if not hist_2024.empty:
                base_2025 = hist_2024.sort_values('Fecha').iloc[-1]['Ejecución']
            else:
                hist_before = df_hist_sel[df_hist_sel['Fecha'] <= pd.to_datetime('2025-12-31')]
                if not hist_before.empty:
                    base_2025 = hist_before.sort_values('Fecha').iloc[-1]['Ejecución']

    for i, escenario in enumerate(escenarios_sel):
        esc_color = colores_escenarios.get(escenario, '#1a73e8')
        df_e = df_proj_sel[df_proj_sel['Escenario'] == escenario]

        # Obtener valores por año (último registro del año si hay varios)
        def get_year_value(df, year):
            dfx = df[df['Fecha'].dt.year == year]
            if dfx.empty:
                return np.nan
            return dfx.sort_values('Fecha').iloc[-1]['Proyección']

        v26 = get_year_value(df_e, 2026)
        v30 = get_year_value(df_e, 2030)

        # Calcular variación porcentual vs último 2025
        pct26 = np.nan
        pct30 = np.nan
        if pd.notna(base_2025) and base_2025 != 0:
            if pd.notna(v26):
                pct26 = (v26 - base_2025) / abs(base_2025) * 100.0
            if pd.notna(v30):
                pct30 = (v30 - base_2025) / abs(base_2025) * 100.0

        with cols[i]:
            # Tarjeta por escenario
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: {esc_color};">
                    <div class="metric-label">Base · Último 2025</div>
                    <div class="metric-value" style="color: #1e293b;">{format_number(base_2025, decimal_places) if pd.notna(base_2025) else 'N/A'}</div>
                    <div class="metric-label" style="margin-top:0.75rem;">{escenario} · 2026</div>
                    <div class="metric-value" style="color: {esc_color};">{format_number(v26, decimal_places) if pd.notna(v26) else 'N/A'}</div>
                    <div class="metric-label" style="margin-top:0.25rem;">Δ% vs 2025</div>
                    <div class="metric-value" style="color: {'#2ecc71' if (pd.notna(pct26) and pct26>=0) else '#e74c3c'};">{(f"{pct26:,.2f}%" if pd.notna(pct26) else 'N/A')}</div>
                    <div class="metric-label" style="margin-top:0.75rem;">{escenario} · 2030</div>
                    <div class="metric-value" style="color: {esc_color};">{format_number(v30, decimal_places) if pd.notna(v30) else 'N/A'}</div>
                    <div class="metric-label" style="margin-top:0.25rem;">Δ% vs 2025</div>
                    <div class="metric-value" style="color: {'#2ecc71' if (pd.notna(pct30) and pct30>=0) else '#e74c3c'};">{(f"{pct30:,.2f}%" if pd.notna(pct30) else 'N/A')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# TABLA DE DATOS DETALLADOS y DESCARGA
# ==============================
st.markdown("---")
with st.expander("📋 Ver Datos Detallados (Histórico y Proyección)"):
    # Preparación de la tabla
    df_hist_display = df_hist_sel.rename(columns={'Ejecución': 'Histórico'})[['Fecha', 'Indicador', 'Histórico', 'Fuente']]
    df_proj_display = df_proj_sel.pivot_table(index='Fecha', columns='Escenario', values='Proyección').reset_index()
    df_final_display = pd.merge(df_hist_display, df_proj_display, on='Fecha', how='outer')
    df_final_display = df_final_display.sort_values(by='Fecha').reset_index(drop=True)
    
    # Clonar para la descarga antes de aplicar formato de texto
    df_download = df_final_display.copy()

    # Aplicar formato de número para visualización
    for col in df_final_display.columns:
        if df_final_display[col].dtype in [np.float64, np.int64]:
            df_final_display[col] = df_final_display[col].apply(lambda x: format_number(x, decimal_places) if pd.notna(x) else '-')
    
    # Ajustar el formato de la columna Fecha (solo mostrar fecha)
    df_final_display['Fecha'] = df_final_display['Fecha'].dt.strftime('%Y-%m-%d')
    
    # --- BOTÓN DE DESCARGA ---
    csv_file = convert_df_to_csv(df_download)
    
    st.download_button(
        label="📥 Descargar Información Detallada (CSV)",
        data=csv_file,
        file_name=f'{indicador_sel}_{modelo_sel}_Proyecciones.csv',
        mime='text/csv',
        key='download_csv_button'
    )
    # --- FIN BOTÓN DE DESCARGA ---

    st.dataframe(
        df_final_display,
        use_container_width=True,
        hide_index=True
    )