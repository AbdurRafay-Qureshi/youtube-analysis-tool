# tabs/insights/performance_matrix.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_performance_matrix(insights):
    """Render Performance Matrix with gradient tiles"""
    try:
        # CSS Styles
        st.markdown("""
            <style>
            .chart-card {
                background: linear-gradient(135deg, rgba(173, 216, 230, 0.15) 0%, rgba(6, 95, 212, 0.08) 100%);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .stat-card {
                background: linear-gradient(135deg, #ADD8E6 0%, #065FD4 100%);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
            </style>
        """, unsafe_allow_html=True)
        
        # Chart container
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Performance Matrix")
        st.markdown("*Video performance by views and engagement*")
        
        # Data preparation
        df = insights.df.copy()
        
        # Calculate medians
        median_views = df['view_count'].median()
        median_engagement = df['engagement_rate'].median()
        
        # Create gradient colors
        engagement_normalized = (df['engagement_rate'] - df['engagement_rate'].min()) / \
                              (df['engagement_rate'].max() - df['engagement_rate'].min())
        
        colors = []
        for val in engagement_normalized:
            r = int(173 + (6 - 173) * val)
            g = int(216 + (95 - 216) * val)
            b = int(230 + (212 - 230) * val)
            colors.append(f'rgb({r},{g},{b})')
        
        # Create figure
        fig = go.Figure()
        
        # Add scatter plot
        fig.add_trace(go.Scatter(
            x=df['view_count'],
            y=df['engagement_rate'],
            mode='markers',
            marker=dict(
                size=df['engagement_rate'] * 2,
                color=colors,
                line=dict(color='white', width=1),
                opacity=0.7
            ),
            text=df['title'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Views: %{x:,.0f}<br>' +
                         'Engagement: %{y:.2f}%<br>' +
                         '<extra></extra>',
            showlegend=False
        ))
        
        # Add quadrant lines
        fig.add_hline(
            y=median_engagement,
            line_dash="dash",
            line_color="rgba(150,150,150,0.3)",
            line_width=1
        )
        
        fig.add_vline(
            x=median_views,
            line_dash="dash",
            line_color="rgba(150,150,150,0.3)",
            line_width=1
        )
        
        # Update layout
        fig.update_layout(
            height=320,
            plot_bgcolor='rgba(173, 216, 230, 0.05)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=30, t=10, b=50),
            xaxis=dict(
                title=dict(text='Views', font=dict(size=11, color='#5a6c7d')),
                gridcolor='rgba(200,200,200,0.3)',
                showgrid=True,
                type='log',
                tickfont=dict(size=10, color='#2c3e50')
            ),
            yaxis=dict(
                title=dict(text='Engagement Rate (%)', font=dict(size=11, color='#5a6c7d')),
                gridcolor='rgba(200,200,200,0.3)',
                showgrid=True,
                tickfont=dict(size=10, color='#2c3e50')
            ),
            hovermode='closest',
            hoverlabel=dict(bgcolor='white', font_size=11, font_family='Arial')
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True, key="performance_matrix", config={'displayModeBar': False})
        
        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create columns for stats
        col1, col2, col3 = st.columns(3)
        
        # Calculate stats
        stars = len(df[(df['view_count'] > median_views) & (df['engagement_rate'] > median_engagement)])
        gems = len(df[(df['view_count'] <= median_views) & (df['engagement_rate'] > median_engagement)])
        improve = len(df[(df['view_count'] <= median_views) & (df['engagement_rate'] <= median_engagement)])
        
        # Render stat cards
        with col1:
            st.markdown(f"""
                <div class="stat-card stat-card-1">
                    <div class="tooltip">
                        <strong>How it's calculated:</strong><br>
                        Videos with BOTH above-median views AND above-median engagement. Your best performers!
                    </div>
                    <div class="stat-label">⭐ Star Videos</div>
                    <div class="stat-value">{stars}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="stat-card stat-card-2">
                    <div class="tooltip">
                        <strong>How it's calculated:</strong><br>
                        Videos with below-median views BUT above-median engagement. Great content that needs promotion!
                    </div>
                    <div class="stat-label">💎 Hidden Gems</div>
                    <div class="stat-value">{gems}</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="stat-card stat-card-3">
                    <div class="tooltip">
                        <strong>How it's calculated:</strong><br>
                        Videos with BOTH below-median views AND below-median engagement. These need improvement!
                    </div>
                    <div class="stat-label">🔧 Need Work</div>
                    <div class="stat-value">{improve}</div>
                </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error rendering performance matrix: {str(e)}")
