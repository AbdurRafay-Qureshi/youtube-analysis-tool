# config/api_manager.py
# Centralized API key and quota management

import streamlit as st
from datetime import datetime, timedelta
import json
import os


class APIManager:
    """Manage API keys and usage quotas"""
    
    def __init__(self):
        self.quota_file = ".quota_tracker.json"
        self.reset_quota_if_needed()
    
    
    def get_youtube_key(self, user_key=None):
        """
        Get YouTube API key (your key or user's).
        
        Args:
            user_key (str): Optional user-provided key
        
        Returns:
            str: API key to use
        """
        if user_key:
            # User provided their own key
            return user_key
        
        # Use your key from secrets
        if "youtube" in st.secrets:
            key = st.secrets["youtube"]["api_key"]
            
            # Check if quota available
            if self.check_quota("youtube"):
                self.increment_usage("youtube")
                return key
            else:
                st.error("⚠️ Daily quota limit reached. Please try again tomorrow or provide your own API key.")
                return None
        
        # No key available
        st.error("❌ No YouTube API key configured. Please provide your own.")
        return None
    
    
    def get_reddit_credentials(self, user_credentials=None):
        """
        Get Reddit API credentials (your credentials or user's).
        
        Args:
            user_credentials (dict): Optional user-provided credentials
                {"client_id": "...", "client_secret": "...", "user_agent": "..."}
        
        Returns:
            dict: Credentials to use
        """
        if user_credentials and user_credentials.get("client_id"):
            # User provided their own credentials
            return user_credentials
        
        # Use your credentials from secrets
        if "reddit" in st.secrets:
            creds = {
                "client_id": st.secrets["reddit"]["client_id"],
                "client_secret": st.secrets["reddit"]["client_secret"],
                "user_agent": st.secrets["reddit"]["user_agent"]
            }
            
            # Check if quota available
            if self.check_quota("reddit"):
                self.increment_usage("reddit")
                return creds
            else:
                st.error("⚠️ Daily quota limit reached. Please try again tomorrow or provide your own credentials.")
                return None
        
        # No credentials available
        st.error("❌ No Reddit credentials configured. Please provide your own.")
        return None
    
    
    def check_quota(self, platform):
        """Check if quota is available for platform."""
        usage = self.load_usage()
        today = datetime.now().date().isoformat()
        
        if today not in usage:
            return True
        
        platform_usage = usage[today].get(platform, 0)
        max_daily = st.secrets.get("quota", {}).get("max_daily_requests", 100)
        
        return platform_usage < max_daily
    
    
    def increment_usage(self, platform):
        """Increment usage counter for platform."""
        usage = self.load_usage()
        today = datetime.now().date().isoformat()
        
        if today not in usage:
            usage[today] = {}
        
        if platform not in usage[today]:
            usage[today][platform] = 0
        
        usage[today][platform] += 1
        
        self.save_usage(usage)
    
    
    def get_remaining_quota(self, platform):
        """Get remaining quota for today."""
        usage = self.load_usage()
        today = datetime.now().date().isoformat()
        
        platform_usage = usage.get(today, {}).get(platform, 0)
        max_daily = st.secrets.get("quota", {}).get("max_daily_requests", 100)
        
        return max_daily - platform_usage
    
    
    def reset_quota_if_needed(self):
        """Reset quota if new day."""
        usage = self.load_usage()
        today = datetime.now().date().isoformat()
        
        # Remove old dates
        usage = {k: v for k, v in usage.items() if k == today}
        
        self.save_usage(usage)
    
    
    def load_usage(self):
        """Load usage data from file."""
        if not os.path.exists(self.quota_file):
            return {}
        
        try:
            with open(self.quota_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    
    def save_usage(self, usage):
        """Save usage data to file."""
        with open(self.quota_file, 'w') as f:
            json.dump(usage, f)
    
    
    def show_quota_info(self, platform):
        """Display quota information in sidebar."""
        remaining = self.get_remaining_quota(platform)
        max_daily = st.secrets.get("quota", {}).get("max_daily_requests", 100)
        
        percentage = (remaining / max_daily) * 100
        
        if percentage > 50:
            color = "#10B981"  # Green
            emoji = "✅"
        elif percentage > 20:
            color = "#F59E0B"  # Yellow
            emoji = "⚠️"
        else:
            color = "#EF4444"  # Red
            emoji = "🔴"
        
        st.sidebar.markdown(f"""
        <div style="
            background: rgba(37, 99, 235, 0.1);
            border: 1px solid {color};
            border-radius: 8px;
            padding: 10px;
            margin: 10px 0;
        ">
            <p style="color: #E2E8F0; font-size: 12px; margin: 0;">
                {emoji} Daily Quota Remaining
            </p>
            <p style="color: {color}; font-size: 18px; font-weight: 600; margin: 5px 0 0 0;">
                {remaining} / {max_daily}
            </p>
        </div>
        """, unsafe_allow_html=True)


# Global instance
api_manager = APIManager()
