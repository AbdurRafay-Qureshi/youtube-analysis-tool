# tabs/insights/video_length_impact.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_video_length_impact(insights):
    """Render Video Length Impact with aligned styling"""
    
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
    st.markdown("### ⏱️ Video Length Impact")
    st.markdown("*Find the sweet spot for your content*")
    
    try:
        df = insights.df.copy()
        
        bins = [0, 5*60, 10*60, 15*60, 30*60, float('inf')]
        labels = ['0-5 min', '5-10 min', '10-15 min', '15-30 min', '30-60 min']
        
        df['duration_bin'] = pd.cut(df['duration_seconds'], bins=bins, labels=labels)
        
        length_stats = df.groupby('duration_bin', observed=True).agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'title': 'count'
        }).rename(columns={'title': 'video_count'})
        
        fig = go.Figure()
        
        for idx, (duration, row) in enumerate(length_stats.iterrows()):
            normalized = idx / (len(length_stats) - 1)
            
            r = int(173 + (6 - 173) * normalized)
            g = int(216 + (95 - 216) * normalized)
            b = int(230 + (212 - 230) * normalized)
            bar_color = f'rgb({r},{g},{b})'
            
            fig.add_trace(go.Bar(
                name='Avg Views',
                x=[str(duration)],
                y=[row['view_count']],
                marker=dict(
                    color=bar_color,
                    line=dict(color='rgba(255,255,255,0.6)', width=1.5),
                    cornerradius=10
                ),
                text=f"{row['view_count']:,.0f}",
                textposition='outside',
                textfont=dict(size=10, color='#2c3e50'),
                hovertemplate=f'<b>{duration}</b><br>' +
                              f'Avg Views: {row["view_count"]:,.0f}<br>' +
                              f'Videos: {int(row["video_count"])}<br>' +
                              f'Engagement: {row["engagement_rate"]:.2f}%<br>' +
                              '<extra></extra>',
                showlegend=False,
                yaxis='y'
            ))
        
        fig.add_trace(go.Scatter(
            name='Engagement',
            x=length_stats.index.astype(str),
            y=length_stats['engagement_rate'],
            mode='lines+markers',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10, color='#FF6B6B', line=dict(color='white', width=2)),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Engagement: %{y:.2f}%<br><extra></extra>'
        ))
        
        fig.update_layout(
            height=320,
            plot_bgcolor='rgba(173, 216, 230, 0.05)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=10, b=50),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10)
            ),
            xaxis=dict(
                title=dict(text='Video Duration', font=dict(size=11, color='#5a6c7d')),
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
            yaxis2=dict(
                title=dict(text='Engagement %', font=dict(size=11, color='#FF6B6B')),
                overlaying='y',
                side='right',
                showgrid=False,
                tickfont=dict(size=10, color='#FF6B6B')
            ),
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=11, font_family='Arial')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="video_length", config={'displayModeBar': False})
        
        best_duration = length_stats['view_count'].idxmax()
        best_views = length_stats.loc[best_duration, 'view_count']
        video_count = length_stats.loc[best_duration, 'video_count']
        
        st.markdown(f"""
            <div class="insight-box">
                <span class="insight-icon">🎯</span>
                <strong>Sweet Spot:</strong> Videos in the <strong>{best_duration}</strong> range perform best ({int(video_count)} videos, {best_views:,.0f} avg views)
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
