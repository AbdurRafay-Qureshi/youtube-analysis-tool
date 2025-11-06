# tabs/insights/growth_timeline.py
import streamlit as st
import plotly.graph_objects as go


def render_growth_timeline(insights):
    """Render Growth Timeline with progressive gradient stats"""
    
    st.markdown("""
    <style>
    .chart-card {
        background: linear-gradient(135deg, rgba(173, 216, 230, 0.15) 0%, rgba(6, 95, 212, 0.08) 100%);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .stat-card {
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        cursor: help;
    }
    .stat-card:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    .tooltip {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 110%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.9);
        color: #fff;
        text-align: center;
        padding: 10px 15px;
        border-radius: 8px;
        width: 220px;
        font-size: 11px;
        line-height: 1.4;
        z-index: 1000;
        transition: opacity 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(0, 0, 0, 0.9) transparent transparent transparent;
    }
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        margin: 8px 0;
    }
    .stat-label {
        font-size: 13px;
        opacity: 0.95;
    }
    /* Progressive gradient: Light blue → Medium blue → Vibrant blue */
    .stat-card-1 { 
        background: linear-gradient(135deg, #E8F4F8 0%, #B3D9EC 100%);
        color: #2c3e50;
    }
    .stat-card-2 { 
        background: linear-gradient(135deg, #7EC8E3 0%, #3FA9D8 100%);
        color: white;
    }
    .stat-card-3 { 
        background: linear-gradient(135deg, #2E86DE 0%, #1B6DC1 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Growth Timeline")
    st.markdown("*Cumulative views growth over time*")
    
    try:
        df = insights.df.copy()
        df = df.sort_values('upload_date')
        
        df['cumulative_views'] = df['view_count'].cumsum()
        df['video_number'] = range(1, len(df) + 1)
        df['date_str'] = df['upload_date'].dt.strftime('%b %d, %Y')
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['upload_date'],
            y=df['cumulative_views'],
            mode='lines',
            name='Total Views',
            line=dict(color='rgb(6, 95, 212)', width=3),
            fill='tozeroy',
            fillcolor='rgba(6, 95, 212, 0.1)',
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                          'Total Views: %{y:,.0f}<br>' +
                          'Video #: %{customdata[1]}<br>' +
                          '<extra></extra>',
            customdata=df[['date_str', 'video_number']].values
        ))
        
        # Add milestone annotations
        milestone_step = 5_000_000
        max_views = df['cumulative_views'].max()
        
        current_milestone = milestone_step
        while current_milestone <= max_views:
            closest_idx = (df['cumulative_views'] - current_milestone).abs().idxmin()
            milestone_date = df.loc[closest_idx, 'upload_date']
            milestone_views = df.loc[closest_idx, 'cumulative_views']
            
            fig.add_annotation(
                x=milestone_date,
                y=milestone_views,
                text=f"{current_milestone/1_000_000:.0f}M",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#065fd4',
                ax=0,
                ay=-30,
                bgcolor='rgba(6, 95, 212, 0.1)',
                bordercolor='#065fd4',
                borderwidth=2,
                borderpad=4,
                font=dict(size=10, color='#2c3e50')
            )
            
            current_milestone += milestone_step
        
        fig.update_layout(
            height=320,
            plot_bgcolor='rgba(173, 216, 230, 0.05)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=30, t=10, b=50),
            showlegend=False,
            xaxis=dict(
                title=dict(text='Upload Date', font=dict(size=11, color='#5a6c7d')),
                gridcolor='rgba(200,200,200,0.3)',
                showgrid=True,
                tickfont=dict(size=10, color='#2c3e50'),
                tickformat='%b %Y'
            ),
            yaxis=dict(
                title=dict(text='Cumulative Views', font=dict(size=11, color='#5a6c7d')),
                gridcolor='rgba(200,200,200,0.3)',
                showgrid=True,
                tickfont=dict(size=10, color='#2c3e50'),
                tickformat=',d'
            ),
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=11, font_family='Arial')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="growth_timeline", config={'displayModeBar': False})
        
        # Progressive gradient stat cards with tooltips
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        total_videos = len(df)
        total_views = df['cumulative_views'].iloc[-1]
        avg_per_video = total_views / total_videos
        
        with col1:
            st.markdown(f"""
                <div class="stat-card stat-card-1">
                    <div class="tooltip">
                        <strong>How it's calculated:</strong><br>
                        Total count of all videos uploaded to your channel. Each video = 1 count.
                    </div>
                    <div class="stat-label">📹 Total Videos</div>
                    <div class="stat-value">{total_videos:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-card stat-card-2">
                    <div class="tooltip">
                        <strong>How it's calculated:</strong><br>
                        Sum of all views across all {total_videos} videos. This is your total reach!
                    </div>
                    <div class="stat-label">👁️ Total Views</div>
                    <div class="stat-value">{total_views:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-card stat-card-3">
                    <div class="tooltip">
                        <strong>How it's calculated:</strong><br>
                        Total Views ÷ Total Videos<br>
                        {total_views:,.0f} ÷ {total_videos} = {avg_per_video:,.0f}
                    </div>
                    <div class="stat-label">📊 Avg per Video</div>
                    <div class="stat-value">{avg_per_video:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
