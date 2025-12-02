"""
Generador de PDF Consolidado de Indicadores y Modelos
======================================================

Este módulo automatiza la generación de un único PDF consolidado que contiene:
- Portada general
- Secciones por Línea Estratégica
- Indicadores con todos sus modelos
- Gráficos históricos y proyecciones
- Fichas de resumen y escenarios

Estructura del PDF:
    Portada General
    → Línea Estratégica A
        → Indicador 1
            → Modelo 1 (portada, gráfico, fichas)
            → Modelo 2 (portada, gráfico, fichas)
        → Indicador 2
            → Modelo 1 (portada, gráfico, fichas)
    → Línea Estratégica B
        ...
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image as RLImage, KeepTogether, Frame, PageTemplate
)
from reportlab.pdfgen import canvas
import io
import base64
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

# ==============================
# CONFIGURACIÓN
# ==============================
BASE_DIR = Path(__file__).parent
RUTA_DATASET = BASE_DIR / "Data" / "Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx"
LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"
OUTPUT_PDF = BASE_DIR / "Reporte_Consolidado_Indicadores_Modelos.pdf"

# Configuración de años de comparación
BASE_YEAR = 2025
COMP_YEAR_1 = 2026
COMP_YEAR_2 = 2030

# Indicadores bianuales
BIANUAL_IDS = {202, 361}
BIANUAL_NAMES = {"Great Place to Work", "Índice de Inclusión"}

# Orden manual de indicadores por línea estratégica
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
        "Nivel de Satisfacción Servicios Prestados - Comunicaciones Internas"
    ]
}

# Colores institucionales
COLORES_LINEAS = {
    "Expansión": "#2c5f8d",
    "Transformación_Organizacional": "#1e3a5f",
    "Calidad": "#4a90c8",
    "Experiencia": "#5ca3d6",
    "Sostenibilidad": "#2ecc71",
    "Educación_para_toda_la_vida": "#3498db"
}

COLORES_ESCENARIOS = {
    'Optimista': '#2ecc71',
    'Realista': '#2c5f8d',
    'Base': '#2c5f8d',
    'Pesimista': '#e74c3c',
    'Histórico': '#D4A017'
}

# Mapeo de nombres de modelos
MODELO_DISPLAY_NAMES = {
    'Media_Movil_Tendencia': '📊 Media Móvil Tendencia',
    'ETS': '📈 ETS',
    'Modelo_Conservador': '📉 Modelo Conservador',
    'Polinomial_Grado_2': '📈 Polinomial Grado 2',
    'Proyeccion_CAGR': '🎯 Proyección CAGR',
    'Regresion_Lineal': '📈 Regresión Lineal',
    'Heuristico_2obs': '🔮 Heurístico',
    'Ensemble_Ponderado': '🤝 Ensemble Ponderado',
    'Promedio_Modelos': '➗ Promedio de Modelos',
    'Suavizado_Exponencial': '📊 Suavizado Exponencial'
}

# ==============================
# FUNCIONES AUXILIARES
# ==============================

def cargar_datos():
    """
    Carga los datasets históricos y de proyecciones.
    Normaliza columnas y fechas.

    Returns:
        tuple: (df_hist, df_proj) DataFrames normalizados
    """
    print("📂 Cargando datasets...")

    # Cargar históricos
    if not RUTA_DATASET.exists():
        raise FileNotFoundError(f"❌ No se encontró: {RUTA_DATASET}")

    df_hist = pd.read_excel(str(RUTA_DATASET))

    # Normalizar columna Fecha
    if 'Fecha' not in df_hist.columns:
        posibles_fechas = [c for c in df_hist.columns if str(c).strip().lower().replace(' ', '_') in [
            'fecha', 'periodo', 'periodo_fecha']]
        if posibles_fechas:
            df_hist = df_hist.rename(columns={posibles_fechas[0]: 'Fecha'})

    df_hist["Fecha"] = pd.to_datetime(df_hist["Fecha"], errors='coerce')

    # Cargar proyecciones
    if not RUTA_PROYECCIONES.exists():
        raise FileNotFoundError(f"❌ No se encontró: {RUTA_PROYECCIONES}")

    _sheets = pd.read_excel(str(RUTA_PROYECCIONES), sheet_name=None)
    if isinstance(_sheets, dict):
        df_proj_raw = pd.concat(_sheets.values(), ignore_index=True)
    else:
        df_proj_raw = _sheets

    # Normalizar columnas proyecciones
    colmap = {str(c): str(c).strip().lower().replace(' ', '_').replace('ó', 'o').replace('é', 'e').replace('á', 'a').replace('í','i').replace('ú','u') for c in df_proj_raw.columns}
    df_proj_raw.columns = list(colmap.values())

    # Renombrar columnas clave
    rename_rules = {}
    for cand in ['fecha_proyeccion', 'fecha_proyecccion', 'fecha', 'fecha_proyeccion_']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Fecha_Proyeccion'
            break
    for cand in ['indicador']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Indicador'
            break
    for cand in ['modelo', 'metodo', 'modelo_ml']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Modelo'
            break
    for cand in ['periodicidad']:
        if cand in df_proj_raw.columns:
            rename_rules[cand] = 'Periodicidad'
            break
    if 'escenario_base' in df_proj_raw.columns:
        rename_rules['escenario_base'] = 'Escenario_Realista'
    if 'escenario_pesimista' in df_proj_raw.columns:
        rename_rules['escenario_pesimista'] = 'Escenario_Pesimista'
    if 'escenario_optimista' in df_proj_raw.columns:
        rename_rules['escenario_optimista'] = 'Escenario_Optimista'
    if 'proyeccion' in df_proj_raw.columns:
        rename_rules['proyeccion'] = 'Escenario_Realista'
    if 'ic_inferior' in df_proj_raw.columns:
        rename_rules['ic_inferior'] = 'Escenario_Pesimista'
    if 'ic_superior' in df_proj_raw.columns:
        rename_rules['ic_superior'] = 'Escenario_Optimista'

    if rename_rules:
        df_proj_raw = df_proj_raw.rename(columns=rename_rules)

    # Validar columnas requeridas
    required = {'Indicador', 'Modelo', 'Fecha_Proyeccion', 'Escenario_Realista', 'Escenario_Pesimista', 'Escenario_Optimista'}
    missing = [c for c in required if c not in df_proj_raw.columns]
    if missing:
        raise ValueError(f"❌ Faltan columnas requeridas: {missing}")

    df_proj_raw["Fecha_Proyeccion"] = pd.to_datetime(df_proj_raw["Fecha_Proyeccion"], errors='coerce')

    # Convertir a formato largo
    df_proj_list = []
    for _, row in df_proj_raw.iterrows():
        base_data = {
            'Indicador': row['Indicador'],
            'Periodicidad': row.get('Periodicidad', 'Semestral'),
            'Fecha': row['Fecha_Proyeccion'],
            'Modelo': row['Modelo']
        }
        if pd.notna(row.get('Escenario_Realista')):
            df_proj_list.append({**base_data, 'Escenario': 'Realista', 'Proyección': row['Escenario_Realista']})
        if pd.notna(row.get('Escenario_Pesimista')):
            df_proj_list.append({**base_data, 'Escenario': 'Pesimista', 'Proyección': row['Escenario_Pesimista']})
        if pd.notna(row.get('Escenario_Optimista')):
            df_proj_list.append({**base_data, 'Escenario': 'Optimista', 'Proyección': row['Escenario_Optimista']})

    df_proj = pd.DataFrame(df_proj_list) if df_proj_list else pd.DataFrame()

    print(f"✅ Datos cargados: {len(df_hist)} registros históricos, {len(df_proj)} proyecciones")
    return df_hist, df_proj


def format_number(value, decimals):
    """Formatea un número con decimales especificados."""
    if pd.isna(value):
        return ''
    try:
        decimals = int(decimals) if pd.notna(decimals) else 0
        return f"{float(value):,.{decimals}f}"
    except:
        return str(value)


def ultimo_semestre_val(df_hist_source: pd.DataFrame, target_year: int = 2025):
    """Obtiene el último valor semestral de un año específico."""
    try:
        if df_hist_source is None or df_hist_source.empty:
            return np.nan
        dfh = df_hist_source.copy()
        if 'Fuente' in dfh.columns:
            dfh = dfh[dfh['Fuente'] == 'Semestral']
        dfx = dfh[dfh['Fecha'].dt.year == target_year]
        if not dfx.empty:
            return dfx.sort_values('Fecha').iloc[-1]['Ejecución']
        dfx_prev = dfh[dfh['Fecha'].dt.year == (target_year - 1)]
        if not dfx_prev.empty:
            return dfx_prev.sort_values('Fecha').iloc[-1]['Ejecución']
        dfx_lte = dfh[dfh['Fecha'] <= pd.to_datetime(f'{target_year}-12-31')]
        if not dfx_lte.empty:
            return dfx_lte.sort_values('Fecha').iloc[-1]['Ejecución']
        return np.nan
    except Exception:
        return np.nan


def generar_grafico_plotly(df_hist, df_proj, indicador, modelo, decimal_places, indicador_negativo):
    """
    Genera un gráfico Plotly con históricos y proyecciones.

    Returns:
        io.BytesIO: Buffer con la imagen PNG del gráfico
    """
    fig = go.Figure()

    # Preparar datos históricos semestrales
    df_hist_sem = df_hist[df_hist["Fuente"] == "Semestral"].copy()
    if not df_hist_sem.empty:
        df_hist_sem = df_hist_sem.sort_values('Fecha').copy()
        df_hist_sem['Fecha_Original'] = df_hist_sem['Fecha']
        df_hist_sem['Fecha'] = df_hist_sem['Fecha_Original'].apply(
            lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
        )
        df_hist_sem = df_hist_sem.groupby('Fecha', as_index=False).last()

        # Agregar traza histórica
        fig.add_trace(go.Scatter(
            x=df_hist_sem["Fecha"],
            y=df_hist_sem["Ejecución"],
            name="Histórico Semestral",
            line=dict(color='#D4A017', width=2),
            marker=dict(size=6, color='#D4A017', line=dict(width=1, color='white')),
            mode='lines+markers',
            hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
        ))

    # Agregar proyecciones por escenario
    escenarios = ['Realista', 'Pesimista', 'Optimista']
    for escenario in escenarios:
        df_esc = df_proj[df_proj["Escenario"] == escenario].copy()
        if not df_esc.empty:
            color = COLORES_ESCENARIOS.get(escenario, '#2c5f8d')
            df_plot = df_esc.sort_values('Fecha').copy()
            df_plot['Fecha_Original'] = df_plot['Fecha']
            df_plot['Fecha'] = df_plot['Fecha_Original'].apply(
                lambda x: pd.Timestamp(year=x.year, month=3, day=15) if x.month <= 6 else pd.Timestamp(year=x.year, month=9, day=15)
            )
            df_plot = df_plot.groupby('Fecha', as_index=False).last()
            df_plot = df_plot.sort_values('Fecha')

            fig.add_trace(go.Scatter(
                x=df_plot["Fecha"],
                y=df_plot["Proyección"],
                name=escenario,
                line=dict(color=color, width=2, dash='dot'),
                marker=dict(size=6, color=color, line=dict(width=1, color='white')),
                mode='lines+markers',
                hovertemplate=f'%{{x}}<br>%{{y:,.{int(decimal_places)}f}}<extra></extra>'
            ))

    # Línea divisoria 2025/2026
    fecha_corte = pd.Timestamp(year=2025, month=12, day=31)
    fecha_corte_str = fecha_corte.strftime('%Y-%m-%d')
    fig.add_vline(x=fecha_corte_str, line_width=2, line_dash="dash", line_color="#808080")

    # Configuración del layout
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        height=500,
        font=dict(family="Arial", size=10, color="#1e293b"),
        title=dict(
            text=f"<b>{indicador}</b>",
            x=0.5, y=0.97, xanchor='center', yanchor='top',
            font=dict(size=14, color="#1e3a5f", family="Arial")
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#cbd5e0",
            borderwidth=1,
            font=dict(size=9)
        ),
        xaxis=dict(
            title="<b>PERIODO</b>",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickfont=dict(size=8),
            linecolor='#cbd5e0',
            linewidth=1,
            mirror=True,
            showline=True
        ),
        yaxis=dict(
            title=f"<b>{indicador.upper()}</b>",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickformat=f",.{int(decimal_places)}f",
            tickfont=dict(size=8),
            showline=True,
            linecolor='#cbd5e0',
            linewidth=1,
            mirror=True,
            zeroline=False
        ),
        margin=dict(t=80, b=60, r=30, l=80)
    )

    # Convertir a imagen PNG
    img_bytes = fig.to_image(format="png", width=800, height=500, scale=2)
    return io.BytesIO(img_bytes)


def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a tupla RGB normalizada."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


# ==============================
# CLASES PARA EL PDF
# ==============================

class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado con números de página y header/footer."""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColorRGB(0.5, 0.5, 0.5)
        self.drawRightString(
            A4[0] - 1*cm,
            1*cm,
            f"Página {self._pageNumber} de {page_count}"
        )


