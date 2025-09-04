import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors
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
RUTA_DATASET = "Data/Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = "Data/Proyecciones_Multimodelo.xlsx"

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

    # Líneas Estratégicas con colores específicos
    # Mapeo de nombres mostrados a valores en el dataset
    lineas_estrategicas = {
        "Expansión": ("Expansión", "#FBAF17"),
        "Transformación_Organizacional": ("Transformación Organizacional", "#42F2F2"), 
        "Calidad": ("Calidad", "#EC0677"),
        "Experiencia": ("Experiencia", "#1FB2DE"),
        "Sostenibilidad": ("Sostenibilidad", "#A6CE38"),
        "Educación_para_la_vida": ("Educación para la vida", "#0F385A")
    }

    linea_sel = st.selectbox(
        "🎯 Línea Estratégica", 
        list(lineas_estrategicas.keys()),
        help="Selecciona la línea estratégica"
    )

    # Obtener el nombre real de la línea y su color
    linea_real, color_linea = lineas_estrategicas[linea_sel]

    # Filtrar indicadores por línea estratégica seleccionada
    if 'Linea' in df_hist.columns:
        # Filtrar usando el nombre real de la línea
        df_hist_filtrado = df_hist[df_hist["Linea"].str.strip() == linea_real.strip()]
        
        # Verificar si hay datos para la línea seleccionada
        if df_hist_filtrado.empty:
            st.warning(f"No se encontraron datos para la línea: {linea_real}")
            # Mostrar todas las líneas disponibles para depuración
            st.write("Líneas disponibles en el dataset:", df_hist["Linea"].unique())
        
        indicadores = sorted(df_hist_filtrado["Indicador"].unique())
    else:
        indicadores = sorted(df_hist["Indicador"].unique())
    
    indicador_sel = st.selectbox("Selecciona un Indicador", indicadores)
    # Obtener modelos disponibles y filtrar ARIMA
    modelos = df_proj["Modelo"].unique()
    modelos_filtrados = [m for m in modelos if m != "ARIMA"]
    
    # Seleccionar modelo
    modelo_sel = st.selectbox("🧠 Modelo ML", modelos_filtrados, help="Selecciona el modelo de Machine Learning para las proyecciones")

    # Filtrar escenarios por modelo seleccionado
    escenarios_modelo = df_proj[df_proj["Modelo"] == modelo_sel]["Escenario"].unique() if modelo_sel in df_proj["Modelo"].unique() else df_proj["Escenario"].unique()
    st.write("🌍 **Selecciona Escenarios:**")
    
    # Crear checkboxes para cada escenario
    escenarios_sel = []
    for escenario in escenarios_modelo:
        if st.checkbox(f"☐ {escenario}", value=(escenario in escenarios_modelo[:2] if len(escenarios_modelo) >= 2 else True)):
            escenarios_sel.append(escenario)

    # Botón para refrescar (si hay randomización futura)
    if st.button("🔄 Refrescar"):
        st.rerun()
    
    # ==============================
    # CONFIGURACIÓN DEL GRÁFICO
    # ==============================
    st.header("📊 Configuración del Gráfico")
    
    # Tipo de visualización
    tipo_visualizacion = st.selectbox(
        "📈 Tipo de Visualización",
        ["Semestral", "Anual"],
        help="Selecciona qué datos mostrar en el gráfico"
    )
    
    # Tipo de gráfico
    tipo_grafico = st.selectbox(
        "📊 Tipo de Gráfico",
        ["Línea", "Barras", "Dispersión"],
        help="Selecciona el tipo de visualización"
    )
    
    # Mostrar números en el gráfico
    mostrar_numeros = st.checkbox("🔢 Mostrar números en el gráfico", value=True)
    
    # Mostrar línea divisoria
    mostrar_linea_divisoria = st.checkbox("📏 Mostrar línea divisoria", value=True)

