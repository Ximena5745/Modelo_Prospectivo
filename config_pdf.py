"""
Archivo de Configuración para el Generador de PDF Consolidado
==============================================================

Este archivo centraliza todas las configuraciones personalizables
del generador de PDF. Modifica los valores aquí para ajustar el
comportamiento sin tocar el código principal.
"""

from pathlib import Path

# ==============================
# RUTAS DE ARCHIVOS
# ==============================

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent

# Archivos de datos de entrada
RUTA_DATASET = BASE_DIR / "Data" / "Dataset_Unificado.xlsx"
RUTA_PROYECCIONES = BASE_DIR / "Data" / "Proyecciones_Multimodelo.xlsx"

# Recursos visuales
LOGO_PATH = BASE_DIR / "Wallpaper-POLI.jpg"

# Archivo de salida
OUTPUT_PDF = BASE_DIR / "Reporte_Consolidado_Indicadores_Modelos.pdf"

# Opción: usar nombre de archivo con fecha
# OUTPUT_PDF = BASE_DIR / f"Reporte_Consolidado_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"


# ==============================
# CONFIGURACIÓN DE AÑOS
# ==============================

# Año base para cálculos históricos
BASE_YEAR = 2025

# Años de comparación en las proyecciones
COMP_YEAR_1 = 2026  # Primer año de proyección a mostrar
COMP_YEAR_2 = 2030  # Último año de proyección a mostrar

# Años para indicadores bianuales (Great Place to Work, Índice de Inclusión)
BIANUAL_COMP_YEAR_1 = 2027
BIANUAL_COMP_YEAR_2 = 2029


# ==============================
# INDICADORES BIANUALES
# ==============================

# IDs de indicadores que se evalúan cada dos años
BIANUAL_IDS = {202, 361}

# Nombres de indicadores bianuales
BIANUAL_NAMES = {
    "Great Place to Work",
    "Índice de Inclusión"
}


# ==============================
# ORDEN PERSONALIZADO DE INDICADORES
# ==============================

# Define el orden de presentación de indicadores por línea estratégica
# Si un indicador no está en la lista, se agregará al final alfabéticamente
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


# ==============================
# PALETA DE COLORES
# ==============================

# Colores por línea estratégica (formato hexadecimal)
COLORES_LINEAS = {
    "Expansión": "#2c5f8d",
    "Transformación_Organizacional": "#1e3a5f",
    "Calidad": "#4a90c8",
    "Experiencia": "#5ca3d6",
    "Sostenibilidad": "#2ecc71",
    "Educación_para_toda_la_vida": "#3498db"
}

# Colores por tipo de escenario
COLORES_ESCENARIOS = {
    'Optimista': '#2ecc71',      # Verde
    'Realista': '#2c5f8d',       # Azul institucional
    'Base': '#2c5f8d',           # Azul institucional (alias)
    'Pesimista': '#e74c3c',      # Rojo
    'Histórico': '#D4A017',      # Dorado
    'Histórico Semestral': '#D4A017',
    'Histórico Anual': '#D4A017'
}

# Colores para tendencias
COLOR_TENDENCIA_POSITIVA = '#2ecc71'    # Verde
COLOR_TENDENCIA_NEGATIVA = '#e74c3c'    # Rojo
COLOR_TENDENCIA_ESTABLE = '#f1c40f'     # Amarillo


# ==============================
# NOMBRES DE MODELOS
# ==============================

# Mapeo de nombres técnicos a nombres amigables con iconos
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
# CONFIGURACIÓN DE GRÁFICOS
# ==============================

# Dimensiones de los gráficos (en píxeles)
GRAFICO_ANCHO = 800
GRAFICO_ALTO = 500

# Escala de resolución (1 = normal, 2 = alta, 3 = ultra alta)
GRAFICO_ESCALA = 2

# Altura del gráfico en el PDF (en pulgadas)
GRAFICO_ALTURA_PDF = 4.0
GRAFICO_ANCHO_PDF = 6.5


