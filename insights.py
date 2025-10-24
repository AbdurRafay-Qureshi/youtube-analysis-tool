# insights.py
# User-friendly analytics charts for content creators

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


class YouTubeInsights:
    """Generate practical, actionable insights for YouTube creators"""
    
    def __init__(self, df, channel_stats):
        self.df = df
        self.stats = channel_stats
    
    def growth_timeline(self):
        """Show cumulative growth over time"""
        df_sorted = self.df.sort_values('upload_date').copy()
        df_sorted['cumulative_views'] = df_sorted['view_count'].cumsum()
        df_sorted['video_number'] = range(1, len(df_sorted) + 1)
        
        fig = go.Figure()
        
        # Cumulative views
        fig.add_trace(go.Scatter(
            x=df_sorted['upload_date'],
            y=df_sorted['cumulative_views'],
            mode='lines',
            name='Total Views',
            line=dict(color='#2563EB', width=3),
            fill='tonexty',
            fillcolor='rgba(37, 99, 235, 0.1)',
            customdata=np.column_stack((
                df_sorted['video_number'].values,
                df_sorted['title'].values
            )),
            hovertemplate=(
                '<b style="color:white">Date: %{x|%b %d, %Y}</b><br>' +
                '<span style="color:white">Total Views: %{y:,}</span><br>' +
                '<span style="color:white">Video #: %{customdata[0]}</span><br>' +
                '<span style="color:white">Latest: %{customdata[1]:.40}...</span><extra></extra>'
            )
        ))
        
        # Video count
        fig.add_trace(go.Scatter(
            x=df_sorted['upload_date'],
            y=df_sorted['video_number'],
            mode='lines',
            name='Video Count',
            line=dict(color='#16A34A', width=2, dash='dot'),
            yaxis='y2',
            hovertemplate='<b style="color:white">%{x|%b %d, %Y}</b><br><span style="color:white">Videos: %{y}</span><extra></extra>'
        ))
        
        fig.update_layout(
            yaxis=dict(title='Cumulative Views', side='left'),
            yaxis2=dict(title='Video Count', side='right', overlaying='y', showgrid=False),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            hoverlabel=dict(
                bgcolor='#1F2937',
                font=dict(size=13, family='Inter, sans-serif', color='#FFFFFF'),
                bordercolor='#374151'
            )
        )
        
        return fig
    
    def best_performing_timeframes(self):
        """Identify which days/times get best performance"""
        day_performance = self.df.groupby('publish_day').agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'like_count': 'mean'
        }).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=day_performance.index,
            y=day_performance['view_count'],
            name='Avg Views',
            marker=dict(color='#2563EB'),
            text=day_performance['view_count'].apply(lambda x: f'{x:,.0f}'),
            textposition='outside',
            customdata=day_performance['engagement_rate'].values,
            hovertemplate='<b style="color:white">%{x}</b><br><span style="color:white">Avg Views: %{y:,}</span><br><span style="color:white">Avg Engagement: %{customdata:.2f}%</span><extra></extra>'
        ))
        
        fig.update_layout(
            title='Average Performance by Day',
            yaxis_title='Average Views',
            showlegend=False,
            hoverlabel=dict(
                bgcolor='#1F2937',
                font=dict(size=13, family='Inter, sans-serif', color='#FFFFFF'),
                bordercolor='#374151'
            )
        )
        
        return fig
    
    def video_length_performance(self):
        """Analyze optimal video length with detailed breakdown"""
        bins = [0, 300, 600, 900, 1800, 3600, float('inf')]
        labels = ['0-5 min', '5-10 min', '10-15 min', '15-30 min', '30-60 min', '60+ min']
        
        df_bins = self.df.copy()
        df_bins['duration_category'] = pd.cut(df_bins['duration_seconds'], bins=bins, labels=labels)
        
        length_analysis = df_bins.groupby('duration_category', observed=True).agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'title': 'count'
        }).rename(columns={'title': 'video_count'})
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=length_analysis.index.astype(str),
            y=length_analysis['view_count'],
            name='Avg Views',
            marker=dict(
                color=length_analysis['engagement_rate'], 
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title='Engagement %', x=1.15)
            ),
            text=length_analysis['video_count'].apply(lambda x: f'{int(x)} videos'),
            textposition='outside',
            customdata=np.column_stack((
                length_analysis['engagement_rate'].values,
                length_analysis['video_count'].values
            )),
            hovertemplate=(
                '<b style="color:white">%{x}</b><br>' +
                '<span style="color:white">Avg Views: %{y:,.0f}</span><br>' +
                '<span style="color:white">Videos: %{customdata[1]:.0f}</span><br>' +
                '<span style="color:white">Avg Engagement: %{customdata[0]:.2f}%</span><extra></extra>'
            )
        ))
        
        fig.update_layout(
            title='Performance by Video Length',
            xaxis_title='Duration',
            yaxis_title='Average Views',
            height=400,
            hoverlabel=dict(
                bgcolor='#1F2937',
                font=dict(size=13, family='Inter, sans-serif', color='#FFFFFF'),
                bordercolor='#374151'
            )
        )
        
        return fig, df_bins
    
    def engagement_heatmap(self):
        """Show engagement patterns by day and hour"""
        heatmap_data = self.df.groupby(['publish_day', 'publish_hour']).agg({
            'engagement_rate': 'mean',
            'view_count': 'mean',
            'title': 'count'
        }).reset_index()
        
        pivot_engagement = heatmap_data.pivot(index='publish_day', columns='publish_hour', values='engagement_rate')
        pivot_views = heatmap_data.pivot(index='publish_day', columns='publish_hour', values='view_count')
        pivot_count = heatmap_data.pivot(index='publish_day', columns='publish_hour', values='title')
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_engagement = pivot_engagement.reindex(day_order)
        pivot_views = pivot_views.reindex(day_order)
        pivot_count = pivot_count.reindex(day_order)
        
        hover_text = []
        for day in day_order:
            row_hover = []
            for hour in range(24):
                if hour in pivot_engagement.columns and pd.notna(pivot_engagement.loc[day, hour]):
                    engagement = pivot_engagement.loc[day, hour]
                    views = pivot_views.loc[day, hour]
                    count = pivot_count.loc[day, hour]
                    text = (
                        f"<b style='color:white'>{day} at {hour:02d}:00 UTC</b><br>" +
                        f"<span style='color:white'>Avg Engagement: {engagement:.2f}%</span><br>" +
                        f"<span style='color:white'>Avg Views: {views:,.0f}</span><br>" +
                        f"<span style='color:white'>Videos: {int(count)}</span>"
                    )
                else:
                    text = f"<b style='color:white'>{day} at {hour:02d}:00</b><br><span style='color:white'>No data</span>"
                row_hover.append(text)
            hover_text.append(row_hover)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_engagement.values,
            x=[f"{h:02d}:00" for h in range(24)],
            y=day_order,
            colorscale='Blues',
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            colorbar=dict(title='Engagement %')
        ))
        
        fig.update_layout(
            title='📊 Engagement Heatmap: Best Times to Upload',
            xaxis_title='Hour (UTC)',
            yaxis_title='Day of Week',
            height=450,
            hoverlabel=dict(
                bgcolor='#1F2937',
                font=dict(size=13, family='Inter, sans-serif', color='#FFFFFF'),
                bordercolor='#374151'
            )
        )
        
        return fig
    
    def performance_matrix(self):
        """Quadrant analysis: Views vs Engagement"""
        median_views = self.df['view_count'].median()
        median_engagement = self.df['engagement_rate'].median()
        
        df_matrix = self.df.copy()
        df_matrix['category'] = 'Low Views, Low Engagement'
        df_matrix.loc[(df_matrix['view_count'] >= median_views) & (df_matrix['engagement_rate'] < median_engagement), 'category'] = 'High Views, Low Engagement'
        df_matrix.loc[(df_matrix['view_count'] < median_views) & (df_matrix['engagement_rate'] >= median_engagement), 'category'] = 'Low Views, High Engagement'
        df_matrix.loc[(df_matrix['view_count'] >= median_views) & (df_matrix['engagement_rate'] >= median_engagement), 'category'] = '⭐ High Views, High Engagement'
        
        fig = px.scatter(
            df_matrix,
            x='view_count',
            y='engagement_rate',
            color='category',
            size='like_count',
            hover_name='title',
            hover_data={
                'view_count': ':,',
                'engagement_rate': ':.2f',
                'like_count': ':,',
                'category': True
            },
            color_discrete_map={
                '⭐ High Views, High Engagement': '#16A34A',
                'High Views, Low Engagement': '#2563EB',
                'Low Views, High Engagement': '#7C3AED',
                'Low Views, Low Engagement': '#94A3B8'
            }
        )
        
        fig.add_hline(
            y=median_engagement,
            line_dash="dot",
            line_color="gray",
            opacity=0.5,
            annotation_text=f"Median Engagement: {median_engagement:.2f}%",
            annotation_position="right"
        )
        fig.add_vline(
            x=median_views,
            line_dash="dot",
            line_color="gray",
            opacity=0.5,
            annotation_text=f"Median Views: {median_views:,.0f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            title='Content Performance Matrix',
            xaxis_title='Views',
            yaxis_title='Engagement Rate (%)',
            legend=dict(title='Performance Quadrant', orientation='v', yanchor='top', y=1, xanchor='left', x=1.02),
            height=500,
            hoverlabel=dict(
                bgcolor='#1F2937',
                font=dict(size=13, family='Inter, sans-serif', color='#FFFFFF'),
                bordercolor='#374151'
            )
        )
        
        return fig
    
    def consistency_score(self):
        """Show upload consistency over time"""
        df_sorted = self.df.sort_values('upload_date').copy()
        df_sorted['days_since_last'] = df_sorted['upload_date'].diff().dt.days
        df_sorted['consistency_ma'] = df_sorted['days_since_last'].rolling(window=5, min_periods=1).mean()
        
        fig = go.Figure()
        
        # Individual uploads
        fig.add_trace(go.Scatter(
            x=df_sorted['upload_date'],
            y=df_sorted['days_since_last'],
            mode='markers',
            name='Days Between Uploads',
            marker=dict(color='#94A3B8', size=8),
            customdata=df_sorted['title'].values,
            hovertemplate=(
                '<b style="color:white">%{x|%b %d, %Y}</b><br>' +
                '<span style="color:white">Days since last: %{y:.0f}</span><br>' +
                '<span style="color:white">Video: %{customdata:.40}...</span><extra></extra>'
            )
        ))
        
        # Moving average
        fig.add_trace(go.Scatter(
            x=df_sorted['upload_date'],
            y=df_sorted['consistency_ma'],
            mode='lines',
            name='5-Video Average',
            line=dict(color='#2563EB', width=3),
            hovertemplate='<b style="color:white">%{x|%b %d, %Y}</b><br><span style="color:white">Avg: %{y:.1f} days</span><extra></extra>'
        ))
        
        fig.update_layout(
            title='Upload Consistency Over Time',
            xaxis_title='Date',
            yaxis_title='Days Between Uploads',
            hovermode='x unified',
            height=400,
            hoverlabel=dict(
                bgcolor='#1F2937',
                font=dict(size=13, family='Inter, sans-serif', color='#FFFFFF'),
                bordercolor='#374151'
            )
        )
        
        return fig