# ==============================
# FILTRAR DATOS SEGÚN SELECCIÓN
# ==============================
# Histórico del indicador (filtrado por línea estratégica)
if 'Linea' in df_hist.columns:
    linea_mapping = {
        "Expansión": "Expansión",
        "Transformación": "Transformación", 
        "Calidad": "Calidad",
        "Experiencia": "Experiencia",
        "Sostenibilidad": "Sostenibilidad",
        "Educación_para_la_vida": "Educación para la vida"
    }
    linea_filtro = linea_mapping.get(linea_sel, linea_sel)
    df_hist_sel = df_hist[
        (df_hist["Indicador"] == indicador_sel) &
        (df_hist["Linea"] == linea_filtro)
    ]
else:
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
# Mostrar línea estratégica seleccionada con su color
st.markdown(f"""
<div style="background-color: {color_linea}; padding: 10px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
    <h3 style="color: white; margin: 0;">🎯 Línea Estratégica: {linea_sel}</h3>
</div>
""", unsafe_allow_html=True)

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

# Separar datos históricos por fuente usando las columnas correctas
df_hist_semestral = df_hist_sel[df_hist_sel["Fuente"] == "Semestral"]  # Datos semestrales
df_hist_anual = df_hist_sel[df_hist_sel["Fuente"] == "Cierre"]         # Datos anuales (cierre)

# Configuración avanzada
with st.expander("⚙️ Configuración Avanzada"):
    st.write(f"**Tipo de Visualización:** {tipo_visualizacion}")
    st.info("Ajusta la configuración avanzada del gráfico según tus necesidades.")
    st.write(f"**Tipo de Gráfico:** {tipo_grafico}")
    st.write(f"**Mostrar Números:** {mostrar_numeros}")
    st.write(f"**Mostrar Línea Divisoria:** {mostrar_linea_divisoria}")
    
    st.write("**Columnas disponibles en datos históricos:**")
    st.write(df_hist_sel.columns.tolist())
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Datos Históricos:**")
        st.write(f"- Total: {len(df_hist_sel)} registros")
        st.write(f"- Semestrales (Fuente='Semestral'): {len(df_hist_semestral)} registros")
        st.write(f"- Anuales (Fuente='Cierre'): {len(df_hist_anual)} registros")
        
        if not df_hist_semestral.empty:
            st.write("**Semestrales por semestre:**")
            df_s1 = df_hist_semestral[df_hist_semestral["Semestre"] == 1]
            df_s2 = df_hist_semestral[df_hist_semestral["Semestre"] == 2]
            st.write(f"- Semestre 1: {len(df_s1)} registros")
            st.write(f"- Semestre 2: {len(df_s2)} registros")
        
        if not df_hist_sel.empty:
            st.write("**Fuentes disponibles:**")
            fuentes = df_hist_sel["Fuente"].unique()
            st.write(fuentes.tolist())
        
        if not df_hist_semestral.empty:
            st.write("**Fechas Semestrales:**")
            st.write(df_hist_semestral["Fecha"].dt.strftime("%Y-%m").tolist())
        
        if not df_hist_anual.empty:
            st.write("**Fechas Anuales:**")
            st.write(df_hist_anual["Fecha"].dt.strftime("%Y-%m").tolist())
    
    with col2:
        st.write("**Datos Proyectados:**")
        st.write(f"- Total: {len(df_proj_sel)} registros")
        
        for escenario in escenarios_sel:
            df_esc = df_proj_sel[df_proj_sel["Escenario"] == escenario]
            if not df_esc.empty:
                df_s1 = df_esc[df_esc["Fecha"].dt.month == 6]
                df_s2 = df_esc[df_esc["Fecha"].dt.month == 12]
                st.write(f"- {escenario}: {len(df_esc)} total, {len(df_s1)} S1, {len(df_s2)} S2")

