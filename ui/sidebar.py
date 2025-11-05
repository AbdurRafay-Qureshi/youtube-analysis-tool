# ui/sidebar.py
import streamlit as st

# Import quota manager
try:
    from config.quota_manager import quota_manager
    QUOTA_ENABLED = True
except ImportError:
    QUOTA_ENABLED = False


def render_sidebar(sentiment_available=False, vader_available=False, predictive_available=False):
    """Modern sidebar with gradient theme"""
    
    with st.sidebar:
        # Minimal CSS - only what's needed, won't break dropdown
        st.markdown("""
        <style>
        /* Sidebar gradient background */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #1E293B 60%, #334155 100%) !important;
        }
        
        /* Light text */
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #F1F5F9 !important;
        }
        
        /* Text inputs */
        section[data-testid="stSidebar"] input[type="text"] {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(148, 163, 184, 0.3) !important;
            color: #F1F5F9 !important;
            border-radius: 8px !important;
        }
        
        /* Primary button */
        section[data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown("# 📊 Social Analytics Hub")
        st.markdown("<p style='color: #94A3B8; font-size: 13px; margin-top: -10px;'>Multi-platform analytics dashboard</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Platform selector - NO CSS APPLIED
        platform = st.selectbox(
            "Select Platform",
            ["🎥 YouTube", "🔴 Reddit"],
            key="platform_selector"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Route
        if "YouTube" in platform:
            return render_youtube_config()
        else:
            return render_reddit_config()


def render_youtube_config():
    """YouTube configuration"""
    
    # Quota display
    if QUOTA_ENABLED:
        try:
            quota_data = quota_manager.quota_data
            used = quota_data.get('used', 0)
            total = quota_data.get('total', 100)
            percentage = (used / total * 100) if total > 0 else 0
            
            if percentage < 50:
                color = "#10B981"
                status = "Good"
            elif percentage < 80:
                color = "#F59E0B"
                status = "Fair"
            else:
                color = "#EF4444"
                status = "Critical"
            
            st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 10px; padding: 16px; margin-bottom: 20px;'>
                <div style='color: #94A3B8; font-size: 11px; text-transform: uppercase; margin-bottom: 8px;'>Daily Quota</div>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                    <span style='color: white; font-size: 20px; font-weight: 700;'>{used} / {total}</span>
                    <span style='background: {color}; color: white; padding: 4px 10px; border-radius: 5px; font-size: 11px; font-weight: 600;'>{status}</span>
                </div>
                <div style='background: rgba(15, 23, 42, 0.8); border-radius: 6px; height: 8px; overflow: hidden;'>
                    <div style='background: {color}; height: 100%; width: {percentage}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            pass
    
    channel_input = st.text_input(
        "Channel Identifier",
        placeholder="@channel or URL",
        key="yt_channel"
    )
    
    analyze_clicked = st.button("🚀 Analyze Channel", use_container_width=True, type="primary")
    
    return {
        "platform": "youtube",
        "channel_input": channel_input,
        "analyze_clicked": analyze_clicked,
        "fetch_comments": False,
        "max_comments": 100,
        "num_videos_for_comments": 10,
        "enable_predictions": False
    }


def render_reddit_config():
    """Reddit configuration"""
    st.markdown("### ⚙️ Configuration")
    
    analysis_type = st.radio(
        "Analyze",
        ["📊 Subreddit", "👤 User"],
        horizontal=True,
        key="reddit_type"
    )
    
    if "Subreddit" in analysis_type:
        identifier = st.text_input(
            "Subreddit Name",
            placeholder="r/python",
            key="reddit_id"
        )
        identifier_type = "subreddit"
    else:
        identifier = st.text_input(
            "Username",
            placeholder="u/spez",
            key="reddit_id"
        )
        identifier_type = "user"
    
    with st.expander("Advanced Options"):
        post_limit = st.slider("Posts to Fetch", 50, 500, 200, 50)
    
    analyze_clicked = st.button("🚀 Analyze Reddit", use_container_width=True, type="primary")
    
    return {
        "platform": "reddit",
        "identifier": identifier,
        "identifier_type": identifier_type,
        "post_limit": post_limit if 'post_limit' in locals() else 200,
        "analyze_clicked": analyze_clicked
    }

# Aliases
render_platform_selector = render_sidebar