# ==============================
# CONFIGURACIÓN DE TIPOGRAFÍA
# ==============================

# Fuentes disponibles en ReportLab
# 'Helvetica', 'Helvetica-Bold', 'Times-Roman', 'Courier'
FUENTE_PRINCIPAL = 'Helvetica'
FUENTE_NEGRITA = 'Helvetica-Bold'

# Tamaños de fuente (en puntos)
TAMAÑO_TITULO_PORTADA = 24
TAMAÑO_TITULO_SECCION = 20
TAMAÑO_TITULO_INDICADOR = 16
TAMAÑO_TITULO_MODELO = 14
TAMAÑO_TEXTO_NORMAL = 10
TAMAÑO_TEXTO_TABLAS = 9
TAMAÑO_PIE_PAGINA = 8


# ==============================
# CONFIGURACIÓN DE LAYOUT
# ==============================

# Márgenes del documento (en centímetros)
MARGEN_SUPERIOR = 1.5
MARGEN_INFERIOR = 1.5
MARGEN_IZQUIERDO = 1.0
MARGEN_DERECHO = 1.0

# Espaciados (en pulgadas)
ESPACIO_ENTRE_SECCIONES = 0.5
ESPACIO_ENTRE_ELEMENTOS = 0.2
ESPACIO_GRANDE = 0.3


# ==============================
# INFORMACIÓN INSTITUCIONAL
# ==============================

# Datos para la portada
NOMBRE_INSTITUCION = "Politécnico Grancolombiano"
TITULO_REPORTE = "REPORTE CONSOLIDADO DE INDICADORES Y MODELOS"
SUBTITULO_REPORTE = "Plataforma Prospectiva de Indicadores Institucionales<br/>Análisis y Proyección 2026-2030"


# ==============================
# OPCIONES DE CONTENIDO
# ==============================

# Incluir/excluir secciones
INCLUIR_PORTADA_GENERAL = True
INCLUIR_PORTADAS_LINEA = True
INCLUIR_PORTADAS_INDICADOR = True
INCLUIR_FICHA_RESUMEN = True
INCLUIR_GRAFICOS = True
INCLUIR_FICHA_ESCENARIOS = True

# Agregar saltos de página
SALTO_PAGINA_ENTRE_MODELOS = True
SALTO_PAGINA_ENTRE_INDICADORES = False
SALTO_PAGINA_ENTRE_LINEAS = True

# Opciones de numeración
NUMERAR_PAGINAS = True
MOSTRAR_TOTAL_PAGINAS = True


# ==============================
# FILTROS OPCIONALES
# ==============================

# Dejar vacío para procesar todo, o especificar lista para filtrar
LINEAS_A_INCLUIR = []  # Ej: ["Expansión", "Calidad"]
INDICADORES_A_EXCLUIR = []  # Ej: ["Indicador obsoleto"]
MODELOS_A_INCLUIR = []  # Ej: ["Ensemble_Ponderado", "ETS"]


# ==============================
# CONFIGURACIÓN AVANZADA
# ==============================

# Mostrar mensajes de debug en consola
DEBUG_MODE = False

# Límite de memoria para gráficos (evitar crashes con muchos datos)
MAX_PUNTOS_GRAFICO = 1000

# Timeout para generación de gráficos individuales (segundos)
TIMEOUT_GRAFICO = 30

# Formato de fecha en portadas y fichas
FORMATO_FECHA_REPORTE = '%d de %B de %Y, %H:%M'
FORMATO_FECHA_CORTA = '%d/%m/%Y'


# ==============================
# VALIDACIÓN DE CONFIGURACIÓN
# ==============================

