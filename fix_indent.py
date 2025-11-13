#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar y reemplazar la línea problemática
for i, line in enumerate(lines):
    if 'text=f"<b>{indicador_sel.upper()}</b>",' in line:
        # Agregar la indentación correcta (12 espacios para alinearse con otros parámetros)
        lines[i] = '            text=f"<b>{indicador_sel.upper()}</b>",\n'
        break

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Indentación corregida exitosamente')
