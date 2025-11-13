#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remover la barra de desplazamiento
content = content.replace(
    'rangeslider=dict(visible=True, thickness=0.05),\n        ',
    ''
)

# Cambiar fixedrange a True para deshabilitar zoom/pan
content = content.replace(
    'fixedrange=False,',
    'fixedrange=True,'
)

# Cambiar el rango para mostrar todos los datos disponibles
content = content.replace(
    'range=["2022-03-15", df_proj_sel[\'Fecha\'].max().strftime(\'%Y-%m-%d\') if not df_proj_sel.empty else "2030-12-31"]',
    'range=[df_hist_trace[\'Fecha\'].min().strftime(\'%Y-%m-%d\') if not df_hist_trace.empty else "2017-01-01", df_proj_sel[\'Fecha\'].max().strftime(\'%Y-%m-%d\') if not df_proj_sel.empty else "2030-12-31"]'
)

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Barra de desplazamiento removida. Gráfica mostrará todos los datos disponibles.')
