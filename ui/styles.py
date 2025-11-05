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


    /* === HEADER FIX === */
    [data-testid="stHeader"] {{
        background-color: {PALETTE['bg']} !important;
        border-bottom: 1px solid {PALETTE['bg']} !important;
        box-shadow: none !important;
    }}
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}


    /* === PREMIUM GRADIENT SIDEBAR === */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, 
            #0B1120 0%, 
            #0F172A 20%, 
            #1E293B 50%, 
            #2D3748 80%, 
            #374151 100%) !important;
        border-right: 1px solid rgba(96, 165, 250, 0.15) !important;
        box-shadow: 4px 0 12px rgba(0, 0, 0, 0.3) !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
        padding: 24px 20px !important;
    }}
    
    /* Sidebar header styling */
    [data-testid="stSidebar"] h1 {{
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }}
    
    /* Sidebar subtitle/description */
    [data-testid="stSidebar"] p {{
        color: #94A3B8 !important;
        font-size: 13px !important;
    }}
    
    /* Sidebar text - light colors */
    [data-testid="stSidebar"] [data-testid="stMarkdown"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] a {{
        color: #E2E8F0 !important;
    }}
    
    /* Sidebar label text */
    [data-testid="stSidebar"] label {{
        font-weight: 600 !important;
        font-size: 13px !important;
        margin-bottom: 8px !important;
    }}
    
    /* Sidebar inputs - glass morphism */
    [data-testid="stSidebar"] input[type="text"] {{
        background: rgba(30, 41, 59, 0.6) !important;
        color: #F1F5F9 !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stSidebar"] input[type="text"]:focus {{
        border-color: rgba(96, 165, 250, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1) !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }}
    [data-testid="stSidebar"] input::placeholder {{
        color: #64748B !important;
    }}
    
    /* Sidebar buttons - premium gradient */
    [data-testid="stSidebar"] button[kind="primary"] {{
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 50%, #1E40AF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 14px 20px !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4), 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }}
    [data-testid="stSidebar"] button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 50%, #1E3A8A 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5), 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }}
    [data-testid="stSidebar"] button[kind="primary"]:active {{
        transform: translateY(0px) !important;
    }}
    
    /* Radio buttons - styled */
    [data-testid="stSidebar"] [role="radiogroup"] {{
        background: rgba(30, 41, 59, 0.5) !important;
        border-radius: 10px !important;
        padding: 10px !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
    }}
    
    /* Selectbox styling */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 10px !important;
    }}
    
    /* Divider lines */
    [data-testid="stSidebar"] hr {{
        border-color: rgba(148, 163, 184, 0.2) !important;
        margin: 20px 0 !important;
    }}
    
    
    /* === MAIN CONTENT STYLES === */
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


    /* === PLOTLY === */
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
