import pandas as pd

# Ruta del archivo
file = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\Data\Resultados Consolidados.xlsx"

# Ruta de salida
output_file = r"C:\Users\ximen\OneDrive\Imágenes\Proyectos\Indicadores\Prospectiva\Data\Dataset_Unificado.xlsx"


# Cargar hojas
base = pd.read_excel(file, sheet_name="Base_Indicadores")
sem = pd.read_excel(file, sheet_name="Consolidado_Semestral")
cierres = pd.read_excel(file, sheet_name="Consolidado_Cierres")



# ======================
# 2. Pivotear metas y ejecuciones por separado
# ======================
meta = sem.pivot_table(
    index=["Id","Indicador","Año"],
    columns="Semestre",
    values="Meta",
    aggfunc="first"
).reset_index().rename(columns={1:"Meta_Sem1", 2:"Meta_Sem2"})

ejec = sem.pivot_table(
    index=["Id","Indicador","Año"],
    columns="Semestre",
    values="Ejecución",
    aggfunc="first"
).reset_index().rename(columns={1:"Ejec_Sem1", 2:"Ejec_Sem2"})

sem_pivot = meta.merge(ejec, on=["Id","Indicador","Año"], how="outer")

# ======================
# 3. Reglas de cierre esperadas
# ======================
def calcular_cierre(row, tipo):
    s1, s2 = row["Ejec_Sem1"], row["Ejec_Sem2"]
    if tipo == "Acumulativo":
        return (s1 or 0) + (s2 or 0)
    elif tipo == "Promedio":
        return ( (s1 or 0) + (s2 or 0) ) / (2 if pd.notna(s2) else 1)
    elif tipo == "Último valor":
        return s2 if pd.notna(s2) else s1
    else:
        return None

# Añadir Tipo_Cierre desde Base_Indicadores
sem_pivot = sem_pivot.merge(base[["Id","Tipo_Cierre"]], on="Id", how="left")
sem_pivot["Cierre_Calculado"] = sem_pivot.apply(lambda r: calcular_cierre(r, r["Tipo_Cierre"]), axis=1)

# ======================
# 4. Comparar con Consolidado_Cierres
# ======================
cierres_sel = cierres[["Id","Año","Ejecución"]].rename(columns={"Ejecución":"Cierre_Real"})
val = sem_pivot.merge(cierres_sel, on=["Id","Año"], how="left")

# Validación de consistencia
val["Diferencia_%"] = (val["Cierre_Real"] - val["Cierre_Calculado"]) / val["Cierre_Real"] * 100
val["Consistencia"] = val["Diferencia_%"].abs().apply(lambda x: "OK" if x < 1 else "Revisar")

# ======================
# 5. Guardar resultados
# ======================
val.to_excel("Validacion_Cierres_Correcta.xlsx", index=False)




# =====================
# 2. Asegurar columna Id
# =====================
id_col = "Id"

# =====================
# 3. Agregar campo Fuente
# =====================
sem["Fuente"] = "Semestral"
cierres["Fuente"] = "Cierre"

# =====================
# 4. Unificar datasets sin perder columnas originales
# =====================
unificado = pd.concat([sem, cierres], ignore_index=True)

# =====================
# 5. Enriquecer con base de indicadores
#    ⚠️ Nos quedamos SOLO con la versión de base para campos descriptivos
# =====================
unificado = unificado.merge(
    base,
    on=id_col,
    how="left",
    suffixes=("", "_base")  # Evita sobrescribir y mantiene los de base
)

# =====================
# 6. Eliminar duplicados innecesarios
# =====================
# Columnas que deben venir SOLO de base
cols_base = ["Indicador", "Clasificación", "Subproceso", "Periodicidad", "Sentido",
             "Linea", "Objetivo", "Meta_PDI", "FACTOR", "CARACTERÍSTICA",
             "Tipo_Cierre", "Proyección"]

# Si existen versiones duplicadas en el dataset, nos quedamos con las de base
for col in cols_base:
    col_base = col + "_base"
    if col_base in unificado.columns:
        unificado[col] = unificado[col_base]  # sobreescribimos con los de base
        unificado.drop(columns=[col_base], inplace=True, errors="ignore")

# =====================
# 7. Unificación de columnas duplicadas de decimales
# =====================
if "Decimales_Meta" in unificado.columns and "Decimales" in unificado.columns:
    unificado["Decimales"] = unificado["Decimales"].fillna(unificado["Decimales_Meta"])
    unificado.drop(columns=["Decimales_Meta"], inplace=True, errors="ignore")

if "DecimalesEje" in unificado.columns and "Decimales_Ejecucion" in unificado.columns:
    unificado["Decimales_Ejecucion"] = unificado["Decimales_Ejecucion"].fillna(unificado["DecimalesEje"])
    unificado.drop(columns=["DecimalesEje"], inplace=True, errors="ignore")

# =====================
# 8. Guardar en Excel
# =====================
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    unificado.to_excel(writer, sheet_name="Unificado", index=False)
    base.to_excel(writer, sheet_name="Base_Indicadores", index=False)
    sem.to_excel(writer, sheet_name="Semestral_Original", index=False)
    cierres.to_excel(writer, sheet_name="Cierres_Original", index=False)

print(f"✅ Archivo generado: {output_file}")