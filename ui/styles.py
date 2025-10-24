# ui/styles.py
from .theme import PALETTE

def css():
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* === BASE & FONT === */
    html, body, [class*="css"] {{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
    .stApp {{ background: {PALETTE['bg']}; }}
    .block-container {{ padding: 24px 36px !important; max-width: 1280px; }}

    /* === HEADER FIX (Removes white bar cutting off title) === */
    [data-testid="stHeader"] {{
        background-color: {PALETTE['bg']} !important;
        border-bottom: 1px solid {PALETTE['bg']} !important;
        box-shadow: none !important;
    }}
    /* Hide the hamburger menu button */
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    /* === REWRITTEN SIDEBAR === */
    [data-testid="stSidebar"] {{
        background-color: #1F2937 !important; /* Nice dark grey (gray-800) */
        border-right: 1px solid #374151 !important; /* (gray-700) */
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background-color: #1F2937 !important;
    }}
    
    /* General sidebar text */
    [data-testid="stSidebar"] [data-testid="stMarkdown"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] a {{
        color: #E5E7EB !important; /* Softer white (gray-200) */
    }}
    
    /* Dark-mode inputs for sidebar */
    [data-testid="stSidebar"] input {{
        background-color: #374151 !important; /* (gray-700) */
        color: #F3F4F6 !important; /* (gray-100) */
        border: 1px solid #4B5563 !important; /* (gray-600) */
        border-radius: 8px !important;
    }}
    [data-testid="stSidebar"] input::placeholder {{
        color: #9CA3AF !important; /* (gray-400) */
    }}
    
    /* Fix password "eye" icon */
    [data-testid="stSidebar"] .stPasswordInput button {{
        background-color: transparent !important;
        border: none !important;
    }}
    [data-testid="stSidebar"] .stPasswordInput button:hover {{
        background-color: #4B5563 !important; /* (gray-600) */
    }}
    [data-testid="stSidebar"] .stPasswordInput button svg {{
        fill: #9CA3AF !important; /* (gray-400) */
    }}
    
    /* Make sidebar buttons full-width */
    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
    }}

    /* Toggles (e.g., "Active Session") */
    [data-testid="stSidebar"] [data-testid="stToggle"] {{
        background-color: #374151; /* (gray-700) */
        border-radius: 10px;
        padding: 12px 16px;
    }}
    [data-testid="stSidebar"] [data-testid="stToggle"] label {{
        color: #F3F4F6 !important;
        font-weight: 600;
    }}
    
    /* === MAIN CONTENT STYLES (Unchanged) === */
    .page-title {{ font-weight: 700; font-size: 28px; color: {PALETTE['text']}; margin: 4px 0 6px; }}
    .page-subtitle {{ font-size: 14px; color: {PALETTE['muted']}; margin-bottom: 18px; }}

    .card {{
        background: {PALETTE['card']};
        border: 1px solid {PALETTE['border']};
        border-radius: 12px;
        box-shadow: 0 1px 2px rgba(16,24,40,.04);
        padding: 16px;
    }}
    .kpi .label {{ text-transform: uppercase; letter-spacing: .4px; color: {PALETTE['muted']}; font-size: 12px; font-weight: 600; }}
    .kpi .value {{ color: {PALETTE['text']}; font-weight: 700; font-size: 28px; line-height: 1.1; margin-top: 6px; }}
    .kpi .delta {{ font-size: 12px; font-weight: 600; margin-top: 8px; }}
    .delta.pos {{ color: {PALETTE['success']}; }}
    .delta.neg {{ color: {PALETTE['danger']}; }}

    .chart-title {{ font-size: 14px; color: {PALETTE['text']}; font-weight: 700; margin-bottom: 8px; }}

    .stTabs [data-baseweb="tab-list"] {{
        background: {PALETTE['card']}; border: 1px solid {PALETTE['border']};
        border-radius: 10px; padding: 6px; gap: 6px;
    }}
    .stTabs [data-baseweb="tab"] {{ color: {PALETTE['muted']}; border-radius: 8px; padding: 10px 16px; font-weight: 600; }}
    .stTabs [aria-selected="true"] {{ background: {PALETTE['primary']}; color: #fff !important; }}

    .stButton>button {{
        background: {PALETTE['primary']}; color:#fff; border:1px solid {PALETTE['primary']};
        border-radius:10px; padding:10px 16px; font-weight:600;
        box-shadow: 0 1px 2px rgba(37,99,235,.25);
    }}
    .stButton>button:hover {{ filter: brightness(1.03); }}

    .stSelectbox label, .stDateInput label {{ color: {PALETTE['text']} !important; font-weight: 600 !important; font-size: 13px !important; }}
    .stSelectbox [data-baseweb="select"] {{ 
        color: {PALETTE['text']} !important; 
        background: {PALETTE['card']} !important;
        border: 1px solid {PALETTE['border']} !important;
        border-radius: 8px !important;
    }}
    .stSelectbox [data-baseweb="select"] > div {{ 
        background: {PALETTE['card']} !important; 
        color: {PALETTE['text']} !important; 
    }}
    
    .stDateInput input {{
        background: {PALETTE['card']} !important;
        color: {PALETTE['text']} !important;
        border: 1px solid {PALETTE['border']} !important;
        border-radius: 8px !important;
    }}

    /* === PLOTLY (Unchanged) === */
    .js-plotly-plot .plotly text {{ fill: {PALETTE['text']} !important; }}
    .js-plotly-plot .plotly .xtick text, .js-plotly-plot .plotly .ytick text {{ fill: {PALETTE['text']} !important; }}
    
    .js-plotly-plot .hoverlayer .hovertext {{ 
        fill: #ffffff !important; 
        color: #ffffff !important;
    }}
    .js-plotly-plot .hoverlayer .hovertext text {{ 
        fill: #ffffff !important; 
        color: #ffffff !important;
    }}
    .js-plotly-plot .hoverlayer .hovertext path {{ 
        fill: #1F2937 !important; 
    }}

    footer {{ visibility: hidden; }}
    </style>
    """

def plotly_layout():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=PALETTE["text"], size=12),
        xaxis=dict(
            gridcolor="#EEF0F4", 
            linecolor=PALETTE["border"], 
            zerolinecolor=PALETTE["border"],
            tickfont=dict(color=PALETTE["text"], size=11)
        ),
        yaxis=dict(
            gridcolor="#EEF0F4", 
            linecolor=PALETTE["border"], 
            zerolinecolor=PALETTE["border"],
            tickfont=dict(color=PALETTE["text"], size=11)
        ),
        hoverlabel=dict(
            bgcolor="#1F2937",
            font=dict(family="Inter, sans-serif", size=13, color="#FFFFFF"),
            bordercolor="#374151"
        ),
        colorway=[PALETTE["primary"], PALETTE["accent"], PALETTE["success"], PALETTE["warning"], PALETTE["danger"], "#0891B2"],
    )