# tabs/top_videos.py
import streamlit as st
import plotly.graph_objects as go
from ui.components import chart_card, end_card
from ui.styles import plotly_layout


def render_top_videos_tab(df):
    """Render Top 10 Videos by Metric tab"""
    
    cont = chart_card("Top 10 by Metric")
    
    sort_by = st.selectbox(
        "Sort by",
        ["view_count", "like_count", "comment_count", "engagement_rate"],
        format_func=lambda s: s.replace("_", " ").title(),
        key="sort_top",
    )
    
    top = df.nlargest(10, sort_by)
    
    # Shorten titles for better display
    top['short_title'] = top['title'].apply(
        lambda x: x[:50] + '...' if len(x) > 50 else x
    )
    
    # Create gradient colors based on engagement_rate
    engagement_values = top['engagement_rate'].values
    colors = []
    for val in engagement_values:
        # Map engagement rate to blue gradient (lighter to darker)
        normalized = (val - engagement_values.min()) / (engagement_values.max() - engagement_values.min() + 0.001)
        # Create gradient from light blue to dark blue
        r = int(65 + (20 - 65) * normalized)
        g = int(105 + (53 - 105) * normalized)
        b = int(225 + (147 - 225) * normalized)
        colors.append(f'rgb({r},{g},{b})')
    
    # Use graph_objects for more control over styling
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top['short_title'],
        x=top[sort_by],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.8)', width=2),
            cornerradius=10
        ),
        text=[f"{v:,.0f}" for v in top[sort_by]],
        textposition='outside',
        textfont=dict(size=11, color='#2c3e50', family='Arial, sans-serif'),
        hovertemplate='<b>%{customdata[0]}</b><br><br>' +
                      'Views: %{customdata[1]:,}<br>' +
                      'Likes: %{customdata[2]:,}<br>' +
                      'Comments: %{customdata[3]:,}<br>' +
                      'Engagement: %{customdata[4]:.2f}%' +
                      '<extra></extra>',
        customdata=top[['title', 'view_count', 'like_count', 'comment_count', 'engagement_rate']].values
    ))
    
    # Get base layout first
    layout_config = plotly_layout()
    
    # Override/add specific settings
    layout_config.update({
        'height': 550,
        'plot_bgcolor': 'rgba(248,249,250,0.5)',
        'margin': dict(l=20, r=80, t=40, b=50),
        'xaxis': dict(
            gridcolor='rgba(200,200,200,0.2)',
            gridwidth=1,
            showgrid=True,
            zeroline=False,
            title=dict(
                text=sort_by.replace("_", " ").title(),
                font=dict(size=13, color='#34495e')
            )
        ),
        'yaxis': dict(
            categoryorder="total ascending",
            tickfont=dict(size=12, color='#2c3e50', family='Arial, sans-serif'),
            showgrid=False
        ),
        'hoverlabel': dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    })
    
    fig.update_layout(**layout_config)
    st.plotly_chart(fig, use_container_width=True, key="chart_top10")
    end_card()
