import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np 

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
# ESTILOS CSS (Mejora de la estética del dashboard)
# ==============================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .main { background-color: #f8fafc; color: #1e293b; }
        .stApp { background-color: #f8fafc; }
        .main .block-container { padding: 2rem 3rem; max-width: 1800px; }
        h1 { color: #0d47a1; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
        h2 { color: #1a73e8; font-size: 1.75rem; font-weight: 600; margin: 2rem 0 1rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }
        /* Estilos para las tarjetas de resumen */
        .card-container { display: flex; justify-content: space-between; gap: 20px; }
        .metric-card {
            flex: 1;
            text-align: center;
            padding: 1rem;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
            border-left: 5px solid #1a73e8;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# DATOS SIMULADOS (Reemplazar con su carga de datos real)
# ==============================

@st.cache_data
def load_and_prepare_data():
    # --- SIMULACIÓN DE DATOS REALES ---
    # DataFrames simulados para histórico y proyección
    data_hist = {
        'Fecha': pd.to_datetime(['2022-01-01', '2022-07-01', '2023-01-01', '2023-07-01', '2024-01-01', '2024-07-01']),
        'Indicador': ['Ingresos'] * 6,
        'Valor': [1500, 1600, 1750, 1900, 2100, 2250],
        'Fuente': ['Semestral', 'Semestral', 'Semestral', 'Semestral', 'Semestral', 'Semestral'],
        'Decimales_Ejecucion': [0] * 6
    }
    df_hist = pd.DataFrame(data_hist)
    df_hist.loc[df_hist['Fecha'].dt.month == 1, 'Fuente'] = 'Cierre' # Simular 'Cierre' para Anual
    
    data_proj = {
        'Fecha': pd.to_datetime(['2025-01-01', '2025-07-01', '2026-01-01', '2026-07-01', '2027-01-01', '2027-07-01', '2030-01-01']),
        'Indicador': ['Ingresos'] * 7,
        'Escenario': ['Base', 'Base', 'Base', 'Base', 'Base', 'Base', 'Base'],
        'Valor': [2400, 2550, 2700, 2900, 3100, 3350, 4500]
    }
    df_proj = pd.DataFrame(data_proj)
    
    # Añadir otros escenarios simulados
    df_proj_pesimista = df_proj.copy()
    df_proj_pesimista['Escenario'] = 'Pesimista'
    df_proj_pesimista['Valor'] = df_proj_pesimista['Valor'] * 0.95
    df_proj = pd.concat([df_proj, df_proj_pesimista], ignore_index=True)

    indicadores = ['Ingresos', 'Egresos', 'Matrículas']
    modelos = ['ARIMA', 'Prophet', 'SARIMAX']
    visualizaciones = ['Semestral', 'Anual']
    
    return df_hist, df_proj, indicadores, modelos, visualizaciones

df_hist, df_proj, indicadores, modelos, visualizaciones = load_and_prepare_data()

# ==============================
# SIDEBAR DE CONTROL
# ==============================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e4/Logo_Poli.png", width=100) # Reemplazar con logo real
    st.title("Filtros del Modelo")
    
    indicador_sel = st.selectbox("🎯 Indicador a Proyectar", indicadores, index=0)
    modelo_sel = st.selectbox("🧠 Modelo de Pronóstico", modelos, index=0)
    tipo_visualizacion = st.selectbox("📅 Tipo de Visualización", visualizaciones, index=0)
    
    st.markdown("---")
    mostrar_numeros = st.checkbox("Mostrar Números en Gráfico", value=False)
    
# Filtrar datos basado en la selección
df_hist_sel = df_hist[df_hist['Indicador'] == indicador_sel]
df_proj_sel = df_proj[df_proj['Indicador'] == indicador_sel]
df_proj_sel = df_proj_sel.sort_values(by='Fecha')


# ==============================
# FUNCIONES AUXILIARES
# ==============================
# Obtener los decimales para el formato del hover
decimal_places = 0
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

# Función de formato con separador de miles y decimales
def format_number(value, dp):
    if pd.isna(value):
        return ""
    # Evitar notación científica y aplicar separador de miles y decimales
    return f"{value:,.{int(dp)}f}"

# Definición de colores para las proyecciones
colores_escenarios = {
    'Base': '#1a73e8',  # Azul fuerte
    'Pesimista': '#e74c3c',  # Rojo
    'Optimista': '#2ecc71',  # Verde
    'Alto': '#f39c12',  # Naranja
    'Bajo': '#34495e'   # Gris oscuro
}

# ==============================
# CUERPO PRINCIPAL DEL DASHBOARD
# ==============================

st.header("Análisis de Proyección de {}".format(indicador_sel))
st.markdown("---")

# ==============================
# TARJETAS DE RESUMEN 
# ==============================

# Se requiere un escenario base para las tarjetas
df_base = df_proj_sel[df_proj_sel['Escenario'] == 'Base']

if not df_base.empty:
    valor_2026 = df_base[df_base['Fecha'].dt.year == 2026]['Valor'].max()
    valor_2030 = df_base[df_base['Fecha'].dt.year == 2030]['Valor'].max()
    ultimo_historico = df_hist_sel['Valor'].max() if not df_hist_sel.empty else np.nan
    
    variacion_periodo = valor_2030 - valor_2026 if pd.notna(valor_2030) and pd.notna(valor_2026) else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="metric-card" style="border-left-color: #2ecc71;"><div style="color: #64748b; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">📈 ÚLTIMO HISTÓRICO</div><div style="font-size: 1.8rem; font-weight: 700; color: #1e293b;">{format_number(ultimo_historico, decimal_places)}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #1a73e8;"><div style="color: #64748b; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">🎯 PROYECCIÓN (2026)</div><div style="font-size: 1.8rem; font-weight: 700; color: #1a73e8;">{format_number(valor_2026, decimal_places)}</div></div>', unsafe_allow_html=True)
    with col3:
        # Se asegura que la variación tenga el color correcto
        delta_color = "#2ecc71" if variacion_periodo > 0 else ("#e74c3c" if variacion_periodo < 0 else "#f1c40f")
        st.markdown(f'<div class="metric-card" style="border-left-color: #f39c12;"><div style="color: #64748b; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">⭐ PROYECCIÓN (2030)</div><div style="font-size: 1.8rem; font-weight: 700; color: #f39c12; margin-bottom: 0.25rem;">{format_number(valor_2030, decimal_places)}</div><div style="color: {delta_color}; font-size: 1rem; font-weight: 600; margin-top: 0.25rem;">Δ {valor_2030 - valor_2026:+,.{int(decimal_places)}f}</div></div>', unsafe_allow_html=True)
    with col4:
        if variacion_periodo > 0: tendencia, icon_tend, color_tend = "Creciente", "🟢", "#2ecc71"
        elif variacion_periodo < 0: tendencia, icon_tend, color_tend = "Decreciente", "🔴", "#e74c3c"
        else: tendencia, icon_tend, color_tend = "Estable", "🟡", "#f1c40f"
        st.markdown(f'<div class="metric-card" style="border-left-color: {color_tend};"><div style="color: #64748b; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">📊 TENDENCIA PERIODO</div><div style="font-size: 2rem; margin: 0.5rem 0;">{icon_tend}</div><div style="color: {color_tend}; font-size: 1.1rem; font-weight: 700;">{tendencia}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ==============================
# GRÁFICO (AJUSTADO Y VALIDADO)
# ==============================
st.subheader("Evolución Histórica y Proyección Detallada")

fig = go.Figure()
df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"]
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"]

# ----------------------------------
# 1. TRAZAS HISTÓRICAS Y PROYECCIONES
# ----------------------------------

# Agregar históricos (Semestral)
fig.add_trace(go.Scatter(
    x=df_hist_semestral['Fecha'], 
    y=df_hist_semestral['Valor'], 
    mode='lines+markers' + ('+text' if mostrar_numeros else ''), 
    text=[format_number(v, decimal_places) for v in df_hist_semestral['Valor']] if mostrar_numeros else None,
    textposition="top center",
    name='Histórico Semestral',
    line=dict(color='#64748b', width=2),
    marker=dict(size=6, symbol='circle', color='#64748b'),
    hovertext=[f"Valor: {format_number(v, decimal_places)}" for v in df_hist_semestral['Valor']],
    hoverinfo='text+x'
))

# Agregar históricos (Cierre/Anual)
fig.add_trace(go.Scatter(
    x=df_hist_anual['Fecha'], 
    y=df_hist_anual['Valor'], 
    mode='lines+markers' + ('+text' if mostrar_numeros else ''),
    text=[format_number(v, decimal_places) for v in df_hist_anual['Valor']] if mostrar_numeros else None,
    textposition="bottom center",
    name='Histórico Cierre (Anual)',
    line=dict(color='#1e293b', width=3),
    marker=dict(size=8, symbol='circle-open', line=dict(width=2)),
    hovertext=[f"Valor: {format_number(v, decimal_places)}" for v in df_hist_anual['Valor']],
    hoverinfo='text+x'
))

# Agregar proyecciones
for escenario in df_proj_sel['Escenario'].unique():
    df_escenario = df_proj_sel[df_proj_sel['Escenario'] == escenario].sort_values(by='Fecha')
    color = colores_escenarios.get(escenario, '#95a5a6') 
    
    fig.add_trace(go.Scatter(
        x=df_escenario['Fecha'], 
        y=df_escenario['Valor'], 
        mode='lines+markers' + ('+text' if mostrar_numeros else ''),
        text=[format_number(v, decimal_places) for v in df_escenario['Valor']] if mostrar_numeros else None,
        textposition="top right",
        name=f'Proyección {escenario}',
        line=dict(color=color, width=3, dash='dot'), 
        marker=dict(size=7, symbol='square', color=color),
        hovertext=[f"Valor: {format_number(v, decimal_places)}" for v in df_escenario['Valor']],
        hoverinfo='text+x'
    ))

# ----------------------------------
# 2. LÍNEA DIVISORIA Y CONFIGURACIÓN DEL EJE X (ERROR CORREGIDO AQUÍ)
# ----------------------------------
fecha_corte = df_hist_sel['Fecha'].max() + pd.Timedelta(days=1) if not df_hist_sel.empty else pd.to_datetime('2025-01-01')

# FIX: Convertir el Timestamp a string para evitar TypeError en add_vline con anotaciones.
fecha_corte_str = fecha_corte.strftime('%Y-%m-%d') 

fig.add_vline(x=fecha_corte_str, line_width=2, line_dash="dash", line_color="#3498db", annotation_text="Inicio Proyección", annotation_position="top left")

# Generar marcas y etiquetas de ticks para el eje X
tickvals = []
ticktext = []
years_hist = sorted(df_hist_sel['Fecha'].dt.year.unique()) if not df_hist_sel.empty else []
years_proj = sorted(df_proj_sel['Fecha'].dt.year.unique()) if not df_proj_sel.empty else []
all_years = sorted(list(set(years_hist) | set(years_proj)))

for year in all_years:
    if tipo_visualizacion == "Semestral":
        tickvals.extend([f"{year}-01-01", f"{year}-07-01"])
        ticktext.extend([f"{year}-S1", f"{year}-S2"])
    else:
        tickvals.append(f"{year}-07-01") 
        ticktext.append(str(year))


# ----------------------------------
# 3. LAYOUT Y ESTILOS (Validación de texto)
# ----------------------------------

fig.update_layout(
    template="plotly_white",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    height=650, 
    font=dict(family="Poppins", size=14, color="#1e293b"),
    
    # TÍTULO PRINCIPAL: Validado
    title=dict(
        text=f"<b>{indicador_sel}</b> - Evolución Histórica y Proyección (Modelo {modelo_sel})",
        x=0.5, y=0.95, xanchor='center', yanchor='top',
        font=dict(size=24, color="#0d47a1", family="Poppins", weight="bold") 
    ),
    hovermode='x unified',
    
    # LEYENDA: Validada (superior, horizontal, interactiva)
    legend=dict(
        orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5,
        bgcolor="rgba(255,255,255,0.95)", bordercolor="#cbd5e0", borderwidth=1.5,
        font=dict(size=13, family="Poppins", color="#1e293b"),
        itemsizing='constant', itemclick='toggle', itemdoubleclick='toggleothers'
    ),
    margin=dict(l=80, r=60, t=120, b=100),
    
    # ETIQUETAS EJE X: Validado (título, ticks, ángulo)
    xaxis=dict(
        title=dict(
            text="<b>PERIODO</b>",
            font=dict(size=16, weight=700, family="Poppins", color="#1e293b"),
            standoff=20
        ),
        showgrid=True, gridcolor='rgba(0,0,0,0.05)',
        tickvals=tickvals, ticktext=ticktext,
        tickfont=dict(size=12, family="Poppins", color="#475569"),
        linecolor='#cbd5e0', linewidth=2, mirror=True, showline=True, automargin=True,
        tickangle=45 if tipo_visualizacion == "Semestral" and len(all_years) > 5 else 0,
        fixedrange=True
    ),
    
    # ETIQUETAS EJE Y: Validado (título explícito y formato de número)
    yaxis=dict(
        title=dict(
            text=f"<b>VALOR DEL INDICADOR ({indicador_sel.upper()})</b>",
            font=dict(size=16, weight=700, family="Poppins", color="#1e293b"),
            standoff=20
        ),
        showgrid=True, gridcolor='rgba(0,0,0,0.05)',
        tickformat=f",.{int(decimal_places)}f", 
        tickfont=dict(size=12, family="Poppins", color="#475569"),
        linecolor='#cbd5e0', linewidth=2, mirror=True, showline=True,
        zeroline=False, automargin=True, fixedrange=True
    ),
    hoverlabel=dict(
        bgcolor="white", font_size=13, font_family="Poppins", bordercolor="#cbd5e0", namelength=-1
    )
)

# ----------------------------------
# 4. RENDERIZADO EN STREAMLIT
# ----------------------------------

st.plotly_chart(fig, use_container_width=True)

# ==============================
# TABLA DE DATOS
# ==============================
st.markdown("---")
with st.expander("📋 Ver Datos Detallados (Histórico y Proyección)"):
    # Prepara el DataFrame combinado para mostrar
    df_hist_display = df_hist_sel.rename(columns={'Valor': 'Histórico'})[['Fecha', 'Indicador', 'Histórico', 'Fuente']]
    
    # Pivotear la tabla de proyecciones para un mejor formato
    df_proj_display = df_proj_sel.pivot_table(index='Fecha', columns='Escenario', values='Valor').reset_index()
    
    # Unir las tablas por Fecha
    df_final_display = pd.merge(df_hist_display, df_proj_display, on='Fecha', how='outer')
    df_final_display = df_final_display.sort_values(by='Fecha').reset_index(drop=True)
    
    # Aplicar formato a los números
    for col in df_final_display.columns:
        if df_final_display[col].dtype in [np.float64, np.int64]:
            df_final_display[col] = df_final_display[col].apply(lambda x: format_number(x, decimal_places) if pd.notna(x) else '-')

    st.dataframe(
        df_final_display,
        use_container_width=True,
        hide_index=True
    )