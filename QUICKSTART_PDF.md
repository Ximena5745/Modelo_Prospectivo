# 🚀 Quick Start - Generador de PDF Consolidado

## ⚡ Inicio Rápido (3 Pasos)

### 1️⃣ Verificar Archivos

Asegúrate de tener estos archivos en tu proyecto:

```
Modelo_Prospectivo/
├── generar_pdf_consolidado.py  ✅ (Generador principal)
├── Data/
│   ├── Dataset_Unificado.xlsx          ✅ (Históricos)
│   └── Proyecciones_Multimodelo.xlsx   ✅ (Proyecciones)
└── Wallpaper-POLI.jpg                   ⚠️  (Opcional - Logo)
```

### 2️⃣ Ejecutar el Generador

**Opción A - Doble clic (Windows):**
```
Ejecutar_pdf.bat
```

**Opción B - Terminal:**
```bash
python generar_pdf_consolidado.py
```

**Opción C - Menú interactivo:**
```bash
python ejemplo_uso_pdf.py
```

### 3️⃣ Obtener el PDF

El archivo generado estará en:
```
Reporte_Consolidado_Indicadores_Modelos.pdf
```

---

## 📊 ¿Qué contiene el PDF?

```
📄 Un único PDF con TODA la información:

├── Portada general
│
├── 📂 LÍNEA: Expansión
│   ├── 📊 Indicador: Total Población
│   │   ├── 🧠 Modelo: Media Móvil
│   │   │   ├── Portada
│   │   │   ├── Ficha de métricas
│   │   │   ├── Gráfico histórico + proyecciones
│   │   │   └── Comparativo de escenarios
│   │   ├── 🧠 Modelo: ETS
│   │   └── ... (todos los modelos)
│   ├── 📊 Indicador: Estudiantes Pregrado
│   └── ... (todos los indicadores)
│
├── 📂 LÍNEA: Calidad
├── 📂 LÍNEA: Experiencia
├── 📂 LÍNEA: Sostenibilidad
├── 📂 LÍNEA: Transformación Organizacional
└── 📂 LÍNEA: Educación para la vida
```

---

## ⏱️ Tiempo Estimado

- **Generación completa**: 5-15 minutos
- **Páginas**: 300-600 (según cantidad de modelos)
- **Tamaño**: 20-50 MB

---

## 🔧 Solución Rápida de Problemas

### ❌ "No se encontró el archivo..."

```bash
# Verificar que existan los archivos
python -c "from pathlib import Path; print('Históricos:', (Path('Data')/'Dataset_Unificado.xlsx').exists()); print('Proyecciones:', (Path('Data')/'Proyecciones_Multimodelo.xlsx').exists())"
```

### ❌ "ModuleNotFoundError: No module named 'reportlab'"

```bash
# Instalar dependencias
pip install -r requirements.txt
```

### ❌ "Error al generar gráficos"

```bash
# Instalar/actualizar kaleido (motor de Plotly)
pip install -U kaleido plotly
```

---

## 🎯 Ejemplos de Uso Rápido

### Generar PDF completo (default)

```bash
python generar_pdf_consolidado.py
```

### Ver solo estadísticas (sin generar PDF)

```bash
python ejemplo_uso_pdf.py 5
```

### Generar PDF de una sola línea estratégica

```bash
python ejemplo_uso_pdf.py 4 Expansión
```

### Menú interactivo

```bash
python ejemplo_uso_pdf.py
```

---

## 📖 Documentación Completa

Para más detalles, consulta:
- [README_PDF_CONSOLIDADO.md](README_PDF_CONSOLIDADO.md) - Documentación completa
- [ejemplo_uso_pdf.py](ejemplo_uso_pdf.py) - Ejemplos de código

---

## 💡 Tips

✅ **Primera vez**: Ejecuta `python ejemplo_uso_pdf.py 5` para ver estadísticas antes de generar

✅ **Prueba rápida**: Usa la opción 4 para generar PDF de una sola línea

✅ **Producción completa**: Usa `python generar_pdf_consolidado.py` para el PDF completo

---

## 📞 ¿Necesitas Ayuda?

1. Revisa los mensajes de consola durante la generación
2. Consulta el [README completo](README_PDF_CONSOLIDADO.md)
3. Verifica que todos los archivos de datos estén presentes

---

**¡Listo! 🎉** Ya puedes generar tu reporte consolidado de indicadores.
