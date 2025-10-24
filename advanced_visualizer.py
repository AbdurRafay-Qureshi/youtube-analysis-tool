# advanced_visualizer.py
# Advanced visualization module with more chart types and interactive plots

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st


class AdvancedVisualizer:
    """Extended visualization capabilities for YouTube analytics"""
    
    def __init__(self):
        self.color_schemes = {
            'primary': ['#FF0000', '#282828', '#FFFFFF', '#065FD4'],
            'engagement': ['#00D084', '#FFC83D', '#FF4E45'],
            'performance': px.colors.sequential.Viridis
        }
    
    def create_funnel_chart(self, df):
        """Create engagement funnel visualization"""
        total_views = df['view_count'].sum()
        total_likes = df['like_count'].sum()
        total_comments = df['comment_count'].sum()
        
        fig = go.Figure(go.Funnel(
            y=['Views', 'Likes', 'Comments'],
            x=[total_views, total_likes, total_comments],
            textposition="inside",
            textinfo="value+percent initial",
            marker={"color": ["#FF0000", "#FF6B6B", "#FF9999"]}
        ))
        
        fig.update_layout(
            title="Engagement Funnel",
            height=400
        )
        return fig
    
    def create_3d_scatter(self, df):
        """Create 3D scatter plot for multi-dimensional analysis"""
        fig = px.scatter_3d(
            df,
            x='view_count',
            y='like_count',
            z='comment_count',
            color='engagement_rate',
            size='duration_seconds',
            hover_data=['title', 'formatted_date'],
            title='3D Performance Analysis',
            labels={
                'view_count': 'Views',
                'like_count': 'Likes',
                'comment_count': 'Comments'
            },
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(height=700)
        return fig
    
    def create_waterfall_chart(self, df):
        """Create waterfall chart for cumulative view growth"""
        df_sorted = df.sort_values('upload_date')
        top_10 = df_sorted.tail(10)
        
        values = top_10['view_count'].tolist()
        text = [f"{v:,.0f}" for v in values]
        
        fig = go.Figure(go.Waterfall(
            name="Views",
            orientation="v",
            measure=["relative"] * len(values),
            x=top_10['title'].str[:30] + '...',
            textposition="outside",
            text=text,
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Cumulative Views - Last 10 Videos",
            showlegend=False,
            height=500,
            xaxis_tickangle=-45
        )
        return fig
    
    def create_sunburst_chart(self, df):
        """Create sunburst chart for hierarchical data visualization"""
        # Group by year, month, and performance category
        df_copy = df.copy()
        df_copy['year'] = df_copy['upload_date'].dt.year
        df_copy['month'] = df_copy['upload_date'].dt.strftime('%B')
        
        # Categorize performance
        view_median = df_copy['view_count'].median()
        df_copy['performance'] = df_copy['view_count'].apply(
            lambda x: 'High' if x > view_median else 'Low'
        )
        
        fig = px.sunburst(
            df_copy,
            path=['year', 'month', 'performance'],
            values='view_count',
            title='Hierarchical View Distribution',
            color='engagement_rate',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(height=600)
        return fig
    
    def create_treemap(self, df):
        """Create treemap for video performance"""
        df_copy = df.copy()
        df_copy['year_month'] = df_copy['upload_date'].dt.to_period('M').astype(str)
        
        fig = px.treemap(
            df_copy.head(50),
            path=['year_month', 'title'],
            values='view_count',
            color='engagement_rate',
            hover_data=['like_count', 'comment_count'],
            title='Video Performance Treemap (Top 50)',
            color_continuous_scale='Plasma'
        )
        
        fig.update_layout(height=600)
        return fig
    
    def create_violin_plot(self, df):
        """Create violin plot for distribution analysis"""
        fig = go.Figure()
        
        metrics = ['view_count', 'like_count', 'comment_count']
        colors = ['#FF0000', '#00D084', '#065FD4']
        
        for metric, color in zip(metrics, colors):
            fig.add_trace(go.Violin(
                y=df[metric],
                name=metric.replace('_', ' ').title(),
                box_visible=True,
                meanline_visible=True,
                fillcolor=color,
                opacity=0.6,
                x0=metric
            ))
        
        fig.update_layout(
            title="Distribution Analysis (Violin Plot)",
            yaxis_title="Count",
            showlegend=True,
            height=500
        )
        return fig
    
    def create_radar_chart(self, channel_stats, avg_metrics):
        """Create radar chart for channel performance metrics"""
        categories = ['Subscribers', 'Avg Views', 'Avg Likes', 
                     'Avg Comments', 'Engagement Rate']
        
        # Normalize values to 0-100 scale
        values = [
            min(channel_stats['total_subscribers'] / 1000000 * 10, 100),
            min(avg_metrics['view_count'] / 100000 * 10, 100),
            min(avg_metrics['like_count'] / 5000 * 10, 100),
            min(avg_metrics['comment_count'] / 500 * 10, 100),
            min(avg_metrics['engagement_rate'] * 10, 100)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Channel Performance',
            line_color='#FF0000',
            fillcolor='rgba(255, 0, 0, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title="Channel Performance Radar",
            height=500
        )
        return fig
    
    def create_heatmap_calendar(self, df):
        """Create calendar heatmap for upload frequency"""
        df_copy = df.copy()
        df_copy['date'] = df_copy['upload_date'].dt.date
        daily_uploads = df_copy.groupby('date').size().reset_index(name='uploads')
        
        # Create a complete date range
        date_range = pd.date_range(
            start=df['upload_date'].min(),
            end=df['upload_date'].max(),
            freq='D'
        )
        
        full_data = pd.DataFrame({'date': date_range.date})
        full_data = full_data.merge(daily_uploads, on='date', how='left').fillna(0)
        
        full_data['year'] = pd.to_datetime(full_data['date']).dt.year
        full_data['week'] = pd.to_datetime(full_data['date']).dt.isocalendar().week
        full_data['day'] = pd.to_datetime(full_data['date']).dt.day_name()
        
        pivot_data = full_data.pivot_table(
            values='uploads',
            index='day',
            columns='week',
            aggfunc='sum',
            fill_value=0
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                    'Friday', 'Saturday', 'Sunday']
        pivot_data = pivot_data.reindex(day_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Reds',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Upload Frequency Heatmap",
            xaxis_title="Week of Year",
            yaxis_title="Day of Week",
            height=400
        )
        return fig
    
    def create_parallel_coordinates(self, df):
        """Create parallel coordinates plot for multi-variate analysis"""
        df_sample = df.nlargest(100, 'view_count').copy()
        
        # Normalize data
        for col in ['view_count', 'like_count', 'comment_count', 
                   'engagement_rate', 'duration_seconds']:
            if col in df_sample.columns:
                df_sample[f'{col}_norm'] = (
                    (df_sample[col] - df_sample[col].min()) / 
                    (df_sample[col].max() - df_sample[col].min())
                )
        
        fig = go.Figure(data=
            go.Parcoords(
                line=dict(
                    color=df_sample['engagement_rate'],
                    colorscale='Viridis',
                    showscale=True,
                    cmin=df_sample['engagement_rate'].min(),
                    cmax=df_sample['engagement_rate'].max()
                ),
                dimensions=[
                    dict(range=[0, 1],
                         label='Views', values=df_sample['view_count_norm']),
                    dict(range=[0, 1],
                         label='Likes', values=df_sample['like_count_norm']),
                    dict(range=[0, 1],
                         label='Comments', values=df_sample['comment_count_norm']),
                    dict(range=[0, 1],
                         label='Engagement', values=df_sample['engagement_rate_norm']),
                    dict(range=[0, 1],
                         label='Duration', values=df_sample['duration_seconds_norm'])
                ]
            )
        )
        
        fig.update_layout(
            title="Parallel Coordinates Analysis (Top 100 Videos)",
            height=500
        )
        return fig
    
    def create_sankey_diagram(self, df):
        """Create Sankey diagram for engagement flow"""
        # Categorize metrics
        df_copy = df.copy()
        
        view_bins = pd.qcut(df_copy['view_count'], q=3, 
                           labels=['Low Views', 'Medium Views', 'High Views'])
        engagement_bins = pd.qcut(df_copy['engagement_rate'], q=3,
                                 labels=['Low Engagement', 'Medium Engagement', 'High Engagement'])
        
        # Create flow data
        flow_data = pd.crosstab(view_bins, engagement_bins)
        
        # Prepare Sankey data
        sources = []
        targets = []
        values = []
        
        view_categories = ['Low Views', 'Medium Views', 'High Views']
        engagement_categories = ['Low Engagement', 'Medium Engagement', 'High Engagement']
        
        labels = view_categories + engagement_categories
        
        for i, view_cat in enumerate(view_categories):
            for j, eng_cat in enumerate(engagement_categories):
                if view_cat in flow_data.index and eng_cat in flow_data.columns:
                    value = flow_data.loc[view_cat, eng_cat]
                    if value > 0:
                        sources.append(i)
                        targets.append(len(view_categories) + j)
                        values.append(value)
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=['#FF6B6B', '#FFA06B', '#FFE66D', 
                      '#95E1D3', '#4ECDC4', '#2E86AB']
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])
        
        fig.update_layout(
            title="View-to-Engagement Flow",
            height=500
        )
        return fig
    
    def create_box_plot_comparison(self, df):
        """Create comparative box plots"""
        df_copy = df.copy()
        
        # Create year-based comparison
        df_copy['year'] = df_copy['upload_date'].dt.year
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Views by Year', 'Likes by Year', 
                          'Comments by Year', 'Engagement by Year')
        )
        
        years = sorted(df_copy['year'].unique())
        
        # Views
        for year in years:
            data = df_copy[df_copy['year'] == year]['view_count']
            fig.add_trace(
                go.Box(y=data, name=str(year), showlegend=False),
                row=1, col=1
            )
        
        # Likes
        for year in years:
            data = df_copy[df_copy['year'] == year]['like_count']
            fig.add_trace(
                go.Box(y=data, name=str(year), showlegend=False),
                row=1, col=2
            )
        
        # Comments
        for year in years:
            data = df_copy[df_copy['year'] == year]['comment_count']
            fig.add_trace(
                go.Box(y=data, name=str(year), showlegend=False),
                row=2, col=1
            )
        
        # Engagement
        for year in years:
            data = df_copy[df_copy['year'] == year]['engagement_rate']
            fig.add_trace(
                go.Box(y=data, name=str(year), showlegend=False),
                row=2, col=2
            )
        
        fig.update_layout(height=800, title_text="Year-over-Year Performance Comparison")
        return fig
    
    def create_candlestick_chart(self, df):
        """Create candlestick chart for performance ranges"""
        df_copy = df.copy()
        df_copy['year_month'] = df_copy['upload_date'].dt.to_period('M')
        
        monthly_stats = df_copy.groupby('year_month')['view_count'].agg([
            ('open', 'first'),
            ('high', 'max'),
            ('low', 'min'),
            ('close', 'last')
        ]).reset_index()
        
        monthly_stats['year_month'] = monthly_stats['year_month'].astype(str)
        
        fig = go.Figure(data=[go.Candlestick(
            x=monthly_stats['year_month'],
            open=monthly_stats['open'],
            high=monthly_stats['high'],
            low=monthly_stats['low'],
            close=monthly_stats['close'],
            name='Views'
        )])
        
        fig.update_layout(
            title='Monthly View Performance (Candlestick)',
            yaxis_title='Views',
            xaxis_title='Month',
            height=500,
            xaxis_rangeslider_visible=False
        )
        return fig