# Función para agregar trazas según el tipo de gráfico
def format_number(value, decimal_places):
    """Formatea un número según la cantidad de decimales especificada"""
    if pd.isna(value) or value == '':
        return ''
    try:
        # Asegurarse de que decimal_places sea un entero
        decimal_places = int(decimal_places) if not pd.isna(decimal_places) else 0
        # Formatear el número con separadores de miles y los decimales correspondientes
        return f"{float(value):,.{decimal_places}f}"
    except (ValueError, TypeError):
        return str(value)

def agregar_traza(fig, x, y, nombre, color, tipo_grafico, mostrar_numeros=True, decimal_places=0):
    """
    Agrega una traza al gráfico con formato personalizado de decimales
    
    Args:
        fig: Figura de Plotly
        x: Datos del eje X
        y: Datos del eje Y
        nombre: Nombre de la traza
        color: Color de la traza
        tipo_grafico: Tipo de gráfico ('Línea', 'Barras', 'Dispersión')
        mostrar_numeros: Si se muestran los valores numéricos
        decimal_places: Número de decimales a mostrar
    """
    # Obtener el formato de texto con los decimales correctos
    text_format = y.apply(lambda val: format_number(val, decimal_places)) if mostrar_numeros else None
    
    # Configuración común para todos los tipos de gráfico
    common_kwargs = {
        'x': x,
        'y': y,
        'name': nombre,
        'hovertemplate': f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>',
        'textfont': dict(size=10, color=color) if mostrar_numeros else None
    }
    
    if tipo_grafico == "Línea":
        # Para líneas, solo mostramos los marcadores sin texto para evitar duplicados
        fig.add_trace(go.Scatter(
            **common_kwargs,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=8, color=color, line=dict(width=1, color='white'))
        ))
        
        # Agregar etiquetas de texto como una traza separada para mejor control
        if mostrar_numeros:
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode="text",
                text=text_format,
                textposition="top center",
                textfont=dict(size=10, color=color),
                showlegend=False,
                hoverinfo='skip'
            ))
            
    elif tipo_grafico == "Barras":
        fig.add_trace(go.Bar(
            **common_kwargs,
            marker_color=color,
            text=text_format if mostrar_numeros else None,
            textposition="outside",
            textfont_size=10,
            textangle=0
        ))
        
    elif tipo_grafico == "Dispersión":
        fig.add_trace(go.Scatter(
            **common_kwargs,
            mode="markers",
            marker=dict(size=10, color=color, symbol="circle", line=dict(width=1, color='white')),
            text=text_format if mostrar_numeros else None,
            textposition="top center"
        ))

