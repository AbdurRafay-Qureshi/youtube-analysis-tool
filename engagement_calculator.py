# engagement_calculator.py
# Advanced Engagement Rate Calculator with 30-day comparison

import pandas as pd
from datetime import datetime, timezone, timedelta


class EngagementCalculator:
    """Calculate accurate engagement metrics with historical comparison"""
    
    def __init__(self, df):
        """
        Initialize with video dataframe
        Args:
            df: DataFrame with columns: upload_date, view_count, like_count, comment_count
        """
        self.df = df.copy()
        self.now = datetime.now(timezone.utc)
    
    def calculate_engagement_rate(self, views, likes, comments):
        """
        Calculate engagement rate using industry-standard formula
        Formula: (Likes + Comments) / Views × 100
        """
        if views == 0:
            return 0.0
        return ((likes + comments) / views * 100)
    
    def get_period_stats(self, start_date, end_date):
        """Get aggregated stats for a specific period"""
        period_df = self.df[
            (self.df['upload_date'] >= start_date) & 
            (self.df['upload_date'] < end_date)
        ]
        
        if period_df.empty:
            return {
                'videos': 0,
                'views': 0,
                'likes': 0,
                'comments': 0,
                'engagement_rate': 0.0
            }
        
        total_views = period_df['view_count'].sum()
        total_likes = period_df['like_count'].sum()
        total_comments = period_df['comment_count'].sum()
        
        return {
            'videos': len(period_df),
            'views': int(total_views),
            'likes': int(total_likes),
            'comments': int(total_comments),
            'engagement_rate': self.calculate_engagement_rate(total_views, total_likes, total_comments)
        }
    
    def get_last_30_days_stats(self):
        """Get stats for the last 30 days"""
        end_date = self.now
        start_date = end_date - timedelta(days=30)
        return self.get_period_stats(start_date, end_date)
    
    def get_previous_30_days_stats(self):
        """Get stats for the 30 days before the last 30 days (31-60 days ago)"""
        end_date = self.now - timedelta(days=30)
        start_date = end_date - timedelta(days=30)
        return self.get_period_stats(start_date, end_date)
    
    def calculate_change_percentage(self, current, previous):
        """Calculate percentage change between two values"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return ((current - previous) / previous * 100)
    
    def get_engagement_comparison(self):
        """
        Get comprehensive engagement comparison between periods
        Returns: dict with current stats, previous stats, and changes
        """
        current = self.get_last_30_days_stats()
        previous = self.get_previous_30_days_stats()
        
        # Calculate changes
        engagement_change = self.calculate_change_percentage(
            current['engagement_rate'], 
            previous['engagement_rate']
        )
        
        views_change = self.calculate_change_percentage(
            current['views'], 
            previous['views']
        )
        
        videos_change = self.calculate_change_percentage(
            current['videos'], 
            previous['videos']
        )
        
        return {
            'current_period': current,
            'previous_period': previous,
            'engagement_change': engagement_change,
            'views_change': views_change,
            'videos_change': videos_change,
            'is_improving': engagement_change > 0
        }
    
    def get_overall_engagement(self):
        """Get overall channel engagement rate (all-time)"""
        total_views = self.df['view_count'].sum()
        total_likes = self.df['like_count'].sum()
        total_comments = self.df['comment_count'].sum()
        
        return {
            'total_videos': len(self.df),
            'total_views': int(total_views),
            'total_likes': int(total_likes),
            'total_comments': int(total_comments),
            'engagement_rate': self.calculate_engagement_rate(total_views, total_likes, total_comments)
        }
    
    def get_engagement_trend(self, days=7):
        """
        Get engagement rate trend over the last N days
        Returns list of daily engagement rates
        """
        trends = []
        
        for i in range(days):
            end_date = self.now - timedelta(days=i)
            start_date = end_date - timedelta(days=1)
            stats = self.get_period_stats(start_date, end_date)
            
            trends.append({
                'date': start_date.date(),
                'engagement_rate': stats['engagement_rate'],
                'views': stats['views'],
                'videos': stats['videos']
            })
        
        return list(reversed(trends))
    
    def format_change(self, change):
        """Format change percentage with appropriate sign and symbol"""
        if change > 0:
            return f"+{change:.1f}%", True
        elif change < 0:
            return f"{change:.1f}%", False
        else:
            return "0.0%", True
