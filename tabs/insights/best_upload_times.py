# tabs/insights/best_upload_times.py
import streamlit as st
import plotly.graph_objects as go


def render_best_upload_times(insights):
    """Render Best Upload Times with aligned styling"""
    
    st.markdown("""
        <style>
        .chart-card {
            background: linear-gradient(135deg, rgba(173, 216, 230, 0.15) 0%, rgba(6, 95, 212, 0.08) 100%);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .insight-box {
            background: linear-gradient(135deg, rgba(173, 216, 230, 0.4) 0%, rgba(6, 95, 212, 0.2) 100%);
            border-left: 4px solid #065FD4;
            border-radius: 8px;
            padding: 15px 20px;
            margin-top: 20px;
            font-size: 14px;
            color: #2c3e50;
        }
        .insight-icon {
            font-size: 18px;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("### 📅 Best Upload Times")
    st.markdown("*Discover which days get the best results*")
    
    try:
        df = insights.df.copy()
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_stats = df.groupby('publish_day').agg({
            'view_count': 'mean',
            'engagement_rate': 'mean'
        }).reindex(day_order)
        
        fig = go.Figure()
        
        for idx, day in enumerate(day_order):
            views = day_stats.loc[day, 'view_count']
            normalized = idx / (len(day_order) - 1)
            
            # Gradient from light to dark blue
            r = int(173 + (6 - 173) * normalized)
            g = int(216 + (95 - 216) * normalized)
            b = int(230 + (212 - 230) * normalized)
            bar_color = f'rgb({r},{g},{b})'
            
            fig.add_trace(go.Bar(
                x=[day],
                y=[views],
                marker=dict(
                    color=bar_color,
                    line=dict(color='rgba(255,255,255,0.6)', width=1.5),
                    cornerradius=10
                ),
                text=f"{views:,.0f}",
                textposition='outside',
                textfont=dict(size=11, color='#2c3e50', weight='bold'),
                hovertemplate=f'<b>{day}</b><br>Avg Views: {views:,.0f}<br><extra></extra>',
                showlegend=False
            ))
        
        fig.update_layout(
            height=320,
            plot_bgcolor='rgba(173, 216, 230, 0.05)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=30, t=10, b=50),
            xaxis=dict(
                title=dict(text='Day of Week', font=dict(size=11, color='#5a6c7d')),
                tickfont=dict(size=10, color='#2c3e50'),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text='Average Views', font=dict(size=11, color='#5a6c7d')),
                gridcolor='rgba(200,200,200,0.3)',
                gridwidth=1,
                showgrid=True,
                tickfont=dict(size=10, color='#2c3e50'),
                tickformat=',d'
            ),
            hoverlabel=dict(bgcolor='white', font_size=11, font_family='Arial')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="best_days", config={'displayModeBar': False})
        
        best_day = day_stats['view_count'].idxmax()
        best_views = day_stats['view_count'].max()
        
        st.markdown(f"""
            <div class="insight-box">
                <span class="insight-icon">💡</span>
                <strong>Best Day:</strong> {best_day} gets the highest average views ({best_views:,.0f})!
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
