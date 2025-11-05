# config/quota_manager.py
# Simple quota tracking for free-tier API usage

import streamlit as st
from datetime import datetime, date
import json
import os


class QuotaManager:
    """Track and limit API usage to stay within free tier"""
    
    def __init__(self):
        self.quota_file = ".quota_usage.json"
        self.today = date.today().isoformat()
        self._cleanup_old_data()
    
    
    def can_make_request(self, platform):
        """
        Check if we can make another request today.
        
        Args:
            platform (str): "youtube" or "reddit"
        
        Returns:
            bool: True if quota available
        """
        usage = self._load_usage()
        
        # Get today's usage
        today_usage = usage.get(self.today, {}).get(platform, 0)
        
        # Get limit from secrets
        limit_key = f"{platform}_daily_limit"
        if "limits" in st.secrets and limit_key in st.secrets["limits"]:
            limit = st.secrets["limits"][limit_key]
        else:
            # Default limits
            limit = 50 if platform == "youtube" else 1000
        
        return today_usage < limit
    
    
    def increment_usage(self, platform):
        """Record that we made a request."""
        usage = self._load_usage()
        
        if self.today not in usage:
            usage[self.today] = {}
        
        if platform not in usage[self.today]:
            usage[self.today][platform] = 0
        
        usage[self.today][platform] += 1
        
        self._save_usage(usage)
    
    
    def get_usage_stats(self, platform):
        """
        Get usage statistics for display.
        
        Returns:
            dict: {"used": int, "limit": int, "remaining": int, "percentage": float}
        """
        usage = self._load_usage()
        used = usage.get(self.today, {}).get(platform, 0)
        
        # Get limit from secrets
        limit_key = f"{platform}_daily_limit"
        if "limits" in st.secrets and limit_key in st.secrets["limits"]:
            limit = st.secrets["limits"][limit_key]
        else:
            limit = 50 if platform == "youtube" else 1000
        
        remaining = max(0, limit - used)
        percentage = (used / limit) * 100 if limit > 0 else 0
        
        return {
            "used": used,
            "limit": limit,
            "remaining": remaining,
            "percentage": percentage
        }
    
    
    def show_quota_badge(self, platform):
        """Display quota status badge in sidebar."""
        stats = self.get_usage_stats(platform)
        
        # Determine color based on remaining quota
        if stats["percentage"] < 50:
            color = "#10B981"  # Green
            emoji = "✅"
            status = "Good"
        elif stats["percentage"] < 80:
            color = "#F59E0B"  # Yellow
            emoji = "⚠️"
            status = "Fair"
        else:
            color = "#EF4444"  # Red
            emoji = "🔴"
            status = "Low"
        
        st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
            border: 1px solid {color};
            border-radius: 10px;
            padding: 12px;
            margin: 15px 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: #94A3B8; font-size: 11px; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">
                        Daily Quota
                    </p>
                    <p style="color: #E2E8F0; font-size: 16px; font-weight: 600; margin: 5px 0 0 0;">
                        {stats["remaining"]} / {stats["limit"]}
                    </p>
                </div>
                <div style="text-align: right;">
                    <p style="font-size: 24px; margin: 0;">
                        {emoji}
                    </p>
                    <p style="color: {color}; font-size: 11px; margin: 0; font-weight: 600;">
                        {status}
                    </p>
                </div>
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                height: 6px;
                margin-top: 10px;
                overflow: hidden;
            ">
                <div style="
                    background: {color};
                    height: 100%;
                    width: {stats['percentage']}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    
    def _load_usage(self):
        """Load usage data from file."""
        if not os.path.exists(self.quota_file):
            return {}
        
        try:
            with open(self.quota_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    
    def _save_usage(self, usage):
        """Save usage data to file."""
        try:
            with open(self.quota_file, 'w') as f:
                json.dump(usage, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save quota usage: {e}")
    
    
    def _cleanup_old_data(self):
        """Remove usage data older than 7 days."""
        usage = self._load_usage()
        
        # Keep only last 7 days
        cutoff_date = datetime.now().date()
        dates_to_keep = [(cutoff_date - timedelta(days=i)).isoformat() for i in range(7)]
        
        cleaned_usage = {k: v for k, v in usage.items() if k in dates_to_keep}
        
        if len(cleaned_usage) != len(usage):
            self._save_usage(cleaned_usage)


# Global singleton instance
from datetime import timedelta
quota_manager = QuotaManager()
