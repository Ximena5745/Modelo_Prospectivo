# generar_informe_unificado.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
from datetime import datetime

# ---------------- CONFIG ----------------
INPUT_FILE = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Data\Dataset_Unificado.xlsx"
SHEET_NAME = "Unificado"
OUTPUT_PDF = "Informe_Ejecutivo_Unificado.pdf"
LOGO_PATH = None   # opcional: r"C:\ruta\a\logo.png"

# Columnas EXACTAS según la estructura que enviaste
COL = {
    'id': 'Id',
    'indicador': 'Indicador',
    'proceso': 'Proceso',
    'periodicidad': 'Periodicidad',
    'sentido': 'Sentido',
    'fecha': 'Fecha',
    'anio': 'Año',
    'mes': 'Mes',
    'periodo': 'Periodo',
    'semestre': 'Semestre',
    'meta': 'Meta',
    'ejecucion': 'Ejecución',
    'cumplimiento': 'Cumplimiento',
    'cumplimiento_real': 'Cumplimiento Real',
    'meta_sign': 'Meta s',
    'ejec_sign': 'Ejecución s',
    'llave': 'Llave',
    'dec_meta': 'Decimales_Meta',
    'dec_ejec': 'Decimales_Ejecucion',
    'fuente': 'Fuente',
    'clasificacion': 'Clasificación',
    'subproceso': 'Subproceso',
    'linea': 'Linea',
    'objetivo': 'Objetivo',
    'meta_pdi': 'Meta_PDI',
    'factor': 'FACTOR',
    'caracteristica': 'CARACTERÍSTICA',
    'tipo_cierre': 'Tipo_Cierre',
    'proyeccion': 'Proyección'
}
# ----------------------------------------

# ---------- Helpers ----------
def safe_to_numeric(series):
    # Reemplaza coma decimal por punto si aparece en strings y convierte a float
    return pd.to_numeric(series.astype(str).str.replace(',','.'), errors='coerce')

def format_with_sign(value, sign, dec):
    # formatea número con separador de miles y decimales y añade signado inteligentemente
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    try:
        dec = int(dec) if not pd.isna(dec) else 0
    except:
        dec = 0
    try:
        num = float(value)
    except:
        return str(value)
    formatted = f"{num:,.{dec}f}"
    sign_str = "" if pd.isna(sign) else str(sign).strip()
    # lógica de posición del signo:
    if sign_str == "%":
        return f"{formatted} {sign_str}"
    if sign_str in ['≤','≥','<','>','=']:
        return f"{sign_str}{formatted}"
    # si el signo parece una unidad textual (ENT, HORAS, etc.) lo ponemos como sufijo
    if sign_str.isalpha():
        return f"{formatted} {sign_str}"
    # por defecto lo ponemos como sufijo (maneja casos como "ENT" o "%")
    return f"{formatted} {sign_str}" if sign_str else formatted

def pct_cumplimiento(ejec, meta):
    try:
        if pd.isna(ejec) or pd.isna(meta) or float(meta) == 0:
            return np.nan
        return float(ejec) / float(meta) * 100.0
    except:
        return np.nan

def add_page_number(canvas_obj, doc_obj):
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica', 8)
    page_str = f"Página {doc_obj.page}"
    canvas_obj.drawRightString(A4[0] - 36, 20, page_str)
    canvas_obj.restoreState()

# ---------- Leer Excel ----------
df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
df.columns = df.columns.str.strip()  # limpiar espacios

# ---------- Normalizaciones (numéricas y fecha) ----------
# Fecha
if COL['fecha'] in df.columns:
    df[COL['fecha']] = pd.to_datetime(df[COL['fecha']], errors='coerce')

# Meta y Ejecución a numérico (maneja coma decimal)
for coln in [COL['meta'], COL['ejecucion']]:
    if coln in df.columns:
        df[coln] = safe_to_numeric(df[coln])

# Decimales - aseguro que existan columnas de decimales
if COL['dec_meta'] not in df.columns:
    df[COL['dec_meta']] = 0
if COL['dec_ejec'] not in df.columns:
    df[COL['dec_ejec']] = 0
# forzar int donde sea posible
try:
    df[COL['dec_meta']] = df[COL['dec_meta']].fillna(0).astype(int)
except:
    df[COL['dec_meta']] = df[COL['dec_meta']].apply(lambda x: int(x) if pd.notna(x) and str(x).isdigit() else 0)

try:
    df[COL['dec_ejec']] = df[COL['dec_ejec']].fillna(0).astype(int)
except:
    df[COL['dec_ejec']] = df[COL['dec_ejec']].apply(lambda x: int(x) if pd.notna(x) and str(x).isdigit() else 0)

