# reddit_insights.py
# Reddit-specific analytics and insights

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


class RedditInsights:
    """Generate insights and visualizations for Reddit data"""
    
    def __init__(self, posts_df, stats):
        """
        Initialize Reddit insights.
        
        Args:
            posts_df (pd.DataFrame): Posts dataframe
            stats (dict): Summary statistics
        """
        self.posts_df = posts_df.copy()
        self.stats = stats
        
        # Ensure datetime conversion
        if 'created_utc' in self.posts_df.columns:
            self.posts_df['created_utc'] = pd.to_datetime(self.posts_df['created_utc'], unit='s')
    
    
    def posting_timeline(self):
        """Show posting frequency over time."""
        df = self.posts_df.copy()
        df['date'] = df['created_utc'].dt.date
        
        daily_posts = df.groupby('date').size().reset_index(name='posts')
        daily_posts['date'] = pd.to_datetime(daily_posts['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_posts['date'],
            y=daily_posts['posts'],
            mode='lines+markers',
            name='Posts per Day',
            line=dict(color='#FF4500', width=2.5),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(255, 69, 0, 0.1)'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Date",
            yaxis_title="Number of Posts",
            hovermode='x unified'
        )
        
        return fig
    
    
    def best_posting_times(self):
        """Show which hours and days get best engagement."""
        df = self.posts_df.copy()
        df['hour'] = df['created_utc'].dt.hour
        df['day_name'] = df['created_utc'].dt.day_name()
        
        hourly_avg = df.groupby('hour')['upvotes'].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hourly_avg['hour'],
            y=hourly_avg['upvotes'],
            marker_color='#FF4500',
            name='Avg Upvotes'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Hour of Day (UTC)",
            yaxis_title="Average Upvotes",
            xaxis=dict(tickmode='linear', tick0=0, dtick=2)
        )
        
        return fig
    
    
    def engagement_heatmap(self):
        """Heatmap of posting activity by day and hour."""
        df = self.posts_df.copy()
        df['hour'] = df['created_utc'].dt.hour
        df['day_name'] = df['created_utc'].dt.day_name()
        
        # Create pivot table
        heatmap_data = df.pivot_table(
            values='upvotes',
            index='day_name',
            columns='hour',
            aggfunc='mean',
            fill_value=0
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Oranges',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Hour of Day (UTC)",
            yaxis_title="Day of Week"
        )
        
        return fig
    
    
    def top_subreddits_performance(self):
        """For user analysis: show performance across subreddits."""
        if 'subreddit' not in self.posts_df.columns:
            return None
        
        df = self.posts_df.copy()
        subreddit_stats = df.groupby('subreddit').agg({
            'upvotes': ['sum', 'mean', 'count'],
            'num_comments': 'sum'
        }).reset_index()
        
        subreddit_stats.columns = ['subreddit', 'total_upvotes', 'avg_upvotes', 'post_count', 'total_comments']
        subreddit_stats = subreddit_stats.sort_values('total_upvotes', ascending=False).head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=subreddit_stats['subreddit'],
            x=subreddit_stats['total_upvotes'],
            orientation='h',
            marker_color='#FF4500',
            name='Total Upvotes'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Total Upvotes",
            yaxis_title="Subreddit",
            yaxis=dict(categoryorder='total ascending')
        )
        
        return fig
    
    
    def content_type_analysis(self):
        """Analyze performance by post type (self, link, etc)."""
        df = self.posts_df.copy()
        
        # Determine post type
        if 'is_self' in df.columns:
            df['post_type'] = df['is_self'].map({True: 'Self Post', False: 'Link/Media'})
        else:
            return None
        
        type_stats = df.groupby('post_type').agg({
            'upvotes': 'mean',
            'num_comments': 'mean',
            'title': 'count'
        }).reset_index()
        
        type_stats.columns = ['post_type', 'avg_upvotes', 'avg_comments', 'count']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=type_stats['post_type'],
            y=type_stats['avg_upvotes'],
            name='Avg Upvotes',
            marker_color='#FF4500'
        ))
        fig.add_trace(go.Bar(
            x=type_stats['post_type'],
            y=type_stats['avg_comments'],
            name='Avg Comments',
            marker_color='#2563EB'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Post Type",
            yaxis_title="Average Count",
            barmode='group'
        )
        
        return fig
    
    
    def engagement_distribution(self):
        """Show distribution of upvotes across posts."""
        df = self.posts_df.copy()
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df['upvotes'],
            nbinsx=30,
            marker_color='#FF4500',
            name='Upvotes Distribution'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Upvotes",
            yaxis_title="Number of Posts",
            showlegend=False
        )
        
        return fig
