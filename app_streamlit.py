import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="Modelo Prospectivo 2030", layout="wide")

# Directorio base
BASE_DIR = Path.cwd()

# ==============================
# CARGA DE DATOS
# ==============================
file_hist = BASE_DIR / "Data" / "historico_indicadores.xlsx"
file_proj = BASE_DIR / "Data" / "proyecciones_indicadores.xlsx"

df_hist = pd.read_excel(file_hist) if file_hist.exists() else pd.DataFrame()
df_proj = pd.read_excel(file_proj) if file_proj.exists() else pd.DataFrame()

# Normalización de columnas mínimas
if "Linea" not in df_hist.columns:
    df_hist["Linea"] = "General"
if "Modelo" not in df_proj.columns:
    df_proj["Modelo"] = "No Definido"

# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("⚙️ Configuración")

linea_sel = st.sidebar.selectbox("🎯 Línea Estratégica", sorted(df_hist["Linea"].unique()))
indicador_sel = st.sidebar.selectbox("📊 Indicador", sorted(df_hist[df_hist["Linea"] == linea_sel]["Indicador"].unique()))

tipo_grafico = st.sidebar.radio("Tipo de gráfico", ["Líneas", "Barras", "Dispersión"])
mostrar_numeros = st.sidebar.checkbox("Mostrar números en puntos", value=True)
mostrar_linea_divisoria = st.sidebar.checkbox("Dividir histórico y proyecciones", value=True)

# ==============================
# FILTROS
# ==============================
df_hist_sel = df_hist[(df_hist["Linea"] == linea_sel) & (df_hist["Indicador"] == indicador_sel)]
df_proj_sel = df_proj[(df_proj["Linea"] == linea_sel) & (df_proj["Indicador"] == indicador_sel)]

# ==============================
# FUNCIÓN: GENERAR GRÁFICO
# ==============================
def generar_grafico(df_hist_sel, df_proj_sel, tipo_grafico, mostrar_numeros, mostrar_linea_divisoria):
    fig = go.Figure()

    # Histórico
    if not df_hist_sel.empty:
        fig.add_trace(go.Scatter(
            x=df_hist_sel["Fecha"],
            y=df_hist_sel["Valor"],
            mode="lines+markers",
            name="Histórico",
            line=dict(color="#0F385A", width=3)
        ))

    # Proyecciones
    for escenario in df_proj_sel["Escenario"].unique():
        df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
        fig.add_trace(go.Scatter(
            x=df_esc["Fecha"],
            y=df_esc["Proyección"],
            mode="lines+markers" if mostrar_numeros else "lines",
            name=f"Escenario {escenario}"
        ))

    # Línea divisoria
    if mostrar_linea_divisoria:
        fig.add_vline(
            x=pd.to_datetime("2026-01-01"),
            line_width=2,
            line_dash="dash",
            line_color="red"
        )

    fig.update_layout(
        template="plotly_white",
        title=f"Evolución del Indicador: {indicador_sel}",
        xaxis_title="Fecha",
        yaxis_title="Valor",
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

# ==============================
# VISUALIZACIÓN PRINCIPAL
# ==============================
st.title("📈 Modelo Prospectivo al 2030")
st.markdown(f"### Línea Estratégica: **{linea_sel}** | Indicador: **{indicador_sel}**")

fig = generar_grafico(df_hist_sel, df_proj_sel, tipo_grafico, mostrar_numeros, mostrar_linea_divisoria)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# KPIs AL 2030
# ==============================
if not df_proj_sel.empty:
    st.subheader("📌 KPIs al 2030")

    df_2030 = df_proj_sel[df_proj_sel["Fecha"].dt.year == 2030]
    cols = st.columns(len(df_2030["Escenario"].unique()))

    for i, escenario in enumerate(sorted(df_2030["Escenario"].unique())):
        valor = df_2030[df_2030["Escenario"] == escenario]["Proyección"].mean()
        delta = ((valor / df_hist_sel["Valor"].iloc[-1]) - 1) * 100 if not df_hist_sel.empty else None

        with cols[i]:
            st.metric(
                label=f"{escenario} 2030",
                value=f"{valor:,.2f}",
                delta=f"{delta:.1f}%" if delta else None,
                help=f"Proyección {escenario} al 2030"
            )

# ==============================
# DESCARGA DE DATOS
# ==============================
st.download_button(
    "⬇️ Descargar datos filtrados",
    df_proj_sel.to_csv(index=False).encode("utf-8"),
    "Proyecciones.csv",
    "text/csv",
    key="download-csv"
)