# ---------- Calcular % cumplimiento (columna nueva Pct_Cumplimiento) ----------
# Si la columna 'Cumplimiento' existe y parece ratio (~1.x), ignoro y calculo con Ejecución/Meta para consistencia.
df['Pct_Cumplimiento'] = df.apply(lambda r: pct_cumplimiento(r.get(COL['ejecucion']), r.get(COL['meta'])), axis=1)

# ---------- Preparar PDF ----------
doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4,
                        rightMargin=36,leftMargin=36,
                        topMargin=72,bottomMargin=36)
styles = getSampleStyleSheet()
h1 = styles['Heading1']
h2 = styles['Heading2']
h3 = styles['Heading3']
normal = styles['Normal']
small = ParagraphStyle('small', parent=styles['Normal'], fontSize=8)

story = []

# Portada
story.append(Paragraph("Informe Ejecutivo de Indicadores - Consolidado", h1))
story.append(Spacer(1, 6))
story.append(Paragraph(f"Origen: {INPUT_FILE} (Hoja: {SHEET_NAME})", normal))
story.append(Spacer(1, 6))
story.append(Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal))
story.append(Spacer(1, 12))
if LOGO_PATH:
    try:
        story.append(Image(LOGO_PATH, width=2*inch, height=2*inch))
        story.append(Spacer(1, 12))
    except Exception as e:
        story.append(Paragraph(f"(No se pudo cargar logo: {e})", small))
story.append(PageBreak())

