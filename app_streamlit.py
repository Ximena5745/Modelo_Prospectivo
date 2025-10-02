import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

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
# ESTILOS CSS MEJORADOS
# ==============================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Fondo principal */
        .main {
            background-color: #f8fafc;
            color: #1e293b;
        }
        
        .stApp {
            background-color: #f8fafc;
        }
        
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1800px;
        }
        
        /* Títulos principales */
        h1 {
            color: #0d47a1;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        h2 {
            color: #1a73e8;
            font-size: 1.75rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #e3f2fd;
        }
        
        h3 {
            color: #1557b0;
            font-size: 1.25rem;
            font-weight: 600;
            margin: 1.5rem 0 0.75rem 0;
        }
        
        /* Sidebar oscuro profesional */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%);
            padding: 1.5rem 1rem;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white !important;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Botón Refrescar mejorado */
        .stButton > button {
            background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(26, 115, 232, 0.4);
            background: linear-gradient(135deg, #1e88e5 0%, #1a73e8 100%);
        }
        
        /* Selectores y controles */
        .stSelectbox label,
        .stCheckbox label {
            font-weight: 500;
            font-size: 0.9rem;
            color: #475569;
        }
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stCheckbox label {
            color: white !important;
        }
        
        .stSelectbox > div,
        .stTextInput > div,
        .stNumberInput > div {
            border-radius: 8px;
            border: 1px solid #cbd5e0;
            background: white;
            transition: all 0.2s ease;
        }
        
        .stSelectbox > div:focus-within {
            border-color: #1a73e8;
            box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.1);
        }
        
        /* Checkboxes mejorados */
        .stCheckbox > label {
            padding: 0.5rem;
            border-radius: 6px;
            transition: background 0.2s ease;
        }
        
        .stCheckbox > label:hover {
            background: rgba(255,255,255,0.1);
        }
        
        /* Pestañas profesionales */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 2px solid #e3f2fd;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #f1f5f9;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            color: #64748b;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: #1a73e8;
            color: white !important;
            box-shadow: 0 -2px 0 #0d47a1 inset;
        }
        
        /* Métricas mejoradas */
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            border-left: 4px solid #1a73e8;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
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
            color: #0d47a1;
            font-size: 2rem;
            font-weight: 700;
            line-height: 1;
        }
        
        /* Fichas de escenarios */
        .scenario-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }
        
        .scenario-card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }
        
        .scenario-base {
            border-left: 5px solid #1a73e8;
        }
        
        .scenario-optimista {
            border-left: 5px solid #2ecc71;
        }
        
        .scenario-pesimista {
            border-left: 5px solid #e74c3c;
        }
        
        .scenario-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        
        .scenario-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }
        
        .scenario-icon-base {
            background: #e3f2fd;
            color: #1a73e8;
        }
        
        .scenario-icon-optimista {
            background: #d5f4e6;
            color: #2ecc71;
        }
        
        .scenario-icon-pesimista {
            background: #fadbd8;
            color: #e74c3c;
        }
        
        .scenario-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1e293b;
        }
        
        /* Gráficos */
        .stPlotlyChart {
            border-radius: 10px;
            overflow: hidden;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        /* Expandibles */
        .stExpander {
            background: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            overflow: hidden;
        }
        
        .stExpander summary {
            font-weight: 600;
            color: #1e293b;
            background: #f8fafc;
        }
        
        /* Línea estratégica */
        .strategic-line-card {
            background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
            border-radius: 10px;
            padding: 1.5rem;
            color: white;
            box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
            margin-bottom: 2rem;
        }
        
        .strategic-line-label {
            font-size: 0.875rem;
            font-weight: 600;
            opacity: 0.9;
            margin-bottom: 0.25rem;
        }
        
        .strategic-line-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# ENCABEZADO
# ==============================
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">MODELO DE PROSPECTIVA POLI</h1>
    <div style="height: 4px; width: 200px; background: linear-gradient(90deg, #1a73e8, #2ecc71); 
                margin: 0 auto 1rem; border-radius: 2px;"></div>
    <p style="color: #64748b; font-size: 1.1rem; margin: 0;">
        Plataforma de análisis y proyección de indicadores estratégicos 2026-2030
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# LECTURA DE DATOS
# ==============================
BASE_DIR = Path(__file__).parent
RUTA_DATASET = str(BASE_DIR / "Data" / "Dataset_Unificado.xlsx")
RUTA_PROYECCIONES = str(BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx")

df_hist = pd.read_excel(RUTA_DATASET)
df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"])

df_proj_raw = pd.read_excel(RUTA_PROYECCIONES)
df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"])

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

# ==============================
# SIDEBAR - CONTROLES
# ==============================
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.markdown('<h2>⚙️ CONTROLES</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    lineas_estrategicas = {
        "Expansión": ("Expansión", "#1a73e8"),
        "Transformación Organizacional": ("Transformación_Organizacional", "#1557b0"), 
        "Calidad": ("Calidad", "#0d47a1"),
        "Experiencia": ("Experiencia", "#1976d2"),
        "Sostenibilidad": ("Sostenibilidad", "#2196f3"),
        "Educación para la vida": ("Educación_para_toda_la_vida", "#1565c0")
    }

    linea_sel = st.selectbox("🎯 Línea Estratégica", list(lineas_estrategicas.keys()))
    display_name, color_linea = lineas_estrategicas[linea_sel]
    
    if 'Linea' in df_hist.columns:
        df_hist_filtrado = df_hist[df_hist["Linea"] == display_name]
        if df_hist_filtrado.empty:
            df_hist_filtrado = df_hist[df_hist["Linea"].str.replace('_', ' ') == linea_sel]
        if df_hist_filtrado.empty:
            df_hist_filtrado = df_hist
        indicadores = sorted(df_hist_filtrado["Indicador"].unique())
    else:
        indicadores = sorted(df_hist["Indicador"].unique())
    
    indicador_sel = st.selectbox("📊 Indicador", indicadores)
    
    modelos = sorted(df_proj["Modelo"].unique()) if not df_proj.empty else []
    modelo_display_names = {
        'ARIMA': '📊 ARIMA',
        'Random_Forest': '🌳 Random Forest',
        'SVR': '🎯 SVR',
        'Linear_Regression': '📈 Regresión Lineal',
        'Prophet': '🔮 Prophet',
        'Crecimiento_Historico': '📜 Histórico'
    }
    
    modelo_options = [modelo_display_names.get(m, m) for m in modelos]
    modelo_display_sel = st.selectbox("🧠 Modelo ML", modelo_options)
    modelo_sel = next((k for k, v in modelo_display_names.items() if v == modelo_display_sel), modelo_display_sel)

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
    tipo_grafico = st.selectbox("Tipo", ["Línea", "Barras", "Dispersión"], label_visibility="collapsed")
    mostrar_numeros = st.checkbox("Mostrar valores", value=True)
    mostrar_linea_divisoria = st.checkbox("Línea divisoria", value=True)

    st.markdown("---")
    if st.button("🔄 REFRESCAR"):
        st.rerun()

# ==============================
# FILTRAR DATOS
# ==============================
if 'Linea' in df_hist.columns:
    df_hist_sel = df_hist[(df_hist["Indicador"] == indicador_sel) & (df_hist["Linea"] == display_name)]
    if df_hist_sel.empty:
        df_hist_sel = df_hist[(df_hist["Indicador"] == indicador_sel) & (df_hist["Linea"].str.replace('_', ' ') == linea_sel)]
else:
    df_hist_sel = df_hist[df_hist["Indicador"] == indicador_sel]

df_proj_sel = df_proj[(df_proj["Indicador"] == indicador_sel) & (df_proj["Modelo"] == modelo_sel) & (df_proj["Escenario"].isin(escenarios_sel))]

# ==============================
# LÍNEA ESTRATÉGICA
# ==============================
st.markdown(f"""
<div class="strategic-line-card">
    <div class="strategic-line-label">LÍNEA ESTRATÉGICA</div>
    <div class="strategic-line-title">🎯 {linea_sel}</div>
</div>
""", unsafe_allow_html=True)

# ==============================
# MÉTRICAS PRINCIPALES
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Modelo Seleccionado</div>
        <div class="metric-value">{modelo_sel}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Escenarios Activos</div>
        <div class="metric-value">{len(escenarios_sel)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if not df_proj_sel.empty and len(escenarios_sel) > 0:
        df2030 = df_proj_sel[df_proj_sel["Fecha"].dt.year == 2030]
        valor_formateado = f"{df2030['Proyección'].mean():,.0f}" if not df2030.empty else "N/A"
    else:
        valor_formateado = "N/A"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Promedio 2030</div>
        <div class="metric-value">{valor_formateado}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# GRÁFICO PRINCIPAL
# ==============================
st.markdown(f"## 📈 {indicador_sel}")

fig = go.Figure()

df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"]
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"]

def format_number(value, decimals):
    if pd.isna(value):
        return ''
    try:
        decimals = int(decimals) if not pd.isna(decimals) else 0
        return f"{float(value):,.{decimals}f}"
    except:
        return str(value)

decimal_places = 0
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

# Colores profesionales
colores_escenarios = {
    'Base': '#1a73e8',
    'Pesimista': '#e74c3c',
    'Optimista': '#2ecc71'
}

# Agregar históricos
if tipo_visualizacion == "Semestral":
    if not df_hist_semestral.empty:
        fig.add_trace(go.Scatter(
            x=df_hist_semestral["Fecha"],
            y=df_hist_semestral["Ejecución"],
            name="Histórico Semestral",
            line=dict(color='#5c8bf2', width=2.5),
            marker=dict(size=8, color='#5c8bf2', line=dict(width=1, color='white')),
            mode='lines+markers',
            hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
        ))
        if mostrar_numeros:
            text_values = df_hist_semestral["Ejecución"].apply(lambda x: format_number(x, decimal_places))
            fig.add_trace(go.Scatter(
                x=df_hist_semestral["Fecha"],
                y=df_hist_semestral["Ejecución"],
                mode="text",
                text=text_values,
                textposition="top center",
                textfont=dict(size=10, color='#5c8bf2'),
                showlegend=False,
                hoverinfo='skip'
            ))
elif tipo_visualizacion == "Anual":
    if not df_hist_anual.empty:
        fig.add_trace(go.Scatter(
            x=df_hist_anual["Fecha"],
            y=df_hist_anual["Ejecución"],
            name="Histórico Anual",
            line=dict(color='#5c8bf2', width=2.5),
            marker=dict(size=8, color='#5c8bf2', line=dict(width=1, color='white')),
            mode='lines+markers',
            hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
        ))
        if mostrar_numeros:
            text_values = df_hist_anual["Ejecución"].apply(lambda x: format_number(x, decimal_places))
            fig.add_trace(go.Scatter(
                x=df_hist_anual["Fecha"],
                y=df_hist_anual["Ejecución"],
                mode="text",
                text=text_values,
                textposition="top center",
                textfont=dict(size=10, color='#5c8bf2'),
                showlegend=False,
                hoverinfo='skip'
            ))

# Agregar proyecciones
for escenario in escenarios_sel:
    df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    if not df_esc.empty:
        color = colores_escenarios.get(escenario, '#1a73e8')
        
        # Separar por semestre
        df_proj_s1 = df_esc[df_esc["Fecha"].dt.month == 6]
        df_proj_s2 = df_esc[df_esc["Fecha"].dt.month == 12]
        
        if tipo_visualizacion == "Semestral":
            # Mostrar ambos semestres
            df_esc_sorted = df_esc.sort_values('Fecha')
            fig.add_trace(go.Scatter(
                x=df_esc_sorted["Fecha"],
                y=df_esc_sorted["Proyección"],
                name=escenario,
                line=dict(color=color, width=2.5, dash='dot'),
                marker=dict(size=8, color=color, line=dict(width=1, color='white')),
                mode='lines+markers',
                hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
            ))
            if mostrar_numeros:
                text_values = df_esc_sorted["Proyección"].apply(lambda x: format_number(x, decimal_places))
                fig.add_trace(go.Scatter(
                    x=df_esc_sorted["Fecha"],
                    y=df_esc_sorted["Proyección"],
                    mode="text",
                    text=text_values,
                    textposition="top center",
                    textfont=dict(size=10, color=color),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        elif tipo_visualizacion == "Anual":
            # Mostrar solo diciembre (S2)
            if not df_proj_s2.empty:
                fig.add_trace(go.Scatter(
                    x=df_proj_s2["Fecha"],
                    y=df_proj_s2["Proyección"],
                    name=f"{escenario} (Anual)",
                    line=dict(color=color, width=2.5, dash='dot'),
                    marker=dict(size=8, color=color, line=dict(width=1, color='white')),
                    mode='lines+markers',
                    hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
                ))
                if mostrar_numeros:
                    text_values = df_proj_s2["Proyección"].apply(lambda x: format_number(x, decimal_places))
                    fig.add_trace(go.Scatter(
                        x=df_proj_s2["Fecha"],
                        y=df_proj_s2["Proyección"],
                        mode="text",
                        text=text_values,
                        textposition="top center",
                        textfont=dict(size=10, color=color),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

# Línea divisoria
if mostrar_linea_divisoria and not df_hist_sel.empty and not df_proj_sel.empty:
    fecha_division = pd.Timestamp('2025-12-31')
    fig.add_shape(
        type="line",
        x0=fecha_division,
        x1=fecha_division,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="#e74c3c", width=3, dash="dash")
    )
    fig.add_annotation(
        x=fecha_division,
        y=0.95,
        yref="paper",
        text="Histórico / Proyección",
        showarrow=False,
        font=dict(color="#e74c3c", size=12, weight="bold"),
        xanchor="center"
    )

fig.update_layout(
    template="plotly",
    plot_bgcolor='#f5f5f5',
    paper_bgcolor='#f5f5f5',
    height=550,
    font=dict(family="Poppins", size=12, color="#1e293b"),
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#e2e8f0",
        borderwidth=1
    ),
    margin=dict(l=50, r=50, t=80, b=50),
    xaxis=dict(
        showgrid=True, 
        gridcolor='white',
        tickformat="%Y-%m"
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='white',
        tickformat=","
    )
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# RESUMEN DE ESCENARIOS
# ==============================
st.markdown("## 📊 Resumen de Escenarios")

ultimo_valor_historico = 0
if not df_hist_anual.empty:
    ultimo_valor_historico = df_hist_anual["Ejecución"].iloc[-1]
elif not df_hist_semestral.empty:
    ultimo_valor_historico = df_hist_semestral["Ejecución"].iloc[-1]
elif not df_hist_sel.empty:
    ultimo_valor_historico = df_hist_sel["Ejecución"].iloc[-1]

for escenario in escenarios_sel:
    df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    
    if not df_esc.empty:
        valor_2026 = df_esc[df_esc["Fecha"].dt.year == 2026]["Proyección"].mean() if not df_esc[df_esc["Fecha"].dt.year == 2026].empty else 0
        valor_2030 = df_esc[df_esc["Fecha"].dt.year == 2030]["Proyección"].mean() if not df_esc[df_esc["Fecha"].dt.year == 2030].empty else 0
        
        variacion_2030 = ((valor_2030 - ultimo_valor_historico) / ultimo_valor_historico * 100) if ultimo_valor_historico != 0 else 0
        variacion_periodo = ((valor_2030 - valor_2026) / valor_2026 * 100) if valor_2026 != 0 else 0
        
        # Determinar clase y color del escenario
        if escenario == "Base":
            clase_escenario = "scenario-base"
            icon_clase = "scenario-icon-base"
            icon = "⚖️"
        elif escenario == "Optimista":
            clase_escenario = "scenario-optimista"
            icon_clase = "scenario-icon-optimista"
            icon = "📈"
        else:  # Pesimista
            clase_escenario = "scenario-pesimista"
            icon_clase = "scenario-icon-pesimista"
            icon = "📉"
        
        # Card del escenario
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="scenario-card {clase_escenario}">
                <div class="scenario-header">
                    <div class="scenario-icon {icon_clase}">{icon}</div>
                    <div class="scenario-title">{escenario}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("📊 2026", f"{valor_2026:,.{int(decimal_places)}f}")
        
        with col3:
            st.metric("🎯 2030", f"{valor_2030:,.{int(decimal_places)}f}", f"{variacion_2030:+.1f}%")
        
        with col4:
            tendencia = "🟢 Creciente" if variacion_periodo > 0 else "🔴 Decreciente" if variacion_periodo < 0 else "🟡 Estable"
            st.markdown(f"""
            <div style="padding: 1rem; text-align: center;">
                <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.25rem;">Variación</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">{variacion_periodo:+.1f}%</div>
                <div style="margin-top: 0.5rem; font-weight: 600;">{tendencia}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1px; background: #e2e8f0; margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# ==============================
# TABLA DE DATOS
# ==============================
with st.expander("📋 Ver Datos Detallados"):
    df_hist_display = df_hist_sel.rename(columns={"Ejecución": "Valor"})[["Fecha", "Indicador", "Valor"]]
    df_hist_display["Tipo"] = "Histórico"
    df_hist_display["Escenario"] = "N/A"
    
    df_proj_display = df_proj_sel.rename(columns={"Proyección": "Valor"})[["Fecha", "Indicador", "Valor", "Escenario"]]
    df_proj_display["Tipo"] = "Proyección"
    
    df_merge = pd.concat([df_hist_display, df_proj_display])
    st.dataframe(df_merge.sort_values("Fecha"), use_container_width=True)