# ==============================
# GENERADOR DE CONTENIDO PDF
# ==============================

class GeneradorPDFConsolidado:
    """Genera un PDF consolidado con todos los indicadores y modelos."""

    def __init__(self, df_hist, df_proj):
        self.df_hist = df_hist
        self.df_proj = df_proj
        self.story = []
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()

    def _configurar_estilos(self):
        """Configura estilos personalizados para el PDF."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a5f'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Título de sección
        self.styles.add(ParagraphStyle(
            name='TituloSeccion',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.white,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#2c5f8d'),
            borderPadding=(10, 10, 10, 10)
        ))

        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

        # Título de indicador
        self.styles.add(ParagraphStyle(
            name='TituloIndicador',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a5f'),
            spaceAfter=8,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))

        # Título de modelo
        self.styles.add(ParagraphStyle(
            name='TituloModelo',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2c5f8d'),
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))

        # Normal con justificación
        self.styles.add(ParagraphStyle(
            name='NormalJustificado',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))

    def agregar_portada_general(self):
        """Agrega la portada general del documento."""
        print("📄 Generando portada general...")

        # Logo si existe
        if LOGO_PATH.exists():
            try:
                img = RLImage(str(LOGO_PATH), width=4*inch, height=3*inch)
                self.story.append(Spacer(1, 0.5*inch))
                self.story.append(img)
                self.story.append(Spacer(1, 0.3*inch))
            except Exception as e:
                print(f"⚠️ No se pudo cargar el logo: {e}")

        # Título
        self.story.append(Spacer(1, 0.5*inch))
        titulo = Paragraph(
            "REPORTE CONSOLIDADO DE INDICADORES Y MODELOS",
            self.styles['TituloPrincipal']
        )
        self.story.append(titulo)
        self.story.append(Spacer(1, 0.3*inch))

        # Subtítulo
        subtitulo = Paragraph(
            "Plataforma Prospectiva de Indicadores Institucionales<br/>Análisis y Proyección 2026-2030",
            self.styles['Subtitulo']
        )
        self.story.append(subtitulo)
        self.story.append(Spacer(1, 0.5*inch))

        # Información de generación
        info = Paragraph(
            f"<b>Fecha de generación:</b> {datetime.now().strftime('%d de %B de %Y, %H:%M')}<br/>"
            f"<b>Institución:</b> Politécnico Grancolombiano",
            self.styles['NormalJustificado']
        )
        self.story.append(info)
        self.story.append(PageBreak())

    def agregar_portada_linea(self, linea, color):
        """Agrega una portada de división por Línea Estratégica."""
        print(f"  📂 Generando portada de línea: {linea}")

        # Rectángulo de color de fondo (simulado con tabla)
        data_rect = [['']]
        t_rect = Table(data_rect, colWidths=[7*inch], rowHeights=[1.5*inch])
        t_rect.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(color)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        self.story.append(Spacer(1, 1.5*inch))
        self.story.append(t_rect)
        self.story.append(Spacer(1, 0.3*inch))

        # Título de la línea
        titulo_linea = Paragraph(
            f"<b>LÍNEA ESTRATÉGICA:</b><br/>{linea.replace('_', ' ').upper()}",
            self.styles['TituloSeccion']
        )
        self.story.append(titulo_linea)
        self.story.append(Spacer(1, 0.5*inch))

        # Descripción (opcional, se puede agregar metadata)
        descripcion = Paragraph(
            f"A continuación se presentan los indicadores y modelos de proyección "
            f"asociados a la línea estratégica <b>{linea.replace('_', ' ')}</b>.",
            self.styles['NormalJustificado']
        )
        self.story.append(descripcion)
        self.story.append(PageBreak())

    def agregar_portada_indicador_modelo(self, linea, indicador, modelo):
        """Agrega una portada para cada combinación indicador-modelo."""
        print(f"    📊 Generando portada: {indicador} - {modelo}")

        modelo_display = MODELO_DISPLAY_NAMES.get(modelo, modelo)

        self.story.append(Spacer(1, 1*inch))

        # Título del indicador
        titulo_ind = Paragraph(
            f"<b>INDICADOR:</b><br/>{indicador}",
            self.styles['TituloIndicador']
        )
        self.story.append(titulo_ind)
        self.story.append(Spacer(1, 0.2*inch))

        # Información del modelo
        info_modelo = Paragraph(
            f"<b>Modelo de proyección:</b> {modelo_display}<br/>"
            f"<b>Línea estratégica:</b> {linea.replace('_', ' ')}<br/>"
            f"<b>Fecha de análisis:</b> {datetime.now().strftime('%d/%m/%Y')}",
            self.styles['NormalJustificado']
        )
        self.story.append(info_modelo)
        self.story.append(Spacer(1, 0.3*inch))

    def agregar_ficha_resumen(self, df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo):
        """Agrega la ficha de resumen con métricas clave."""
        print(f"      📋 Generando ficha de resumen...")

        # Obtener datos del escenario Realista
        df_base = df_proj_ind[df_proj_ind["Escenario"] == 'Realista'].copy()

        if df_base.empty:
            self.story.append(Paragraph("⚠️ No hay datos disponibles para el escenario base.", self.styles['Normal']))
            return

        # Calcular métricas
        ultimo_historico = ultimo_semestre_val(df_hist_ind, target_year=BASE_YEAR)
        valor_y1 = df_base[df_base['Fecha'].dt.year == COMP_YEAR_1]['Proyección'].max()
        valor_y2 = df_base[df_base['Fecha'].dt.year == COMP_YEAR_2]['Proyección'].max()
        variacion_periodo = valor_y2 - valor_y1 if pd.notna(valor_y2) and pd.notna(valor_y1) else 0

        # Determinar tendencia
        if variacion_periodo > 0:
            tendencia = "Creciente 🟢"
            color_tend = colors.HexColor('#2ecc71')
        elif variacion_periodo < 0:
            tendencia = "Decreciente 🔴"
            color_tend = colors.HexColor('#e74c3c')
        else:
            tendencia = "Estable 🟡"
            color_tend = colors.HexColor('#f1c40f')

        # Crear tabla de métricas
        data_metricas = [
            ['MÉTRICA', 'VALOR'],
            ['📈 Último Histórico', format_number(ultimo_historico, decimal_places)],
            [f'🎯 Proyección {COMP_YEAR_1}', format_number(valor_y1, decimal_places)],
            [f'⭐ Proyección {COMP_YEAR_2}', format_number(valor_y2, decimal_places)],
            ['Δ Variación Periodo', format_number(variacion_periodo, decimal_places)],
            ['📊 Tendencia Periodo', tendencia]
        ]

        t_metricas = Table(data_metricas, colWidths=[3*inch, 2*inch])
        t_metricas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5f8d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        titulo_ficha = Paragraph("<b>📊 FICHA DE RESUMEN - ESCENARIO BASE</b>", self.styles['TituloModelo'])
        self.story.append(titulo_ficha)
        self.story.append(Spacer(1, 0.1*inch))
        self.story.append(t_metricas)
        self.story.append(Spacer(1, 0.2*inch))

    def agregar_grafico(self, df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo):
        """Agrega el gráfico de evolución histórica y proyección."""
        print(f"      📈 Generando gráfico...")

        try:
            img_buffer = generar_grafico_plotly(
                df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo
            )
            img = RLImage(img_buffer, width=6.5*inch, height=4*inch)

            titulo_grafico = Paragraph("<b>📈 GRÁFICO DE EVOLUCIÓN Y PROYECCIÓN</b>", self.styles['TituloModelo'])
            self.story.append(titulo_grafico)
            self.story.append(Spacer(1, 0.1*inch))
            self.story.append(img)
            self.story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            print(f"      ⚠️ Error generando gráfico: {e}")
            self.story.append(Paragraph(f"⚠️ No se pudo generar el gráfico: {e}", self.styles['Normal']))

    def agregar_ficha_escenarios(self, df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo):
        """Agrega la ficha de comparativo de escenarios."""
        print(f"      📋 Generando ficha de escenarios...")

        escenarios = ['Realista', 'Pesimista', 'Optimista']
        base_historico = ultimo_semestre_val(df_hist_ind, target_year=BASE_YEAR)

        data_escenarios = [['ESCENARIO', f'PROYECCIÓN {COMP_YEAR_1}', f'Δ% vs {BASE_YEAR}', f'PROYECCIÓN {COMP_YEAR_2}', f'Δ% vs {BASE_YEAR}']]

        for escenario in escenarios:
            df_e = df_proj_ind[df_proj_ind['Escenario'] == escenario]

            v_y1 = df_e[df_e['Fecha'].dt.year == COMP_YEAR_1].sort_values('Fecha').iloc[-1]['Proyección'] if not df_e[df_e['Fecha'].dt.year == COMP_YEAR_1].empty else np.nan
            v_y2 = df_e[df_e['Fecha'].dt.year == COMP_YEAR_2].sort_values('Fecha').iloc[-1]['Proyección'] if not df_e[df_e['Fecha'].dt.year == COMP_YEAR_2].empty else np.nan

            pct_y1 = np.nan
            pct_y2 = np.nan
            if pd.notna(base_historico) and base_historico != 0:
                if pd.notna(v_y1):
                    if indicador_negativo:
                        pct_y1 = (base_historico / v_y1 - 1) * 100.0
                    else:
                        pct_y1 = (v_y1 - base_historico) / abs(base_historico) * 100.0
                if pd.notna(v_y2):
                    if indicador_negativo:
                        pct_y2 = (base_historico / v_y2 - 1) * 100.0
                    else:
                        pct_y2 = (v_y2 - base_historico) / abs(base_historico) * 100.0

            data_escenarios.append([
                escenario,
                format_number(v_y1, decimal_places) if pd.notna(v_y1) else 'N/A',
                f"{pct_y1:,.2f}%" if pd.notna(pct_y1) else 'N/A',
                format_number(v_y2, decimal_places) if pd.notna(v_y2) else 'N/A',
                f"{pct_y2:,.2f}%" if pd.notna(pct_y2) else 'N/A'
            ])

        t_escenarios = Table(data_escenarios, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.5*inch, 1.2*inch])
        t_escenarios.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5f8d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor('#e8f5e9'),  # Realista - verde claro
                colors.HexColor('#ffebee'),  # Pesimista - rojo claro
                colors.HexColor('#e3f2fd')   # Optimista - azul claro
            ]),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        titulo_escenarios = Paragraph("<b>🌍 COMPARATIVO DE ESCENARIOS</b>", self.styles['TituloModelo'])
        self.story.append(titulo_escenarios)
        self.story.append(Spacer(1, 0.1*inch))
        self.story.append(t_escenarios)
        self.story.append(Spacer(1, 0.2*inch))

    def generar_pdf(self):
        """Genera el PDF completo con todas las líneas, indicadores y modelos."""
        print("\n🚀 Iniciando generación de PDF consolidado...\n")

        # Portada general
        self.agregar_portada_general()

        # Mapeo de líneas estratégicas
        lineas_estrategicas = {
            "Expansión": ("Expansión", COLORES_LINEAS["Expansión"]),
            "Transformación Organizacional": ("Transformación_Organizacional", COLORES_LINEAS["Transformación_Organizacional"]),
            "Calidad": ("Calidad", COLORES_LINEAS["Calidad"]),
            "Experiencia": ("Experiencia", COLORES_LINEAS["Experiencia"]),
            "Sostenibilidad": ("Sostenibilidad", COLORES_LINEAS["Sostenibilidad"]),
            "Educación para la vida": ("Educación_para_toda_la_vida", COLORES_LINEAS["Educación_para_toda_la_vida"])
        }

        # Iterar por cada línea estratégica
        for linea_display, (linea_key, color_linea) in lineas_estrategicas.items():
            print(f"\n📦 Procesando Línea Estratégica: {linea_display}")

            # Portada de la línea
            self.agregar_portada_linea(linea_display, color_linea)

            # Filtrar indicadores de esta línea
            if 'Linea' in self.df_hist.columns:
                df_hist_linea = self.df_hist[self.df_hist["Linea"] == linea_key]
                if df_hist_linea.empty:
                    df_hist_linea = self.df_hist[self.df_hist["Linea"].str.replace('_', ' ') == linea_display]
            else:
                df_hist_linea = self.df_hist

            # Obtener lista ordenada de indicadores
            indicadores_disponibles = set(df_hist_linea["Indicador"].unique())
            orden_manual = ORDEN_INDICADORES.get(linea_key, [])
            if orden_manual:
                indicadores = [ind for ind in orden_manual if ind in indicadores_disponibles]
                indicadores_faltantes = sorted(indicadores_disponibles - set(indicadores))
                indicadores.extend(indicadores_faltantes)
            else:
                indicadores = sorted(indicadores_disponibles)

            # Iterar por cada indicador
            for indicador in indicadores:
                print(f"\n  📊 Procesando Indicador: {indicador}")

                # Filtrar datos históricos del indicador
                df_hist_ind = df_hist_linea[df_hist_linea["Indicador"] == indicador]

                # Obtener modelos disponibles para este indicador
                modelos = sorted(
                    self.df_proj[self.df_proj['Indicador'] == indicador]['Modelo']
                    .dropna().astype(str).unique()
                )

                if not modelos:
                    print(f"    ⚠️ No hay modelos disponibles para {indicador}")
                    continue

                # Configuración del indicador
                decimal_places = 0
                if 'Decimales_Ejecucion' in df_hist_ind.columns and not df_hist_ind.empty:
                    decimal_places = int(df_hist_ind['Decimales_Ejecucion'].iloc[0]) if pd.notna(df_hist_ind['Decimales_Ejecucion'].iloc[0]) else 0

                indicador_negativo = False
                if 'Sentido' in df_hist_ind.columns and not df_hist_ind.empty:
                    sentido = df_hist_ind['Sentido'].iloc[0] if not df_hist_ind.empty else 'Positivo'
                    indicador_negativo = str(sentido).strip().lower() == 'negativo'

                # Iterar por cada modelo
                for modelo in modelos:
                    print(f"\n    🧠 Procesando Modelo: {modelo}")

                    # Filtrar proyecciones del modelo
                    df_proj_ind = self.df_proj[
                        (self.df_proj["Indicador"] == indicador) &
                        (self.df_proj["Modelo"] == modelo)
                    ].copy()

                    if df_proj_ind.empty:
                        print(f"      ⚠️ No hay proyecciones para {modelo}")
                        continue

                    # Agregar contenido del indicador-modelo
                    self.agregar_portada_indicador_modelo(linea_display, indicador, modelo)
                    self.agregar_ficha_resumen(df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo)
                    self.agregar_grafico(df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo)
                    self.agregar_ficha_escenarios(df_hist_ind, df_proj_ind, indicador, modelo, decimal_places, indicador_negativo)

                    # Salto de página después de cada modelo
                    self.story.append(PageBreak())

        # Construir el PDF
        print("\n📦 Construyendo documento PDF...")
        doc = SimpleDocTemplate(
            str(OUTPUT_PDF),
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )

        doc.build(self.story, canvasmaker=NumberedCanvas)
        print(f"\n✅ PDF generado exitosamente: {OUTPUT_PDF}")
        print(f"📂 Ubicación: {OUTPUT_PDF.absolute()}")


# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def main():
    """Función principal que ejecuta la generación del PDF."""
    print("=" * 80)
    print("GENERADOR DE PDF CONSOLIDADO DE INDICADORES Y MODELOS")
    print("=" * 80)
    print()

    try:
        # Cargar datos
        df_hist, df_proj = cargar_datos()

        # Crear generador y producir PDF
        generador = GeneradorPDFConsolidado(df_hist, df_proj)
        generador.generar_pdf()

        print("\n" + "=" * 80)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ ERROR EN LA GENERACIÓN DEL PDF")
        print("=" * 80)
        print(f"\n{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