# ---------- Iterar: Linea -> Objetivo -> Meta_PDI ----------
group_linea = df.groupby(COL['linea'], sort=False)
for linea_name, df_linea in group_linea:
    story.append(Paragraph(f"Línea Estratégica: <b>{linea_name}</b>", h1))
    story.append(Spacer(1, 8))

    group_obj = df_linea.groupby(COL['objetivo'], sort=False)
    for obj_name, df_obj in group_obj:
        story.append(Paragraph(f"Objetivo Estratégico: <b>{obj_name}</b>", h2))
        story.append(Spacer(1, 6))

        group_meta = df_obj.groupby(COL['meta_pdi'], sort=False)
        for meta_name, df_meta in group_meta:
            story.append(Paragraph(f"Meta Estratégica: <b>{meta_name}</b>", h3))
            story.append(Spacer(1, 6))

            # Obtener último registro por indicador (última Fecha preferida)
            df_meta_local = df_meta.copy()
            if COL['fecha'] in df_meta_local.columns and df_meta_local[COL['fecha']].notna().any():
                df_meta_local = df_meta_local.sort_values(COL['fecha'])
                df_last = df_meta_local.groupby(COL['indicador'], as_index=False).last()
            else:
                # fallback: ordenar por Año y Periodo si Fecha no está
                sort_cols = []
                if COL['anio'] in df_meta_local.columns:
                    sort_cols.append(COL['anio'])
                if COL['periodo'] in df_meta_local.columns:
                    sort_cols.append(COL['periodo'])
                if sort_cols:
                    df_meta_local = df_meta_local.sort_values(sort_cols)
                    df_last = df_meta_local.groupby(COL['indicador'], as_index=False).last()
                else:
                    df_last = df_meta_local.groupby(COL['indicador'], as_index=False).last()

            # Tabla ejecutiva: Indicador | Último Periodo | Meta | Ejecución | % Cumplimiento
            tabla_data = [["Indicador", "Último periodo", "Meta", "Ejecución", "% Cumplimiento"]]
            for _, row in df_last.iterrows():
                nombre = row.get(COL['indicador'], "")
                # periodo/fecha a mostrar
                if COL['fecha'] in row and pd.notna(row.get(COL['fecha'])):
                    periodo_str = pd.to_datetime(row.get(COL['fecha'])).strftime("%Y-%m-%d")
                else:
                    periodo_str = str(row.get(COL['periodo'])) if pd.notna(row.get(COL['periodo'])) else (str(row.get(COL['anio'])) if pd.notna(row.get(COL['anio'])) else "")

                meta_val = format_with_sign(row.get(COL['meta']), row.get(COL['meta_sign'], ""), row.get(COL['dec_meta'], 0))
                eje_val = format_with_sign(row.get(COL['ejecucion']), row.get(COL['ejec_sign'], ""), row.get(COL['dec_ejec'], 0))
                pct = row.get('Pct_Cumplimiento')
                pct_str = "" if pd.isna(pct) else f"{round(float(pct),2)}%"

                tabla_data.append([nombre, periodo_str, meta_val, eje_val, pct_str])

            colWidths = [240, 80, 80, 80, 80]
            t = Table(tabla_data, colWidths=colWidths, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2E6DA4")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (1,1), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('FONTSIZE', (0,1), (-1,-1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))

            # Gráficos: serie histórica por indicador (agregado según periodicidad)
            # Construir serie histórica agregada por indicador para esta Meta_PDI
            try:
                # determinar periodicidad predominante en este conjunto
                per = None
                if COL['periodicidad'] in df_meta.columns:
                    # modo (valor más frecuente)
                    per = df_meta[COL['periodicidad']].mode().iloc[0] if not df_meta[COL['periodicidad']].mode().empty else None

                # Para graficar calculamos Pct por Periodo (si no hay, usamos Fecha)
                if str(per).strip().lower().startswith('anual') or per == 'Anual':
                    # agrupar por Año
                    if COL['anio'] in df_meta.columns:
                        hist = df_meta.groupby(COL['anio'], as_index=False).agg({'Pct_Cumplimiento':'mean'}).sort_values(COL['anio'])
                        x = hist[COL['anio']].astype(str).tolist()
                        y = hist['Pct_Cumplimiento'].tolist()
                    else:
                        # fallback usar fecha (por año)
                        df_meta_temp = df_meta.copy()
                        df_meta_temp['__anio'] = pd.to_datetime(df_meta_temp[COL['fecha']], errors='coerce').dt.year
                        hist = df_meta_temp.groupby('__anio', as_index=False).agg({'Pct_Cumplimiento':'mean'}).sort_values('__anio')
                        x = hist['__anio'].astype(str).tolist()
                        y = hist['Pct_Cumplimiento'].tolist()
                elif str(per).strip().lower().startswith('semestral') or per == 'Semestral':
                    # agrupar por Periodo (columna Periodo que viene tipo "2022-1")
                    if COL['periodo'] in df_meta.columns and df_meta[COL['periodo']].notna().any():
                        # ordenar por fecha si existe, sino por nombre de periodo
                        if COL['fecha'] in df_meta.columns and df_meta[COL['fecha']].notna().any():
                            df_meta_sorted = df_meta.sort_values(COL['fecha'])
                        else:
                            df_meta_sorted = df_meta.sort_values(COL['periodo'])
                        hist = df_meta_sorted.groupby(COL['periodo'], as_index=False).agg({'Pct_Cumplimiento':'mean'})
                        x = hist[COL['periodo']].astype(str).tolist()
                        y = hist['Pct_Cumplimiento'].tolist()
                    else:
                        # fallback: usar Año-Semestre combinados
                        df_meta_temp = df_meta.copy()
                        df_meta_temp['__periodo'] = df_meta_temp[COL['anio']].astype(str) + "-" + df_meta_temp[COL['semestre']].astype(str)
                        hist = df_meta_temp.groupby('__periodo', as_index=False).agg({'Pct_Cumplimiento':'mean'}).sort_values('__periodo')
                        x = hist['__periodo'].astype(str).tolist()
                        y = hist['Pct_Cumplimiento'].tolist()
                else:
                    # periodicidad desconocida: usar Fecha (por yyyy-mm)
                    if COL['fecha'] in df_meta.columns and df_meta[COL['fecha']].notna().any():
                        df_meta_temp = df_meta.copy()
                        df_meta_temp['__ym'] = pd.to_datetime(df_meta_temp[COL['fecha']], errors='coerce').dt.to_period('M').astype(str)
                        hist = df_meta_temp.groupby('__ym', as_index=False).agg({'Pct_Cumplimiento':'mean'}).sort_values('__ym')
                        x = hist['__ym'].astype(str).tolist()
                        y = hist['Pct_Cumplimiento'].tolist()
                    else:
                        x = []
                        y = []

                if len(x) > 0 and any([ (val is not None and not (isinstance(val, float) and np.isnan(val))) for val in y ]):
                    fig, ax = plt.subplots(figsize=(7, 2.2))
                    ax.bar(range(len(x)), y)
                    ax.axhline(100, color='red', linestyle='--', linewidth=0.8)
                    ax.set_ylabel("% Cumplimiento")
                    ax.set_xticks(range(len(x)))
                    ax.set_xticklabels(x, rotation=45, ha="right", fontsize=8)
                    plt.tight_layout()

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                    plt.close(fig)
                    buf.seek(0)
                    img = Image(buf, width=6.5*inch, height=2.2*inch)
                    story.append(img)
                    story.append(Spacer(1, 12))
                else:
                    story.append(Paragraph("No hay datos históricos suficientes para graficar.", small))
                    story.append(Spacer(1, 8))
            except Exception as e:
                story.append(Paragraph(f"Error creando gráfico: {e}", small))
                story.append(Spacer(1, 8))

            # separar metas con un pequeño salto
            story.append(Spacer(1, 6))

        # después de cada objetivo hacemos salto de página para que quede ordenado
        story.append(PageBreak())

# ---------- Generar PDF ----------
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print("PDF generado:", OUTPUT_PDF)
