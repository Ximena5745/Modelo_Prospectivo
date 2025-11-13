#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar fixedrange=True por fixedrange=False para permitir zoom/pan
content = content.replace(
    'fixedrange=True,',
    'fixedrange=False,'
)

# Agregar rangeslider después de fixedrange=False
content = content.replace(
    'fixedrange=False,\n        # Ajustar márgenes para etiquetas rotadas',
    'fixedrange=False,\n        rangeslider=dict(visible=True, thickness=0.05),\n        # Ajustar márgenes para etiquetas rotadas'
)

# Cambiar el rango inicial para mostrar desde 2022-S1
# Buscar la línea del range y reemplazarla para que el rango visible sea desde 2022-S1
content = content.replace(
    'range=[df_hist_trace[\'Fecha\'].min().strftime(\'%Y-%m-%d\') if not df_hist_trace.empty else "2017-01-01", df_proj_sel[\'Fecha\'].max().strftime(\'%Y-%m-%d\') if not df_proj_sel.empty else "2030-12-31"]',
    'range=["2022-03-15", df_proj_sel[\'Fecha\'].max().strftime(\'%Y-%m-%d\') if not df_proj_sel.empty else "2030-12-31"]'
)

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Barra de desplazamiento agregada exitosamente')
