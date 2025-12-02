"""
Ejemplo de uso del Generador de PDF Consolidado
================================================

Este script muestra diferentes formas de usar el generador de PDF.
"""

from generar_pdf_consolidado import (
    cargar_datos,
    GeneradorPDFConsolidado,
    main
)
from pathlib import Path

# ============================================================
# OPCIÓN 1: Ejecución Simple (recomendada)
# ============================================================
def opcion_1_simple():
    """
    Forma más simple: ejecutar la función principal que hace todo.
    """
    print("🚀 OPCIÓN 1: Ejecución simple")
    print("-" * 60)
    main()


# ============================================================
# OPCIÓN 2: Ejecución con Control de Datos
# ============================================================
def opcion_2_con_control():
    """
    Control sobre los datos cargados antes de generar el PDF.
    Útil para hacer validaciones o filtrados personalizados.
    """
    print("\n🚀 OPCIÓN 2: Ejecución con control de datos")
    print("-" * 60)

    # Cargar datos
    df_hist, df_proj = cargar_datos()

    # Aquí puedes hacer validaciones o filtrados
    print(f"\n📊 Datos cargados:")
    print(f"   - Registros históricos: {len(df_hist)}")
    print(f"   - Registros de proyección: {len(df_proj)}")
    print(f"   - Indicadores únicos: {df_hist['Indicador'].nunique()}")
    print(f"   - Modelos únicos: {df_proj['Modelo'].nunique()}")

    # Ejemplo: Filtrar solo una línea estratégica
    # df_hist = df_hist[df_hist['Linea'] == 'Expansión']
    # df_proj = df_proj[df_proj['Indicador'].isin(df_hist['Indicador'].unique())]

    # Crear generador y producir PDF
    generador = GeneradorPDFConsolidado(df_hist, df_proj)
    generador.generar_pdf()


# ============================================================
# OPCIÓN 3: Generar PDF Solo para Indicadores Específicos
# ============================================================
def opcion_3_indicadores_especificos():
    """
    Genera PDF solo para un conjunto específico de indicadores.
    """
    print("\n🚀 OPCIÓN 3: PDF de indicadores específicos")
    print("-" * 60)

    # Cargar datos
    df_hist, df_proj = cargar_datos()

    # Definir indicadores de interés
    indicadores_interes = [
        "Total Población",
        "Estudiantes Pregrado",
        "Brand equity"
    ]

    print(f"\n🎯 Filtrando indicadores:")
    for ind in indicadores_interes:
        print(f"   - {ind}")

    # Filtrar datos
    df_hist_filtrado = df_hist[df_hist['Indicador'].isin(indicadores_interes)]
    df_proj_filtrado = df_proj[df_proj['Indicador'].isin(indicadores_interes)]

    print(f"\n📊 Datos filtrados:")
    print(f"   - Registros históricos: {len(df_hist_filtrado)}")
    print(f"   - Registros de proyección: {len(df_proj_filtrado)}")

    # Generar PDF
    generador = GeneradorPDFConsolidado(df_hist_filtrado, df_proj_filtrado)
    generador.generar_pdf()


# ============================================================
# OPCIÓN 4: Generar PDF por Línea Estratégica
# ============================================================
def opcion_4_por_linea(linea_estrategica="Expansión"):
    """
    Genera PDF solo para una línea estratégica específica.

    Args:
        linea_estrategica: Nombre de la línea (ej: "Expansión", "Calidad")
    """
    print(f"\n🚀 OPCIÓN 4: PDF solo para {linea_estrategica}")
    print("-" * 60)

    # Cargar datos
    df_hist, df_proj = cargar_datos()

    # Filtrar por línea estratégica
    df_hist_linea = df_hist[df_hist['Linea'] == linea_estrategica]

    # Obtener indicadores de esta línea
    indicadores_linea = df_hist_linea['Indicador'].unique()

    # Filtrar proyecciones
    df_proj_linea = df_proj[df_proj['Indicador'].isin(indicadores_linea)]

    print(f"\n📊 Línea: {linea_estrategica}")
    print(f"   - Indicadores: {len(indicadores_linea)}")
    print(f"   - Registros históricos: {len(df_hist_linea)}")
    print(f"   - Registros de proyección: {len(df_proj_linea)}")

    # Generar PDF
    generador = GeneradorPDFConsolidado(df_hist_linea, df_proj_linea)
    generador.generar_pdf()


