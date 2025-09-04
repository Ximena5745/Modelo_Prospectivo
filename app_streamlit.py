import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ============================
# CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="Prospectiva Indicadores Poli", layout="wide")

# Rutas de archivos (ajusta si cambian)
FILE_HIST = "Data/Dataset_Unificado.xlsx"
FILE_PROY = "Data/Proyecciones_Multimodelo.xlsx"

# ============================
# CARGA DE DATOS
# ============================
@st.cache_data
def load_data():
    # Leer histórico
    df_hist = pd.read_excel(FILE_HIST, sheet_name="Unificado")
    df_hist.columns = df_hist.columns.str.strip().str.lower()  # limpiar nombres columnas
    
    # Convertir fecha
    if "fecha" in df_hist.columns:
        df_hist["fecha"] = pd.to_datetime(df_hist["fecha"], errors="coerce")

    # Leer proyecciones
    df_proj = pd.read_excel(FILE_PROY)
    df_proj.columns = df_proj.columns.str.strip().str.lower()
    
    if "fecha" in df_proj.columns:
        df_proj["fecha"] = pd.to_datetime(df_proj["fecha"], errors="coerce")
    
    return df_hist, df_proj

df_hist, df_proj = load_data()

# ============================
# SIDEBAR
# ============================
st.sidebar.header("Filtros")

# Lista de indicadores
indicadores = sorted(df_hist["indicador"].dropna().unique())
indicador_sel = st.sidebar.selectbox("Selecciona un indicador", indicadores)

# Escenario
escenarios = sorted(df_proj["escenario"].dropna().unique())
escenario_sel = st.sidebar.radio("Escenario", escenarios, index=0)

# ============================
# FILTRADO DE DATOS
# ============================
df_hist_filt = df_hist[df_hist["indicador"] == indicador_sel]
df_proj_filt = df_proj[(df_proj["indicador"] == indicador_sel) & (df_proj["escenario"] == escenario_sel)]

# ============================
# GRÁFICO
# ============================
st.subheader(f"📊 Evolución del Indicador: {indicador_sel} ({escenario_sel})")

fig = px.line()

# Línea histórica
if not df_hist_filt.empty:
    fig.add_scatter(
        x=df_hist_filt["fecha"],
        y=df_hist_filt["ejecución"],
        mode="lines+markers",
        name="Histórico",
        line=dict(color="blue")
    )

# Proyecciones por modelo
if not df_proj_filt.empty:
    for modelo in df_proj_filt["modelo"].unique():
        df_m = df_proj_filt[df_proj_filt["modelo"] == modelo]
        fig.add_scatter(
            x=df_m["fecha"],
            y=df_m["proyección"],
            mode="lines+markers",
            name=f"Proyección - {modelo}"
        )

fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Valor",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ============================
# TABLAS
# ============================
col1, col2 = st.columns(2)

with col1:
    st.write("### 📑 Datos Históricos")
    st.dataframe(df_hist_filt[["fecha", "meta", "ejecución", "cumplimiento", "cumplimiento real"]])

with col2:
    st.write("### 🔮 Proyecciones")
    st.dataframe(df_proj_filt[["fecha", "proyección", "modelo", "escenario"]])

# ============================
# INFO EXTRA
# ============================
st.sidebar.markdown("---")
st.sidebar.info("Este dashboard combina histórico (`Dataset_Unificado.xlsx`) con proyecciones (`Proyecciones_Multimodelo.xlsx`).")
