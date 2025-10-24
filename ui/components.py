# ui/components.py

import streamlit as st

def kpi(label, value, change, positive=True):
    """Enhanced KPI card with gradient and exact numbers"""
    # Define light blue gradient colors based on position
    gradients = {
        "Subscribers": "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)",  # Very light blue
        "Total Views": "linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%)",  # Light blue
        "Total Videos": "linear-gradient(135deg, #BFDBFE 0%, #93C5FD 100%)",  # Medium light blue
        "Engagement Rate": "linear-gradient(135deg, #93C5FD 0%, #60A5FA 100%)"  # Medium blue
    }
    
    gradient = gradients.get(label, "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)")
    
    change_color = "#10B981" if positive else "#EF4444"
    change_icon = "▲" if positive else "▼"
    
    st.markdown(f"""
    <div style="background: {gradient}; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #E0F2FE;">
        <div style="color: #64748B; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">{label}</div>
        <div style="color: #1E293B; font-size: 28px; font-weight: 700; margin-bottom: 6px; font-family: 'Inter', sans-serif;">{value}</div>
        <div style="color: {change_color}; font-size: 12px; font-weight: 600;">
            {change_icon} {change}
        </div>
    </div>
    """, unsafe_allow_html=True)


def chart_card(title):
    """Card container for charts"""
    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #E5E7EB;">
        <h3 style="margin: 0 0 15px 0; color: #1F2937; font-size: 16px; font-weight: 600;">{title}</h3>
    </div>
    """, unsafe_allow_html=True)
    return st.container()


def end_card():
    """End card container"""
    pass


def section(title, subtitle=""):
    """Section header"""
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h1 style="margin: 0; color: #1F2937; font-size: 32px; font-weight: 700;">{title}</h1>
        <p style="margin: 8px 0 0 0; color: #6B7280; font-size: 14px;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def info_card(title, description):
    """Info card for landing page"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-radius: 10px; padding: 24px; border: 1px solid #BFDBFE;">
        <h3 style="margin: 0 0 12px 0; color: #1E293B; font-size: 18px; font-weight: 600;">{title}</h3>
        <p style="margin: 0; color: #475569; font-size: 14px; line-height: 1.6;">{description}</p>
    </div>
    """, unsafe_allow_html=True)
