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
try:
    RUTA_DATASET = str(BASE_DIR / "Data" / "Dataset_Unificado.xlsx")
    RUTA_PROYECCIONES = str(BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx")

    df_hist = pd.read_excel(RUTA_DATASET)
    df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"])

    df_proj_raw = pd.read_excel(RUTA_PROYECCIONES)
    df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"])
except: 
    # --- SIMULACIÓN DE DATOS (Fallback si no encuentra los archivos) ---
    df_hist = pd.DataFrame({
        'Fecha': pd.to_datetime(['2022-01-01', '2022-07-01', '2023-01-01', '2023-07-01', '2024-01-01', '2024-07-01']),
        'Indicador': ['Ingresos'] * 6,
        'Linea': ['Expansión'] * 6,
        'Ejecución': [15000, 16000, 17500, 19000, 21000, 22500],
        'Fuente': ['Cierre', 'Semestral', 'Cierre', 'Semestral', 'Cierre', 'Semestral'],
        'Decimales_Ejecucion': [0] * 6
    })
    df_proj_raw = pd.DataFrame({
        'Indicador': ['Ingresos'] * 6,
        'Modelo': ['ARIMA'] * 6,
        'Fecha_Proyeccion': pd.to_datetime(['2025-01-01', '2025-07-01', '2026-01-01', '2026-07-01', '2027-01-01', '2030-01-01']),
        'Escenario_Base': [24000, 25500, 27000, 29000, 31000, 35000],
        'Escenario_Pesimista': [23000, 24000, 25000, 26500, 28000, 32000],
        'Escenario_Optimista': [25000, 27000, 29000, 31500, 34000, 39000]
    })
    st.info("Usando datos de simulación. Asegúrese de que sus archivos están en la carpeta 'Data'.")
    # --- FIN SIMULACIÓN ---


df_proj_list = []
if not df_proj_raw.empty:
    for _, row in df_proj_raw.iterrows():
        base_data = {'Indicador': row['Indicador'], 'Periodicidad': row.get('Periodicidad', 'Semestral'), 'Fecha': row['Fecha_Proyeccion'], 'Modelo': row['Modelo']}
        if pd.notna(row.get('Escenario_Base')): df_proj_list.append({**base_data, 'Escenario': 'Base', 'Proyección': row['Escenario_Base']})
        if pd.notna(row.get('Escenario_Pesimista')): df_proj_list.append({**base_data, 'Escenario': 'Pesimista', 'Proyección': row['Escenario_Pesimista']})
        if pd.notna(row.get('Escenario_Optimista')): df_proj_list.append({**base_data, 'Escenario': 'Optimista', 'Proyección': row['Escenario_Optimista']})

df_proj = pd.DataFrame(df_proj_list) if df_proj_list else pd.DataFrame()

# ==============================
# SIDEBAR
# ==============================
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
        indicadores = sorted(df_hist_filtrado["Indicador"].unique())
    else:
        indicadores = sorted(df_hist["Indicador"].unique())
    
    indicador_sel = st.selectbox("📊 Indicador", indicadores)
    
    # Modelos ML 
    modelos = sorted(df_proj["Modelo"].unique()) if not df_proj.empty else []
    modelo_display_names = {'ARIMA': '📊 ARIMA', 'Random_Forest': '🌳 Random Forest', 'SVR': '🎯 SVR', 'Linear_Regression': '📈 Regresión Lineal', 'Prophet': '🔮 Prophet', 'Crecimiento_Historico': '📜 Histórico'}
    modelo_options = [modelo_display_names.get(m, m) for m in modelos]
    modelo_display_sel = st.selectbox("🧠 Modelo ML", modelo_options)
    modelo_sel = next((k for k, v in modelo_display_names.items() if v == modelo_display_sel), modelo_display_sel)
    
    # Escenarios 
    escenarios_disponibles = ['Base', 'Pesimista', 'Optimista']
    if not df_proj.empty and modelo_sel in df_proj["Modelo"].unique():
        escenarios_modelo = df_proj[df_proj["Modelo"] == modelo_sel]["Escenario"].unique()
        escenarios_disponibles = [e for e in escenarios_disponibles if e in escenarios_modelo]
    
    st.markdown("**🌍 Escenarios:**")
    escenarios_sel = []
    escenario_icons = {'Base': '⚖️', 'Pesimista': '📉', 'Optimista': '📈'}
    for escenario in escenarios_disponibles:
        icon = escenario_icons.get(escenario, '🌍')
        default_value = escenario in ['Base', 'Optimista']
        if st.checkbox(f"{icon} {escenario}", value=default_value, key=f"esc_{escenario}"):
            escenarios_sel.append(escenario)
    
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

df_proj_sel = df_proj[(df_proj["Indicador"] == indicador_sel) & (df_proj["Modelo"] == modelo_sel) & (df_proj["Escenario"].isin(escenarios_sel))]

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

decimal_places = 0
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

colores_escenarios = {
    'Base': '#1a73e8', 
    'Pesimista': '#e74c3c',
    'Optimista': '#2ecc71',
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

df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"]
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"]

fig = go.Figure()

# Agregar históricos (Lógica simplificada por periodicidad)
df_hist_trace = df_hist_semestral if tipo_visualizacion == "Semestral" else df_hist_anual
trace_name = "Histórico Semestral" if tipo_visualizacion == "Semestral" else "Histórico Anual"

if not df_hist_trace.empty:
    fig.add_trace(go.Scatter(x=df_hist_trace["Fecha"], y=df_hist_trace["Ejecución"], name=trace_name, line=dict(color='#FF00FF', width=2.5), marker=dict(size=8, color='#FF00FF', line=dict(width=1, color='white')), mode='lines+markers', hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'))
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
                color='#FF00FF', 
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
        
        df_plot = df_esc.sort_values('Fecha')
        
        if tipo_visualizacion == "Anual":
            # CORRECCIÓN APLICADA: Tomar la última proyección disponible en cada año (la más representativa del cierre anual)
            # 1. Encuentra el índice de la fecha máxima para cada año proyectado
            idx = df_esc.groupby(df_esc['Fecha'].dt.year)['Fecha'].idxmax()
            # 2. Usa esos índices para seleccionar solo los puntos de cierre anual
            df_plot = df_esc.loc[idx].sort_values('Fecha')
        
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
if mostrar_linea_divisoria and not df_hist_sel.empty and not df_proj_sel.empty:
    last_hist_date = df_hist_sel['Fecha'].max()
    fecha_corte = last_hist_date + pd.Timedelta(days=1)
    fecha_corte_str = fecha_corte.strftime('%Y-%m-%d')

    # 1. Añadir la línea vertical (SOLO LA LÍNEA)
    fig.add_vline(
        x=fecha_corte_str, 
        line_width=3, 
        line_dash="dash", 
        line_color="#e74c3c"
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
        font=dict(color="#e74c3c", size=12, weight="bold"),
        yshift=-10 
    )


# Configuración del formato de fechas para el eje X (YYYY-S#)
tickvals = []
ticktext = []
years = []

if not df_hist_sel.empty: years.extend(df_hist_sel['Fecha'].dt.year.unique())
if not df_proj_sel.empty: years.extend(df_proj_sel['Fecha'].dt.year.unique())
all_years = sorted(list(set(years)))

for year in all_years:
    if tipo_visualizacion == "Semestral":
        tickvals.extend([f"{year}-01-01", f"{year}-07-01"])
        ticktext.extend([f"{year}-S1", f"{year}-S2"]) 
    elif tipo_visualizacion == "Anual":
        tickvals.append(f"{year}-07-01") 
        ticktext.append(str(year))


# Actualizar el layout del gráfico
fig.update_layout(
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    height=900,
    font=dict(family="Poppins", size=22, color="#1e293b"),
    
    title=dict(
        text=f"<b>{indicador_sel}</b> - Evolución Histórica y Proyección (Modelo: {modelo_sel})",
        x=0.5, y=0.95, xanchor='center', yanchor='top',
        font=dict(size=32, color="#0d47a1", family="Poppins", weight="bold")
    ),
    hovermode='x unified',
    legend=dict(
        orientation="h", yanchor="bottom", y=1.08, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.95)", bordercolor="#cbd5e0", borderwidth=1.5,
        font=dict(size=22, family="Poppins", color="#1e293b", weight=500),
        itemsizing='constant', itemclick=False, itemdoubleclick=False
    ),
    # Ajustar el espaciado para las etiquetas
    
    # ETIQUETAS EJE X: Formato YYYY-S# y Rotación
    xaxis=dict(
        title=dict(
            text="<b>PERIODO</b>",
            font=dict(size=24, weight=600, family="Poppins", color="#1e293b"),
            standoff=20
        ),
        showgrid=True, gridcolor='rgba(0,0,0,0.05)', gridwidth=1,
        tickvals=tickvals,
        ticktext=ticktext, 
        tickfont=dict(size=20, family="Poppins", color="#1e293b", weight=500),
        linecolor='#cbd5e0', linewidth=2, mirror=True, showline=True, automargin=True,
        # Rotación forzada a 45 grados para vista Semestral
        tickangle=45 if tipo_visualizacion == "Semestral" else 0,
        title_standoff=25,
        fixedrange=True
    ),
    
    # ETIQUETAS EJE Y
    yaxis=dict(
        title=dict(
            text=f"<b>{indicador_sel.upper()}</b>",
            font=dict(size=24, weight=600, family="Poppins", color="#1e293b"),
            standoff=20
        ),
        showgrid=True, gridcolor='rgba(0,0,0,0.05)', gridwidth=1,
        tickformat=f",.{int(decimal_places)}f",
        title_standoff=25,
        showline=True,
        linewidth=2,
        linecolor='#cbd5e0',
        mirror=True,
        tickfont=dict(size=20, family="Poppins", color="#1e293b", weight=500),
        zeroline=False, automargin=True
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
    margin=dict(t=160, b=140, l=140, r=100, pad=15)
)

# Mostrar la gráfica
st.plotly_chart(fig, use_container_width=True)

# ==============================
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