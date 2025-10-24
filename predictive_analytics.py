# predictive_analytics.py
# Machine learning module for predictions and forecasting

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import streamlit as st


class PredictiveAnalytics:
    """Machine learning predictions for YouTube performance"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_importance = None
    
    def prepare_features(self, df):
        """Prepare features for machine learning"""
        df_ml = df.copy()
        
        # Time-based features
        df_ml['hour'] = df_ml['upload_date'].dt.hour
        df_ml['day_of_week'] = df_ml['upload_date'].dt.dayofweek
        df_ml['day_of_month'] = df_ml['upload_date'].dt.day
        df_ml['month'] = df_ml['upload_date'].dt.month
        df_ml['year'] = df_ml['upload_date'].dt.year
        df_ml['is_weekend'] = (df_ml['day_of_week'] >= 5).astype(int)
        
        # Video features
        df_ml['duration_minutes'] = df_ml['duration_seconds'] / 60
        df_ml['title_length'] = df_ml['title'].str.len()
        df_ml['has_uppercase'] = df_ml['title'].str.contains(r'[A-Z]{2,}').astype(int)
        
        # Lag features (if enough data)
        if len(df_ml) > 5:
            df_ml['prev_video_views'] = df_ml['view_count'].shift(1).fillna(0)
            df_ml['avg_last_3_views'] = df_ml['view_count'].rolling(window=3, min_periods=1).mean()
        
        return df_ml
    
    def train_view_predictor(self, df, target='view_count'):
        """Train model to predict video views"""
        df_ml = self.prepare_features(df)
        
        # Select features
        feature_cols = [
            'duration_seconds', 'hour', 'day_of_week', 'month',
            'is_weekend', 'title_length', 'has_uppercase'
        ]
        
        # Add lag features if available
        if 'prev_video_views' in df_ml.columns:
            feature_cols.extend(['prev_video_views', 'avg_last_3_views'])
        
        # Remove rows with NaN
        df_clean = df_ml[feature_cols + [target]].dropna()
        
        if len(df_clean) < 10:
            return None, "Not enough data for training (need at least 10 videos)"
        
        X = df_clean[feature_cols]
        y = df_clean[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train multiple models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
        }
        
        results = {}
        
        for name, model in models.items():
            # Train
            if name == 'Linear Regression':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
            # Evaluate
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            results[name] = {
                'model': model,
                'r2': r2,
                'mae': mae,
                'rmse': rmse,
                'predictions': y_pred,
                'actual': y_test
            }
        
        # Get feature importance from best tree-based model
        best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
        if best_model_name in ['Random Forest', 'Gradient Boosting']:
            self.feature_importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': results[best_model_name]['model'].feature_importances_
            }).sort_values('importance', ascending=False)
        
        self.models = results
        return results, None
    
    def predict_next_video_views(self, df, next_video_params):
        """Predict views for next video based on parameters"""
        if 'Random Forest' not in self.models:
            return None
        
        model = self.models['Random Forest']['model']
        
        # Prepare features for new video
        features = {
            'duration_seconds': next_video_params.get('duration', 600),
            'hour': next_video_params.get('hour', 12),
            'day_of_week': next_video_params.get('day_of_week', 0),
            'month': next_video_params.get('month', 1),
            'is_weekend': 1 if next_video_params.get('day_of_week', 0) >= 5 else 0,
            'title_length': next_video_params.get('title_length', 50),
            'has_uppercase': next_video_params.get('has_uppercase', 0)
        }
        
        # Add lag features if model was trained with them
        if 'prev_video_views' in self.feature_importance['feature'].values:
            latest_views = df['view_count'].iloc[-1] if not df.empty else 0
            features['prev_video_views'] = latest_views
            features['avg_last_3_views'] = df['view_count'].tail(3).mean() if len(df) >= 3 else latest_views
        
        X_new = pd.DataFrame([features])
        prediction = model.predict(X_new)[0]
        
        return max(0, int(prediction))
    
    def forecast_channel_growth(self, df, days_ahead=30):
        """Forecast channel growth using time series analysis"""
        df_sorted = df.sort_values('upload_date')
        
        # Aggregate by date
        daily_views = df_sorted.groupby(df_sorted['upload_date'].dt.date)['view_count'].sum()
        
        if len(daily_views) < 7:
            return None, "Not enough historical data for forecasting"
        
        # Simple exponential smoothing
        alpha = 0.3
        forecast = []
        last_value = daily_views.iloc[-1]
        
        for i in range(days_ahead):
            forecast.append(last_value)
            # Simple persistence model with slight trend
            trend = (daily_views.iloc[-1] - daily_views.iloc[0]) / len(daily_views)
            last_value = last_value + trend
        
        # Create forecast dataframe
        last_date = pd.to_datetime(daily_views.index[-1])
        forecast_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecasted_views': forecast
        })
        
        return forecast_df, None
    
    def analyze_optimal_upload_time(self, df):
        """Analyze best time to upload videos"""
        if df.empty:
            return None
        
        # Group by hour and day of week
        hour_performance = df.groupby('publish_hour').agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'title': 'count'
        }).rename(columns={'title': 'video_count'})
        
        day_performance = df.groupby('publish_day').agg({
            'view_count': 'mean',
            'engagement_rate': 'mean',
            'title': 'count'
        }).rename(columns={'title': 'video_count'})
        
        # Find optimal time
        best_hour = hour_performance['view_count'].idxmax()
        best_day = day_performance['view_count'].idxmax()
        
        return {
            'best_hour': best_hour,
            'best_day': best_day,
            'hour_performance': hour_performance,
            'day_performance': day_performance
        }
    
    def calculate_video_score(self, df):
        """Calculate a comprehensive performance score for each video"""
        df_scored = df.copy()
        
        # Normalize metrics to 0-100 scale
        for col in ['view_count', 'like_count', 'comment_count', 'engagement_rate']:
            if col in df_scored.columns:
                min_val = df_scored[col].min()
                max_val = df_scored[col].max()
                if max_val > min_val:
                    df_scored[f'{col}_normalized'] = (
                        (df_scored[col] - min_val) / (max_val - min_val) * 100
                    )
                else:
                    df_scored[f'{col}_normalized'] = 50
        
        # Calculate weighted score
        df_scored['performance_score'] = (
            df_scored['view_count_normalized'] * 0.4 +
            df_scored['like_count_normalized'] * 0.3 +
            df_scored['comment_count_normalized'] * 0.2 +
            df_scored['engagement_rate_normalized'] * 0.1
        )
        
        # Categorize
        df_scored['performance_tier'] = pd.cut(
            df_scored['performance_score'],
            bins=[0, 25, 50, 75, 100],
            labels=['Poor', 'Fair', 'Good', 'Excellent']
        )
        
        return df_scored