# Obtener el número de decimales para el indicador seleccionado
decimal_places = 0  # Valor por defecto
if 'Decimales_Ejecucion' in df_hist_sel.columns and not df_hist_sel.empty:
    # Tomar el primer valor de Decimales_Ejecucion (debería ser el mismo para todos los registros del mismo indicador)
    decimal_places = int(df_hist_sel['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_sel['Decimales_Ejecucion'].iloc[0]) else 0

# Agregar datos históricos según la configuración
if tipo_visualizacion == "Semestral":
    # Para "Semestral" mostrar todos los datos semestrales en una línea
    if not df_hist_semestral.empty:
        agregar_traza(fig, df_hist_semestral["Fecha"], df_hist_semestral["Ejecución"], 
                     "Histórico Semestral", "#3498DB", tipo_grafico, mostrar_numeros, decimal_places)

elif tipo_visualizacion == "Anual":
    # Para "Anual" mostrar solo datos de cierre (anuales)
    if not df_hist_anual.empty:
        agregar_traza(fig, df_hist_anual["Fecha"], df_hist_anual["Ejecución"], 
                     "Histórico Anual (Cierre)", "#FF6B6B", tipo_grafico, mostrar_numeros, decimal_places)

# Si no hay datos separados, mostrar línea histórica general
if df_hist_semestral.empty and df_hist_anual.empty and not df_hist_sel.empty:
    agregar_traza(fig, df_hist_sel["Fecha"], df_hist_sel["Ejecución"], 
                 "Histórico", "#2C3E50", tipo_grafico, mostrar_numeros, decimal_places)

# Agregar proyecciones según la configuración
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
        
        # Agregar proyecciones según la configuración
        if tipo_visualizacion == "Semestral":
            # Para semestral: combinar S1 y S2 en una sola línea continua
            if not df_escenario.empty:
                # Ordenar por fecha para asegurar el orden correcto
                df_escenario = df_escenario.sort_values('Fecha')
                
                # Crear una sola traza para la línea
                fig.add_trace(go.Scatter(
                    x=df_escenario["Fecha"],
                    y=df_escenario["Proyección"],
                    mode='lines+markers',
                    name=escenario,
                    line=dict(color=color, width=2.5),
                    marker=dict(size=8, color=color, symbol='circle', 
                              line=dict(width=1, color='white')),
                    hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
                ))
                
                # Agregar etiquetas de texto para los puntos
                if mostrar_numeros:
                    # Combinar S1 y S2 y ordenar por fecha
                    puntos = []
                    if not df_proj_s1.empty:
                        puntos.extend([(d, v, 'S1') for d, v in zip(df_proj_s1["Fecha"], 
                                                                  df_proj_s1["Proyección"].apply(lambda x: format_number(x, decimal_places)))])
                    if not df_proj_s2.empty:
                        puntos.extend([(d, v, 'S2') for d, v in zip(df_proj_s2["Fecha"], 
                                                                  df_proj_s2["Proyección"].apply(lambda x: format_number(x, decimal_places)))])
                    
                    # Ordenar por fecha
                    puntos.sort()
                    
                    # Agregar una sola traza de texto para todos los puntos
                    if puntos:
                        fechas, valores, _ = zip(*puntos)
                        # Calcular la posición vertical de las etiquetas (más cerca de los puntos)
                        y_positions = df_escenario[df_escenario["Fecha"].isin(fechas)]["Proyección"]
                        offset = y_positions.max() * 0.015  # Reducir el desplazamiento vertical
                        
                        fig.add_trace(go.Scatter(
                            x=fechas,
                            y=y_positions + offset,  # Ajuste más sutil
                            mode='text',
                            text=valores,
                            textposition='top center',
                            textfont=dict(size=10, color=color, family='Arial'),
                            showlegend=False,
                            hoverinfo='skip'
                        ))
                
        elif tipo_visualizacion == "Anual":
            # Para anual: mostrar solo diciembre (S2)
            if not df_proj_s2.empty:
                agregar_traza(fig, df_proj_s2["Fecha"], df_proj_s2["Proyección"], 
                             f"{escenario} (S2)", color, tipo_grafico, mostrar_numeros, decimal_places)
            elif not df_escenario.empty:
                # Si no hay datos anuales específicos, mostrar todos los datos
                agregar_traza(fig, df_escenario["Fecha"], df_escenario["Proyección"], 
                             f"{escenario}", color, tipo_grafico, mostrar_numeros, decimal_places)
        
        # Si no hay datos separados por semestre y no se ha agregado nada, mostrar línea general
        if df_proj_s1.empty and df_proj_s2.empty and tipo_visualizacion == "Semestral y Anual":
            agregar_traza(fig, df_escenario["Fecha"], df_escenario["Proyección"], 
                         f"Proyección ({modelo_sel}-{escenario})", color, tipo_grafico, mostrar_numeros)

# Línea vertical divisoria entre histórico y proyección
if mostrar_linea_divisoria and not df_hist_sel.empty and not df_proj_sel.empty:
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
    template="plotly_white",  # Cambiar a tema claro para mejor legibilidad
    xaxis_title="Fecha",
    yaxis_title=indicador_sel,
    height=600,  # Aumentar altura para mejor visualización
    margin=dict(l=50, r=50, t=80, b=80),  # Márgenes más amplios
    font=dict(family="Arial", size=12, color="#2c3e50"),  # Fuente más legible
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
    
    
