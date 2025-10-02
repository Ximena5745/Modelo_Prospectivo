import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(
    page_title="📊 Modelo Prospectivo",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Fondo general */
    .main {
        background-color: #f8fbff;
    }
    /* Encabezados */
    h1, h2, h3 {
        color: #0a2342 !important;
    }
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #0a2342;
        font-weight: bold;
    }
    /* Tarjetas */
    .stTabs [role="tablist"] {
        background-color: #e6f0ff;
        border-radius: 10px;
        padding: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# CARGA DE DATOS
# ==============================
@st.cache_data
def load_data():
    df_hist = pd.read_excel("data/historico_indicadores.xlsx")
    df_proj = pd.read_excel("data/proyecciones_multimodelo.xlsx")
    return df_hist, df_proj

df_hist, df_proj = load_data()

# ==============================
# NORMALIZACIÓN DE COLUMNAS
# ==============================
df_hist.columns = [str(c).strip().lower() for c in df_hist.columns]
df_proj.columns = [str(c).strip().lower() for c in df_proj.columns]

rename_map = {
    "linea": "Linea",
    "indicador": "Indicador",
    "fecha": "Fecha",
    "valor": "Valor",
    "modelo": "Modelo",
    "escenario": "Escenario",
    "proyeccion": "Proyección"
}

df_hist.rename(columns={k: v for k, v in rename_map.items() if k in df_hist.columns}, inplace=True)
df_proj.rename(columns={k: v for k, v in rename_map.items() if k in df_proj.columns}, inplace=True)

# Columnas mínimas
if "Linea" not in df_hist.columns:
    df_hist["Linea"] = "General"
if "Indicador" not in df_hist.columns:
    df_hist["Indicador"] = "Indicador Genérico"
if "Modelo" not in df_proj.columns:
    df_proj["Modelo"] = "No Definido"
if "Escenario" not in df_proj.columns:
    df_proj["Escenario"] = "Escenario Único"

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("⚙️ Configuración")

linea_sel = st.sidebar.selectbox("📌 Línea", sorted(df_hist["Linea"].unique()))
indicador_sel = st.sidebar.selectbox(
    "📊 Indicador",
    sorted(df_hist[df_hist["Linea"] == linea_sel]["Indicador"].unique())
)

tipo_visualizacion = st.sidebar.radio("📅 Tipo de visualización", ["Anual", "Semestral"])
tipo_grafico = st.sidebar.radio("📈 Tipo de gráfico", ["Líneas", "Barras", "Dispersión"])
mostrar_linea_divisoria = st.sidebar.checkbox("➖ Mostrar línea divisoria entre histórico y proyecciones", True)
mostrar_numeros = st.sidebar.checkbox("🔢 Mostrar valores en el gráfico", False)

# ==============================
# FILTRO DE DATOS
# ==============================
df_hist_sel = df_hist[(df_hist["Linea"] == linea_sel) & (df_hist["Indicador"] == indicador_sel)]
df_proj_sel = df_proj[(df_proj["Linea"] == linea_sel) & (df_proj["Indicador"] == indicador_sel)]

# ==============================
# TÍTULO PRINCIPAL
# ==============================
st.title("📊 Tablero Prospectivo de Indicadores")
st.markdown(f"**Línea seleccionada:** {linea_sel} | **Indicador:** {indicador_sel}")

# ==============================
# KPIs PRINCIPALES (valores 2030 por escenario)
# ==============================
st.subheader("📌 Proyecciones 2030 por escenario")

df_kpis = df_proj_sel[df_proj_sel["Fecha"] == 2030]

cols = st.columns(len(df_kpis["Escenario"].unique()) if not df_kpis.empty else 1)
if not df_kpis.empty:
    for i, (escenario, valor) in enumerate(df_kpis.groupby("Escenario")["Proyección"].mean().items()):
        cols[i].metric(label=f"Escenario {escenario}", value=f"{valor:,.2f}")
else:
    st.info("ℹ️ No hay proyecciones para el año 2030 en este indicador.")

# ==============================
# VISUALIZACIÓN PRINCIPAL
# ==============================
st.subheader("📈 Tendencia histórica y proyecciones")

df_hist_sel["Tipo"] = "Histórico"
df_proj_sel["Tipo"] = "Proyección"

df_viz = pd.concat(
    [
        df_hist_sel.rename(columns={"Valor": "Resultado"}),
        df_proj_sel.rename(columns={"Proyección": "Resultado"})
    ],
    ignore_index=True
)

if tipo_visualizacion == "Semestral" and "Fecha" in df_viz.columns:
    df_viz["Periodo"] = df_viz["Fecha"].astype(str) + "-S1"
else:
    df_viz["Periodo"] = df_viz["Fecha"]

tab1, tab2, tab3 = st.tabs(["📊 Gráfico", "📋 Datos", "💡 Insights"])

with tab1:
    if tipo_grafico == "Líneas":
        fig = px.line(df_viz, x="Periodo", y="Resultado", color="Tipo",
                      line_dash="Tipo", markers=True,
                      title=f"Tendencia del Indicador {indicador_sel}")
    elif tipo_grafico == "Barras":
        fig = px.bar(df_viz, x="Periodo", y="Resultado", color="Tipo",
                     barmode="group", title=f"Tendencia del Indicador {indicador_sel}")
    else:
        fig = px.scatter(df_viz, x="Periodo", y="Resultado", color="Tipo",
                         title=f"Tendencia del Indicador {indicador_sel}")

    if mostrar_linea_divisoria:
        if "Tipo" in df_viz.columns and "Histórico" in df_viz["Tipo"].values:
            max_hist = df_viz[df_viz["Tipo"] == "Histórico"]["Periodo"].max()
            fig.add_vline(x=max_hist, line_dash="dash", line_color="gray")

    if mostrar_numeros:
        fig.update_traces(text=df_viz["Resultado"].round(2),
                          textposition="top center")

    fig.update_layout(
        title_x=0.3,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12, color="#0a2342"),
        legend=dict(orientation="h", y=-0.2, x=0.3),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.dataframe(df_viz, use_container_width=True)

with tab3:
    st.write("🔎 **Insights automáticos**")
    try:
        ultimo_hist = df_hist_sel[df_hist_sel["Fecha"] == df_hist_sel["Fecha"].max()]["Valor"].mean()
        proj_2030 = df_proj_sel[df_proj_sel["Fecha"] == 2030]["Proyección"].mean()
        crecimiento = proj_2030 - ultimo_hist
        st.write(f"📈 Crecimiento proyectado al 2030: **{crecimiento:,.2f} unidades** respecto al último dato histórico.")
    except:
        st.warning("⚠️ No fue posible calcular insights por datos incompletos.")
