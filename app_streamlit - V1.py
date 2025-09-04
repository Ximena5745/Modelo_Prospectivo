import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random


# ==============================
# CONFIGURACIÓN STREAMLIT
# ==============================
st.set_page_config(
    page_title="Modelo Prospectivo ML 2026-2030",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================
# LECTURA DE DATOS REALES
# ==============================
RUTA_DATASET = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\Data\Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\Proyecciones\Proyecciones_Multimodelo.xlsx"

# Datos históricos
df_hist = pd.read_excel(RUTA_DATASET)
df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"])

# Proyecciones (2026-2030)
df_proj = pd.read_excel(RUTA_PROYECCIONES)
df_proj["Fecha"] = pd.to_datetime(df_proj["Fecha"])


# ==============================
# SIDEBAR - CONTROLES
# ==============================
with st.sidebar:
    st.header("⚙️ Controles de Escenario")

    indicadores = sorted(df_hist["Indicador"].unique())
    indicador_sel = st.selectbox("Selecciona un Indicador", indicadores)

    modelos = df_proj["Modelo"].unique()
    modelo_sel = st.selectbox("🧠 Modelo ML", modelos)

    escenarios = df_proj["Escenario"].unique()
    st.write("🌍 **Selecciona Escenarios:**")
    
    # Crear checkboxes para cada escenario
    escenarios_sel = []
    for escenario in escenarios:
        if st.checkbox(f"☐ {escenario}", value=(escenario in escenarios[:2] if len(escenarios) >= 2 else True)):
            escenarios_sel.append(escenario)

    # Botón para refrescar (si hay randomización futura)
    if st.button("🔄 Refrescar"):
        st.rerun()

# ==============================
# FILTRAR DATOS SEGÚN SELECCIÓN
# ==============================
# Histórico del indicador
df_hist_sel = df_hist[df_hist["Indicador"] == indicador_sel]

# Proyección del indicador (múltiples escenarios)
df_proj_sel = df_proj[
    (df_proj["Indicador"] == indicador_sel) &
    (df_proj["Modelo"] == modelo_sel) &
    (df_proj["Escenario"].isin(escenarios_sel))
]

# ==============================
# KPIs PRINCIPALES (valores 2030 por escenario)
# ==============================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 Modelo seleccionado", modelo_sel)
with col2:
    st.metric("🌍 Escenarios activos", len(escenarios_sel))
with col3:
    if not df_proj_sel.empty:
        df2030 = df_proj_sel[df_proj_sel["Fecha"].dt.year == 2030]
        if not df2030.empty:
            valor_promedio_2030 = df2030["Proyección"].mean()
            st.metric("📌 Promedio 2030", f"{valor_promedio_2030:,.0f}")
        else:
            st.metric("📌 Promedio 2030", "N/A")
    else:
        st.metric("📌 Promedio 2030", "N/A")

# ==============================
# GRÁFICO PRINCIPAL
# ==============================
st.subheader(f"📊 Evolución del Indicador: {indicador_sel}")

fig = go.Figure()

# Líneas históricas diferenciadas por fuente
# Separar datos semestrales y anuales
df_hist_semestral = df_hist_sel[df_hist_sel["Fecha"].dt.month == 6]  # Junio (semestre 1)
df_hist_anual = df_hist_sel[df_hist_sel["Fecha"].dt.month == 12]     # Diciembre (semestre 2/anual)

# Línea histórica semestral (semestre 1)
if not df_hist_semestral.empty:
    fig.add_trace(go.Scatter(
        x=df_hist_semestral["Fecha"],
        y=df_hist_semestral["Ejecución"],
        mode="lines+markers+text",
        name="Histórico Semestral (S1)",
        line=dict(color="#3498DB", width=3),
        marker=dict(size=6, color="#3498DB", symbol="circle"),
        text=df_hist_semestral["Ejecución"].apply(lambda x: f"{x:,.0f}"),
        textposition="top center",
        textfont=dict(size=10, color="#3498DB")
    ))

# Línea histórica anual (semestre 2)
if not df_hist_anual.empty:
    fig.add_trace(go.Scatter(
        x=df_hist_anual["Fecha"],
        y=df_hist_anual["Ejecución"],
        mode="lines+markers+text",
        name="Histórico Anual (S2)",
        line=dict(color="#E74C3C", width=4),
        marker=dict(size=8, color="#E74C3C", symbol="square"),
        text=df_hist_anual["Ejecución"].apply(lambda x: f"{x:,.0f}"),
        textposition="top center",
        textfont=dict(size=10, color="#E74C3C")
    ))

# Si no hay datos separados, mostrar línea histórica general
if df_hist_semestral.empty and df_hist_anual.empty:
    fig.add_trace(go.Scatter(
        x=df_hist_sel["Fecha"],
        y=df_hist_sel["Ejecución"],
        mode="lines+markers+text",
        name="Histórico",
        line=dict(color="#2C3E50", width=4),
        marker=dict(size=6, color="#2C3E50"),
        text=df_hist_sel["Ejecución"].apply(lambda x: f"{x:,.0f}"),
        textposition="top center",
        textfont=dict(size=10, color="#2C3E50")
    ))

# Líneas proyectadas para cada escenario con colores específicos (semestralizadas)
colores = ['#FF00FF', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
for i, escenario in enumerate(escenarios_sel):
    df_escenario = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    if not df_escenario.empty:
        # Separar proyecciones por semestre
        df_proj_s1 = df_escenario[df_escenario["Fecha"].dt.month == 6]  # Junio (S1)
        df_proj_s2 = df_escenario[df_escenario["Fecha"].dt.month == 12]  # Diciembre (S2)
        
        # Asignar colores específicos según el tipo de escenario
        if "optimista" in escenario.lower() or "alto" in escenario.lower():
            color = "#00FF00"  # Verde brillante para optimista
        elif "pesimista" in escenario.lower() or "bajo" in escenario.lower():
            color = "#FF0000"  # Rojo para pesimista
        else:
            color = colores[i % len(colores)]  # Color por defecto
        
        # Proyección Semestre 1 (Junio)
        if not df_proj_s1.empty:
            fig.add_trace(go.Scatter(
                x=df_proj_s1["Fecha"],
                y=df_proj_s1["Proyección"],
                mode="lines+markers+text",
                name=f"Proyección S1 ({modelo_sel}-{escenario})",
                line=dict(color=color, width=2, dash="dash"),
                marker=dict(size=5, color=color, symbol="diamond"),
                text=df_proj_s1["Proyección"].apply(lambda x: f"{x:,.0f}"),
                textposition="top center",
                textfont=dict(size=10, color=color)
            ))
        
        # Proyección Semestre 2 (Diciembre)
        if not df_proj_s2.empty:
            fig.add_trace(go.Scatter(
                x=df_proj_s2["Fecha"],
                y=df_proj_s2["Proyección"],
                mode="lines+markers+text",
                name=f"Proyección S2 ({modelo_sel}-{escenario})",
                line=dict(color=color, width=3, dash="dash"),
                marker=dict(size=6, color=color, symbol="diamond"),
                text=df_proj_s2["Proyección"].apply(lambda x: f"{x:,.0f}"),
                textposition="top center",
                textfont=dict(size=10, color=color)
            ))
        
        # Si no hay datos separados por semestre, mostrar línea general
        if df_proj_s1.empty and df_proj_s2.empty:
            fig.add_trace(go.Scatter(
                x=df_escenario["Fecha"],
                y=df_escenario["Proyección"],
                mode="lines+markers+text",
                name=f"Proyección ({modelo_sel}-{escenario})",
                line=dict(color=color, width=3, dash="dash"),
                marker=dict(size=5, color=color, symbol="diamond"),
                text=df_escenario["Proyección"].apply(lambda x: f"{x:,.0f}"),
                textposition="top center",
                textfont=dict(size=10, color=color)
            ))

# Línea vertical divisoria entre histórico y proyección
if not df_hist_sel.empty and not df_proj_sel.empty:
    # Fecha específica para la división: 2025-S2 (diciembre de 2025)
    fecha_division = pd.Timestamp('2025-12-31')
    
    # Agregar línea vertical usando add_shape
    fig.add_shape(
        type="line",
        x0=fecha_division,
        x1=fecha_division,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="red", width=3, dash="dash")
    )
    
    # Agregar anotación para la línea divisoria
    fig.add_annotation(
        x=fecha_division,
        y=0.95,
        yref="paper",
        text="División Histórico/Proyección",
        showarrow=False,
        font=dict(color="red", size=12),
        xanchor="left"
    )

# Combinar fechas históricas y proyectadas para el eje X
todas_fechas = pd.concat([df_hist_sel["Fecha"], df_proj_sel["Fecha"]]).drop_duplicates().sort_values()

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Fecha",
    yaxis_title=indicador_sel,
    height=500,
    yaxis=dict(
        tickformat=",",
        separatethousands=True
    ),
    xaxis=dict(
        tickformat="%Y-%m",
        tickmode="array",
        ticktext=[f"{fecha.year}-S{1 if fecha.month <= 6 else 2}" for fecha in todas_fechas],
        tickvals=todas_fechas.tolist(),
        tickangle=45
    )
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# TABLA DE DATOS
# ==============================
with st.expander("📋 Ver Datos Detallados"):
    # Datos históricos
    df_hist_display = df_hist_sel.rename(columns={"Ejecución": "Valor"})[["Fecha", "Indicador", "Valor"]]
    df_hist_display["Tipo"] = "Histórico"
    df_hist_display["Escenario"] = "N/A"
    
    # Datos proyectados
    df_proj_display = df_proj_sel.rename(columns={"Proyección": "Valor"})[["Fecha", "Indicador", "Valor", "Escenario"]]
    df_proj_display["Tipo"] = "Proyección"
    
    # Combinar datos
    df_merge = pd.concat([df_hist_display, df_proj_display])
    st.dataframe(df_merge.sort_values("Fecha"), use_container_width=True)

# ==============================
# FICHAS DE RESUMEN DE ESCENARIOS
# ==============================
st.subheader("📊 Resumen de Escenarios")

# Calcular valores de referencia (último valor histórico)
# Priorizar datos anuales sobre semestrales
if not df_hist_anual.empty:
    ultimo_valor_historico = df_hist_anual["Ejecución"].iloc[-1]
elif not df_hist_semestral.empty:
    ultimo_valor_historico = df_hist_semestral["Ejecución"].iloc[-1]
else:
    ultimo_valor_historico = df_hist_sel["Ejecución"].iloc[-1] if not df_hist_sel.empty else 0

# Definir colores para las fichas
colores_fichas = ['#FF00FF', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']

# Crear fichas para cada escenario seleccionado
for i, escenario in enumerate(escenarios_sel):
    df_escenario = df_proj_sel[df_proj_sel["Escenario"] == escenario]
    
    if not df_escenario.empty:
        # Valores del escenario
        valor_2026 = df_escenario[df_escenario["Fecha"].dt.year == 2026]["Proyección"].iloc[0] if not df_escenario[df_escenario["Fecha"].dt.year == 2026].empty else 0
        valor_2030 = df_escenario[df_escenario["Fecha"].dt.year == 2030]["Proyección"].iloc[0] if not df_escenario[df_escenario["Fecha"].dt.year == 2030].empty else 0
        
        # Cálculos de variación
        variacion_2026 = ((valor_2026 - ultimo_valor_historico) / ultimo_valor_historico * 100) if ultimo_valor_historico != 0 else 0
        variacion_2030 = ((valor_2030 - ultimo_valor_historico) / ultimo_valor_historico * 100) if ultimo_valor_historico != 0 else 0
        variacion_periodo = ((valor_2030 - valor_2026) / valor_2026 * 100) if valor_2026 != 0 else 0
        
        # Determinar color y tipo de escenario
        if "optimista" in escenario.lower() or "alto" in escenario.lower():
            color = "#00FF00"  # Verde brillante
            tipo_escenario = "Optimista"
        elif "pesimista" in escenario.lower() or "bajo" in escenario.lower():
            color = "#FF0000"  # Rojo
            tipo_escenario = "Pesimista"
        else:
            color = colores_fichas[i % len(colores_fichas)]
            tipo_escenario = "Neutral"
        
        # Crear ficha con columnas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                <h3>🌍 {escenario}</h3>
                <p style="font-size: 14px; margin: 5px 0;">{tipo_escenario}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric(
                "📈 2026",
                f"{valor_2026:,.0f}",
                f"{variacion_2026:+.1f}%"
            )
        
        with col3:
            st.metric(
                "🎯 2030",
                f"{valor_2030:,.0f}",
                f"{variacion_2030:+.1f}%"
            )
        
        with col4:
            st.metric(
                "📊 Variación 2026-2030",
                f"{variacion_periodo:+.1f}%",
                f"{valor_2030 - valor_2026:+,.0f}"
            )
        
        with col5:
            # Indicador de tendencia con mejor visualización
            if variacion_periodo > 0:
                tendencia = "🟢 Creciente"
                color_tendencia = "#d4edda"
                color_texto = "#155724"
            elif variacion_periodo < 0:
                tendencia = "🔴 Decreciente"
                color_tendencia = "#f8d7da"
                color_texto = "#721c24"
            else:
                tendencia = "🟡 Estable"
                color_tendencia = "#fff3cd"
                color_texto = "#856404"
            
            st.markdown(f"""
            <div style="background-color: {color_tendencia}; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid {color_texto};">
                <h4 style="color: {color_texto}; margin: 0;">{tendencia}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")  # Separador entre fichas
    
    