def validar_configuracion():
    """
    Valida que la configuración sea correcta antes de generar el PDF.

    Returns:
        tuple: (es_valida: bool, errores: list)
    """
    errores = []

    # Validar existencia de archivos
    if not RUTA_DATASET.exists():
        errores.append(f"❌ No se encontró: {RUTA_DATASET}")

    if not RUTA_PROYECCIONES.exists():
        errores.append(f"❌ No se encontró: {RUTA_PROYECCIONES}")

    if not LOGO_PATH.exists():
        print(f"⚠️ Advertencia: No se encontró el logo: {LOGO_PATH}")
        print("   El PDF se generará sin logo.")

    # Validar años
    if COMP_YEAR_1 >= COMP_YEAR_2:
        errores.append(f"❌ COMP_YEAR_1 ({COMP_YEAR_1}) debe ser menor que COMP_YEAR_2 ({COMP_YEAR_2})")

    if BASE_YEAR >= COMP_YEAR_1:
        errores.append(f"❌ BASE_YEAR ({BASE_YEAR}) debe ser menor que COMP_YEAR_1 ({COMP_YEAR_1})")

    # Validar colores
    for linea, color in COLORES_LINEAS.items():
        if not color.startswith('#') or len(color) != 7:
            errores.append(f"❌ Color inválido para {linea}: {color}")

    # Validar dimensiones
    if GRAFICO_ANCHO <= 0 or GRAFICO_ALTO <= 0:
        errores.append("❌ Las dimensiones del gráfico deben ser positivas")

    if GRAFICO_ESCALA < 1:
        errores.append("❌ La escala del gráfico debe ser >= 1")

    return (len(errores) == 0, errores)


# ==============================
# INFORMACIÓN DE CONFIGURACIÓN
# ==============================

def mostrar_configuracion():
    """Muestra un resumen de la configuración actual."""
    print("\n" + "=" * 70)
    print("  CONFIGURACIÓN DEL GENERADOR DE PDF")
    print("=" * 70)

    print("\n📁 Archivos:")
    print(f"   Históricos:    {RUTA_DATASET}")
    print(f"   Proyecciones:  {RUTA_PROYECCIONES}")
    print(f"   Logo:          {LOGO_PATH}")
    print(f"   Salida PDF:    {OUTPUT_PDF}")

    print("\n📅 Años de análisis:")
    print(f"   Base:          {BASE_YEAR}")
    print(f"   Comparación 1: {COMP_YEAR_1}")
    print(f"   Comparación 2: {COMP_YEAR_2}")

    print("\n🎨 Diseño:")
    print(f"   Gráficos:      {GRAFICO_ANCHO}x{GRAFICO_ALTO} px (escala {GRAFICO_ESCALA}x)")
    print(f"   Fuente:        {FUENTE_PRINCIPAL} / {FUENTE_NEGRITA}")
    print(f"   Título:        {TAMAÑO_TITULO_PORTADA} pt")

    print("\n📊 Contenido:")
    print(f"   Portada general:   {'✅' if INCLUIR_PORTADA_GENERAL else '❌'}")
    print(f"   Portadas línea:    {'✅' if INCLUIR_PORTADAS_LINEA else '❌'}")
    print(f"   Fichas resumen:    {'✅' if INCLUIR_FICHA_RESUMEN else '❌'}")
    print(f"   Gráficos:          {'✅' if INCLUIR_GRAFICOS else '❌'}")
    print(f"   Fichas escenarios: {'✅' if INCLUIR_FICHA_ESCENARIOS else '❌'}")

    if LINEAS_A_INCLUIR:
        print(f"\n🔍 Filtros activos:")
        print(f"   Líneas: {', '.join(LINEAS_A_INCLUIR)}")

    if INDICADORES_A_EXCLUIR:
        print(f"   Excluir: {len(INDICADORES_A_EXCLUIR)} indicadores")

    if MODELOS_A_INCLUIR:
        print(f"   Modelos: {', '.join(MODELOS_A_INCLUIR)}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Si se ejecuta directamente, mostrar configuración y validar
    mostrar_configuracion()

    print("\n🔍 Validando configuración...")
    es_valida, errores = validar_configuracion()

    if es_valida:
        print("\n✅ Configuración válida - Lista para generar PDF")
    else:
        print("\n❌ Errores encontrados en la configuración:")
        for error in errores:
            print(f"   {error}")
