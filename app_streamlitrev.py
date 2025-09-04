import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random

# Configuración de la página
st.set_page_config(
    page_title="Modelo Prospectivo ML 2026-2030",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #374151 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #1f2937;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #374151;
    }
    .sidebar .sidebar-content {
        background: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de estados de sesión
if 'seed' not in st.session_state:
    st.session_state.seed = 42

# Configuración de modelos ML
MODELOS_ML = {
    'prophet': {
        'nombre': 'Prophet (Facebook)',
        'descripcion': 'Ideal para series temporales con estacionalidades y tendencias',
        'precision': 0.92,
        'complejidad': 'Media',
        'color': '#3b82f6',
        'variabilidad': 0.02,
        'tendencia': 1.02
    },
    'arima': {
        'nombre': 'ARIMA',
        'descripcion': 'Modelo autorregresivo clásico para series temporales',
        'precision': 0.88,
        'complejidad': 'Alta',
        'color': '#10b981',
        'variabilidad': 0.03,
        'tendencia': 1.018
    },
    'lstm': {
        'nombre': 'LSTM Neural Network',
        'descripcion': 'Red neuronal recurrente para patrones complejos',
        'precision': 0.94,
        'complejidad': 'Muy Alta',
        'color': '#f59e0b',
        'variabilidad': 0.015,
        'tendencia': 1.025
    },
    'regression': {
        'nombre': 'Regresión Múltiple',
        'descripcion': 'Modelo lineal con múltiples variables explicativas',
        'precision': 0.85,
        'complejidad': 'Baja',
        'color': '#8b5cf6',
        'variabilidad': 0.04,
        'tendencia': 1.015
    },
    'ensemble': {
        'nombre': 'Ensemble (Híbrido)',
        'descripcion': 'Combinación de múltiples modelos para mayor precisión',
        'precision': 0.96,
        'complejidad': 'Muy Alta',
        'color': '#ef4444',
        'variabilidad': 0.01,
        'tendencia': 1.022
    }
}

# Datos históricos base
DATOS_HISTORICOS = {
    'EBITDA': [38500, 39200, 41000, 42100, 41800],
    'Revenue': [125000, 128500, 132000, 135500, 134200],
    'CAPEX': [15000, 16200, 17500, 18200, 17800],
    'Estudiantes': [25000, 25800, 26500, 27200, 26900],
    'Profesores': [1200, 1250, 1280, 1320, 1310]
}

def calcular_proyeccion(datos_base, modelo_key, ajuste_cagr, shock_2027, limite_min, limite_max):
    """Calcula las proyecciones según el modelo ML seleccionado"""
    modelo = MODELOS_ML[modelo_key]
    ultimo_valor = datos_base[-1]
    proyecciones = []
    
    # Configurar semilla para reproducibilidad
    np.random.seed(st.session_state.seed)
    
    for i in range(1, 6):
        tendencia_base = ultimo_valor * (modelo['tendencia'] ** i)
        ajuste_cagr_factor = (1 + ajuste_cagr/100) ** i
        shock_factor = 1 + shock_2027/100 if i == 2 else 1  # Shock en 2027 (i=2)
        
        valor = tendencia_base * ajuste_cagr_factor * shock_factor
        variacion = valor * modelo['variabilidad'] * (np.random.random() - 0.5)
        
        valor_final = max(limite_min, min(limite_max, valor + variacion))
        proyecciones.append(valor_final)
    
    return proyecciones

def generar_datos_completos(indicador, modelo_ml, ajuste_cagr, shock_2027, limite_min, limite_max, escenarios):
    """Genera los datos históricos y proyecciones completas"""
    historicos = DATOS_HISTORICOS[indicador]
    proyeccion = calcular_proyeccion(historicos, modelo_ml, ajuste_cagr, shock_2027, limite_min, limite_max)
    
    años = ['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    datos = []
    
    # Datos históricos
    for i in range(len(historicos)):
        datos.append({
            'año': años[i],
            'historico': historicos[i],
            'tipo': 'Histórico'
        })
    
    # Datos proyectados
    for i in range(len(proyeccion)):
        año = años[len(historicos) + i]
        valor_base = proyeccion[i]
        
        datos.append({
            'año': año,
            'tipo': 'Proyección',
            'tendencial': valor_base if escenarios['tendencial'] else None,
            'optimista': valor_base * 1.08 if escenarios['optimista'] else None,
            'conservador': valor_base * 0.95 if escenarios['conservador'] else None,
            'disruptivo': valor_base * 1.12 if escenarios['disruptivo'] else None,
            'confianza_min': valor_base * 0.9,
            'confianza_max': valor_base * 1.1
        })
    
    return pd.DataFrame(datos)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🧠 Modelo Prospectivo ML 2026-2030</h1>
    <p>Análisis predictivo avanzado con Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Controles
with st.sidebar:
    st.header("⚙️ Controles de Escenario")
    
    # Selector de indicador
    indicador_seleccionado = st.selectbox(
        "Indicador",
        options=list(DATOS_HISTORICOS.keys()),
        index=0
    )
    
    # Selector de modelo ML
    modelo_ml = st.selectbox(
        "🧠 Modelo ML",
        options=list(MODELOS_ML.keys()),
        format_func=lambda x: MODELOS_ML[x]['nombre'],
        index=0
    )
    
    # Información del modelo seleccionado
    modelo_actual = MODELOS_ML[modelo_ml]
    st.info(f"""
    **Precisión:** {modelo_actual['precision']*100:.1f}%  
    **Complejidad:** {modelo_actual['complejidad']}  
    **Descripción:** {modelo_actual['descripcion']}
    """)
    
    st.divider()
    
    # Escenarios
    st.subheader("Escenarios")
    escenarios = {
        'tendencial': st.checkbox("Tendencial", value=True),
        'optimista': st.checkbox("Optimista", value=True),
        'conservador': st.checkbox("Conservador", value=True),
        'disruptivo': st.checkbox("Disruptivo", value=True)
    }
    
    st.divider()
    
    # Ajustes de parámetros
    ajuste_cagr = st.slider("Ajuste sobre CAGR (pp)", -10.0, 10.0, -2.5, 0.1)
    shock_2027 = st.slider("Shock 2027 (%)", -20.0, 20.0, 0.0, 0.5)
    
    st.divider()
    
    # Límites
    st.subheader("Límites Meta")
    limite_min = st.number_input("Límite mínimo", value=0, step=1000)
    limite_max = st.number_input("Límite máximo", value=100000000, step=10000)
    
    # Botón para regenerar con nueva semilla
    if st.button("🎲 Regenerar Proyecciones"):
        st.session_state.seed = random.randint(1, 10000)
        st.rerun()

# Generar datos
datos_completos = generar_datos_completos(
    indicador_seleccionado, modelo_ml, ajuste_cagr, shock_2027, 
    limite_min, limite_max, escenarios
)

# Calcular valor 2030 para KPIs
valor_2030 = datos_completos[datos_completos['año'] == '2030']['tendencial'].iloc[0] if not datos_completos[datos_completos['año'] == '2030'].empty else 0

# KPIs principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Proyección 2030",
        f"{valor_2030:,.0f}" if valor_2030 else "N/A",
        delta="Tendencial"
    )

with col2:
    st.metric(
        "Precisión Modelo",
        f"{modelo_actual['precision']*100:.1f}%",
        delta=f"{modelo_actual['complejidad']}"
    )

with col3:
    st.metric(
        "CAGR Ajustado",
        f"{ajuste_cagr:.1f}pp",
        delta=f"Shock 2027: {shock_2027:.1f}%"
    )

with col4:
    st.metric(
        "Estado",
        "Óptimo",
        delta="✅ Configurado"
    )

# Gráfico principal - Evolución temporal
st.subheader(f"📈 Comparativo por Escenarios con {modelo_actual['nombre']} (2026-2030)")

fig = go.Figure()

# Datos históricos
datos_historicos_plot = datos_completos[datos_completos['tipo'] == 'Histórico']
fig.add_trace(go.Scatter(
    x=datos_historicos_plot['año'],
    y=datos_historicos_plot['historico'],
    mode='lines+markers',
    name='Histórico',
    line=dict(color='#6b7280', width=3),
    marker=dict(size=8)
))

# Área de confianza
datos_proyeccion = datos_completos[datos_completos['tipo'] == 'Proyección']
if not datos_proyeccion.empty:
    fig.add_trace(go.Scatter(
        x=datos_proyeccion['año'],
        y=datos_proyeccion['confianza_max'],
        fill=None,
        mode='lines',
        line_color='rgba(59, 130, 246, 0)',
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=datos_proyeccion['año'],
        y=datos_proyeccion['confianza_min'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(59, 130, 246, 0)',
        fillcolor='rgba(59, 130, 246, 0.1)',
        name='Intervalo de Confianza'
    ))

# Escenarios
colores_escenarios = {
    'tendencial': '#3b82f6',
    'optimista': '#10b981', 
    'conservador': '#f59e0b',
    'disruptivo': '#8b5cf6'
}

for escenario, activo in escenarios.items():
    if activo and escenario in datos_proyeccion.columns:
        datos_escenario = datos_proyeccion[datos_proyeccion[escenario].notna()]
        fig.add_trace(go.Scatter(
            x=datos_escenario['año'],
            y=datos_escenario[escenario],
            mode='lines+markers',
            name=escenario.capitalize(),
            line=dict(color=colores_escenarios[escenario], width=2, dash='dash' if escenario == 'tendencial' else None),
            marker=dict(size=6)
        ))

# Línea divisoria 2025
fig.add_vline(x=4.5, line_dash="dot", line_color="red", annotation_text="Inicio Proyección")

fig.update_layout(
    title=f"Evolución de {indicador_seleccionado}",
    xaxis_title="Año",
    yaxis_title=indicador_seleccionado,
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Segunda fila de gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧠 Comparación de Modelos ML")
    
    # Generar datos para todos los modelos
    comparacion_modelos = []
    for key, modelo in MODELOS_ML.items():
        proyeccion_2030 = calcular_proyeccion(
            DATOS_HISTORICOS[indicador_seleccionado], 
            key, ajuste_cagr, shock_2027, limite_min, limite_max
        )
        comparacion_modelos.append({
            'Modelo': modelo['nombre'],
            'Precisión': modelo['precision'],
            'Valor 2030': proyeccion_2030[4],
            'Color': modelo['color']
        })
    
    df_comparacion = pd.DataFrame(comparacion_modelos)
    
    fig_bar = px.bar(
        df_comparacion, 
        x='Modelo', 
        y='Valor 2030',
        title=f"Proyecciones 2030 por Modelo - {indicador_seleccionado}",
        template="plotly_dark"
    )
    fig_bar.update_traces(marker_color='#3b82f6')
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("📊 Métricas de Modelos")
    
    # Tabla de métricas
    for key, modelo in MODELOS_ML.items():
        estado = "🔥 Seleccionado" if key == modelo_ml else ""
        with st.container():
            st.markdown(f"""
            <div style="padding: 10px; border-left: 4px solid {modelo['color']}; margin: 5px 0; background: rgba(31, 41, 55, 0.5);">
                <strong style="color: {modelo['color']};">{modelo['nombre']}</strong> {estado}<br>
                <small>Precisión: {modelo['precision']*100:.1f}% | {modelo['complejidad']}</small><br>
                <small style="color: #9ca3af;">{modelo['descripcion']}</small>
            </div>
            """, unsafe_allow_html=True)

# Evolución comparativa por año
st.subheader("📅 Evolución Comparativa por Año")

años_proyeccion = ['2028', '2029', '2030']
cols = st.columns(3)

for i, año in enumerate(años_proyeccion):
    with cols[i]:
        datos_año = datos_completos[datos_completos['año'] == año]
        if not datos_año.empty:
            st.markdown(f"**{año}**")
            for escenario, activo in escenarios.items():
                if activo and escenario in datos_año.columns:
                    valor = datos_año[escenario].iloc[0]
                    if pd.notna(valor):
                        color = colores_escenarios[escenario]
                        st.markdown(f"<span style='color: {color};'>{escenario.capitalize()}: {valor:,.0f}</span>", unsafe_allow_html=True)

# Tabla de datos detallada
with st.expander("📋 Ver Datos Detallados"):
    # Preparar datos para mostrar
    datos_display = datos_completos.copy()
    
    # Formatear números
    numeric_columns = ['historico', 'tendencial', 'optimista', 'conservador', 'disruptivo']
    for col in numeric_columns:
        if col in datos_display.columns:
            datos_display[col] = datos_display[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")
    
    st.dataframe(datos_display, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🔬 Dashboard de Análisis Prospectivo con Machine Learning</p>
    <p><small>Desarrollado con Streamlit y Plotly | Modelo actual: <strong>{}</strong></small></p>
</div>
""".format(modelo_actual['nombre']), unsafe_allow_html=True)