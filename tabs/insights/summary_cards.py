# tabs/insights/summary_cards.py
import streamlit as st
from ui.components import kpi


def render_summary_cards(df):
    """Render KPI summary cards at top of Insights tab"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_views = df['view_count'].sum()
        kpi("📈 Total Views", f"{total_views:,.0f}", "")
    
    with col2:
        avg_engagement = df['engagement_rate'].mean()
        kpi("📊 Avg Engagement", f"{avg_engagement:.2f}%", "")
    
    with col3:
        best_day = df.groupby('publish_day')['view_count'].mean().idxmax()
        kpi("🎯 Best Day", best_day, "")
    
    with col4:
        consistency = df.groupby(df['upload_date'].dt.to_period('M')).size().std()
        kpi("📅 Upload Consistency", f"{consistency:.1f}", "videos/month std")
