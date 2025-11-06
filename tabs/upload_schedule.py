# tabs/upload_schedule.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_upload_schedule_tab(df):
    """Render Upload Schedule Analysis tab"""
    
    # Title with better spacing
    st.markdown("")
    st.markdown("## 📅 Upload Schedule Analysis")
    st.markdown("")
    
    # ===== HOUR CHART FIRST (Full Width at Top) =====
    st.markdown("### ⏰ Uploads by Hour (UTC)")
    
    hour_uploads = df.groupby('publish_hour').size().reset_index(name='count')
    hour_uploads = hour_uploads.sort_values('publish_hour')
    
    # Find peak hour
    peak_hour = hour_uploads.loc[hour_uploads['count'].idxmax(), 'publish_hour']
    peak_count = hour_uploads['count'].max()
    
    fig_hour = go.Figure()
    
    # Area fill - BLUE only
    fig_hour.add_trace(go.Scatter(
        x=hour_uploads['publish_hour'],
        y=hour_uploads['count'],
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(6, 95, 212, 0.15)',
        line=dict(color='rgb(6, 95, 212)', width=3),
        name='Uploads',
        hovertemplate='<b>Hour %{x}:00</b><br>Uploads: %{y}<extra></extra>'
    ))
    
    # Add markers
    fig_hour.add_trace(go.Scatter(
        x=hour_uploads['publish_hour'],
        y=hour_uploads['count'],
        mode='markers',
        marker=dict(
            size=8,
            color='rgb(6, 95, 212)',
            line=dict(color='white', width=2)
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Highlight peak hour
    fig_hour.add_annotation(
        x=peak_hour,
        y=peak_count,
        text=f"Peak: {peak_count}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#065fd4",
        ax=0,
        ay=-40,
        bgcolor="rgba(6, 95, 212, 0.1)",
        bordercolor="#065fd4",
        borderwidth=2,
        borderpad=4,
        font=dict(size=11, color="#2c3e50")
    )
    
    fig_hour.update_layout(
        height=320,
        plot_bgcolor='rgba(248,249,250,0.3)',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=50),
        xaxis=dict(
            title=dict(text='Hour of Day (UTC)', font=dict(size=12, color='#5a6c7d')),
            tickmode='linear',
            tick0=0,
            dtick=3,
            tickfont=dict(size=11, color='#2c3e50'),
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        yaxis=dict(
            title=dict(text='Upload Count', font=dict(size=12, color='#5a6c7d')),
            gridcolor='rgba(200,200,200,0.2)',
            gridwidth=1
        ),
        hoverlabel=dict(bgcolor="white", font_size=11)
    )
    
    st.plotly_chart(fig_hour, use_container_width=True, key="hour_chart")
    st.markdown(f"⚡ **Peak upload hour:** {peak_hour}:00 UTC ({peak_count} uploads)")
    
    # Divider
    st.markdown("---")
    
    # ===== DAY CHART SECOND (Full Width at Bottom) =====
    st.markdown("### 📊 Uploads by Day")
    
    day_uploads = df.groupby('publish_day').size().reset_index(name='uploads')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_uploads['publish_day'] = pd.Categorical(day_uploads['publish_day'], categories=day_order, ordered=True)
    day_uploads = day_uploads.sort_values('publish_day')
    
    # Create BLUE gradient colors (light to dark) based on upload count
    max_uploads = day_uploads['uploads'].max()
    colors = []
    for val in day_uploads['uploads']:
        normalized = val / max_uploads
        # Light blue to dark blue gradient
        r = int(173 + (6 - 173) * normalized)
        g = int(216 + (95 - 216) * normalized)
        b = int(230 + (212 - 230) * normalized)
        colors.append(f'rgb({r},{g},{b})')
    
    fig_day = go.Figure()
    
    fig_day.add_trace(go.Bar(
        x=day_uploads['publish_day'],
        y=day_uploads['uploads'],
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.6)', width=1.5),
            cornerradius=8
        ),
        text=day_uploads['uploads'],
        textposition='outside',
        textfont=dict(size=13, color='#2c3e50', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Uploads: %{y}<extra></extra>'
    ))
    
    fig_day.update_layout(
        height=380,
        plot_bgcolor='rgba(248,249,250,0.3)',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=50),
        xaxis=dict(
            title=dict(text='Day of Week', font=dict(size=12, color='#5a6c7d')),
            tickfont=dict(size=11, color='#2c3e50'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text='Uploads', font=dict(size=12, color='#5a6c7d')),
            gridcolor='rgba(200,200,200,0.2)',
            gridwidth=1,
            showgrid=True
        ),
        hoverlabel=dict(bgcolor="white", font_size=11)
    )
    
    st.plotly_chart(fig_day, use_container_width=True, key="day_chart")
    
    # Best day insight
    best_day = day_uploads.loc[day_uploads['uploads'].idxmax(), 'publish_day']
    st.markdown(f"🌟 **Most active day:** {best_day} ({max_uploads} uploads)")
