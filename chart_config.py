"""
Chart configuration for the Modelo Prospectivo application.
This file contains the chart layout configuration to be imported in app_streamlit.py
"""

def get_chart_layout(indicador_sel, tickvals=None, ticktext=None):
    """
    Returns the layout configuration for the main chart.
    
    Args:
        indicador_sel (str): The name of the indicator to display
        tickvals (list, optional): List of tick values for x-axis
        ticktext (list, optional): List of tick labels for x-axis
        
    Returns:
        dict: Layout configuration dictionary
    """
    layout = {
        'template': "plotly_white",
        'plot_bgcolor': '#ffffff',
        'paper_bgcolor': '#ffffff',
        'height': 650,
        'font': {
            'family': "Poppins",
            'size': 14,
            'color': "#1e293b"
        },
        'title': {
            'text': f"{indicador_sel} - Evolución Histórica y Proyección",
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 20,
                'color': "#0d47a1",
                'family': "Poppins"
            }
        },
        'hovermode': 'x unified',
        'legend': {
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.02,
            'xanchor': "center",
            'x': 0.5,
            'bgcolor': "rgba(255,255,255,0.95)",
            'bordercolor': "#cbd5e0",
            'borderwidth': 1,
            'font': {
                'size': 14,
                'family': "Poppins",
                'color': "#1e293b"
            },
            'itemsizing': 'constant'
        },
        'margin': {
            'l': 80,
            'r': 60,
            't': 120,
            'b': 100
        },
        'xaxis': {
            'title': {
                'text': "<b>Periodo</b>",
                'font': {
                    'size': 16,
                    'weight': 600,
                    'family': "Poppins",
                    'color': "#1e293b"
                },
                'standoff': 15
            },
            'showgrid': True,
            'gridcolor': 'rgba(0,0,0,0.05)',
            'gridwidth': 1,
            'tickfont': {
                'size': 12,
                'family': "Poppins",
                'color': "#1e293b"
            },
            'linecolor': '#cbd5e0',
            'linewidth': 2,
            'mirror': True,
            'showline': True,
            'automargin': True,
            'tickangle': 0
        },
        'yaxis': {
            'title': {
                'text': f"<b>{indicador_sel}</b>",
                'font': {
                    'size': 16,
                    'weight': 600,
                    'family': "Poppins",
                    'color': "#1e293b"
                },
                'standoff': 15
            },
            'showgrid': True,
            'gridcolor': 'rgba(0,0,0,0.05)',
            'gridwidth': 1,
            'tickformat': ",.0f",
            'tickfont': {
                'size': 12,
                'family': "Poppins",
                'color': "#1e293b"
            },
            'linecolor': '#cbd5e0',
            'linewidth': 2,
            'mirror': True,
            'showline': True,
            'zeroline': False,
            'automargin': True
        },
        'hoverlabel': {
            'bgcolor': "white",
            'font_size': 14,
            'font_family': "Poppins",
            'bordercolor': "#cbd5e0",
            'namelength': -1
        }
    }
    
    # Add custom tick values if provided
    if tickvals and ticktext:
        layout['xaxis']['tickvals'] = tickvals
        layout['xaxis']['ticktext'] = ticktext
    
    return layout
