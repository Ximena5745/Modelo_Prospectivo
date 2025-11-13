#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar el placeholder inválido
content = content.replace('{{ ... }}', 'text=f"<b>{indicador_sel.upper()}</b>",')

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Archivo corregido exitosamente')
