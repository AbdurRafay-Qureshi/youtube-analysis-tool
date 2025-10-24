# ui/__init__.py
from .styles import css, plotly_layout
from .components import kpi, chart_card, end_card, section, info_card
from .sidebar import render_platform_selector

# Create alias for backward compatibility
render_sidebar = render_platform_selector

__all__ = [
    'css',
    'plotly_layout', 
    'kpi',
    'chart_card',
    'end_card',
    'section',
    'info_card',
    'render_platform_selector',
    'render_sidebar'  # Backward compatibility
]