# ============================================================
# OPCIÓN 5: Estadísticas y Validación sin Generar PDF
# ============================================================
def opcion_5_solo_estadisticas():
    """
    Muestra estadísticas de los datos sin generar el PDF.
    Útil para validación antes de la generación completa.
    """
    print("\n🚀 OPCIÓN 5: Solo estadísticas (sin generar PDF)")
    print("-" * 60)

    # Cargar datos
    df_hist, df_proj = cargar_datos()

    print("\n📊 ESTADÍSTICAS GENERALES")
    print("=" * 60)

    # Históricos
    print("\n📈 Datos Históricos:")
    print(f"   - Total registros: {len(df_hist)}")
    print(f"   - Indicadores únicos: {df_hist['Indicador'].nunique()}")
    if 'Linea' in df_hist.columns:
        print(f"   - Líneas estratégicas: {df_hist['Linea'].nunique()}")
        print("\n   📂 Indicadores por línea:")
        for linea in sorted(df_hist['Linea'].unique()):
            count = df_hist[df_hist['Linea'] == linea]['Indicador'].nunique()
            print(f"      • {linea}: {count} indicadores")

    # Proyecciones
    print("\n📊 Proyecciones:")
    print(f"   - Total registros: {len(df_proj)}")
    print(f"   - Indicadores con proyecciones: {df_proj['Indicador'].nunique()}")
    print(f"   - Modelos únicos: {df_proj['Modelo'].nunique()}")

    if 'Modelo' in df_proj.columns:
        print("\n   🧠 Distribución de modelos:")
        modelos_count = df_proj.groupby('Modelo')['Indicador'].nunique().sort_values(ascending=False)
        for modelo, count in modelos_count.items():
            print(f"      • {modelo}: {count} indicadores")

    if 'Escenario' in df_proj.columns:
        print("\n   🌍 Escenarios disponibles:")
        escenarios = df_proj['Escenario'].unique()
        for escenario in sorted(escenarios):
            print(f"      • {escenario}")

    # Validaciones
    print("\n🔍 VALIDACIONES")
    print("=" * 60)

    # Indicadores sin proyecciones
    indicadores_hist = set(df_hist['Indicador'].unique())
    indicadores_proj = set(df_proj['Indicador'].unique())
    sin_proyeccion = indicadores_hist - indicadores_proj

    if sin_proyeccion:
        print(f"\n⚠️ Indicadores SIN proyecciones ({len(sin_proyeccion)}):")
        for ind in sorted(sin_proyeccion):
            print(f"   - {ind}")
    else:
        print("\n✅ Todos los indicadores tienen proyecciones")

    # Indicadores solo en proyecciones
    solo_en_proj = indicadores_proj - indicadores_hist
    if solo_en_proj:
        print(f"\n⚠️ Indicadores SOLO en proyecciones ({len(solo_en_proj)}):")
        for ind in sorted(solo_en_proj):
            print(f"   - {ind}")

    print("\n" + "=" * 60)
    print("✅ Análisis completado")


# ============================================================
# MENÚ INTERACTIVO
# ============================================================
def menu_interactivo():
    """
    Muestra un menú para elegir la opción de ejecución.
    """
    print("\n" + "=" * 60)
    print("  GENERADOR DE PDF CONSOLIDADO - MENÚ DE OPCIONES")
    print("  Politécnico Grancolombiano")
    print("=" * 60)

    opciones = {
        '1': ('Generación completa (todos los indicadores y modelos)', opcion_1_simple),
        '2': ('Generación con control de datos', opcion_2_con_control),
        '3': ('Solo indicadores específicos', opcion_3_indicadores_especificos),
        '4': ('Solo una línea estratégica', lambda: opcion_4_por_linea("Expansión")),
        '5': ('Mostrar solo estadísticas (sin generar PDF)', opcion_5_solo_estadisticas),
        '0': ('Salir', None)
    }

    print("\n📋 Opciones disponibles:")
    for key, (descripcion, _) in opciones.items():
        print(f"   [{key}] {descripcion}")

    print("\n" + "-" * 60)
    eleccion = input("Selecciona una opción [0-5]: ").strip()

    if eleccion in opciones:
        descripcion, funcion = opciones[eleccion]
        if funcion:
            print(f"\n✅ Ejecutando: {descripcion}")
            print("=" * 60)
            funcion()
        else:
            print("\n👋 Saliendo...")
    else:
        print("\n❌ Opción no válida")


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    import sys

    # Si se pasa un argumento numérico, ejecutar esa opción directamente
    if len(sys.argv) > 1:
        opcion = sys.argv[1]
        if opcion == '1':
            opcion_1_simple()
        elif opcion == '2':
            opcion_2_con_control()
        elif opcion == '3':
            opcion_3_indicadores_especificos()
        elif opcion == '4':
            # Permitir pasar la línea como segundo argumento
            linea = sys.argv[2] if len(sys.argv) > 2 else "Expansión"
            opcion_4_por_linea(linea)
        elif opcion == '5':
            opcion_5_solo_estadisticas()
        else:
            print("❌ Opción no válida")
            print("Uso: python ejemplo_uso_pdf.py [1-5]")
    else:
        # Sin argumentos: mostrar menú interactivo
        menu_interactivo()
