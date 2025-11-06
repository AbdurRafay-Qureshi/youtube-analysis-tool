# tabs/insights/__init__.py
import streamlit as st
from .summary_cards import render_summary_cards
from .growth_timeline import render_growth_timeline
from .performance_matrix import render_performance_matrix
from .best_upload_times import render_best_upload_times
from .video_length_impact import render_video_length_impact
from .engagement_heatmap import render_engagement_heatmap


def render_insights_tab(df, stats):
    """Main Insights tab - orchestrates all sub-components"""
    
    if df.empty:
        from ui.components import info_card
        info_card("Insights", "Analyze your content with practical, actionable insights")
        return
    
    from insights import YouTubeInsights
    insights = YouTubeInsights(df, stats)
    
    # Header
    st.markdown("## 💡 Channel Insights")
    st.markdown("")
    
    # ===== TOP: Summary KPI Cards =====
    render_summary_cards(df)
    
    st.markdown("---")
    
    # ===== ROW 1: Growth + Performance =====
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        render_growth_timeline(insights)
    
    with col2:
        render_performance_matrix(insights)
    
    st.markdown("---")
    
    # ===== ROW 2: Upload Times + Video Length =====
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        render_best_upload_times(insights)
    
    with col2:
        render_video_length_impact(insights)
    
    st.markdown("---")
    
    # ===== FULL WIDTH: Heatmap =====
    render_engagement_heatmap(insights)


# IMPORTANT: Export the main function
__all__ = ['render_insights_tab']
