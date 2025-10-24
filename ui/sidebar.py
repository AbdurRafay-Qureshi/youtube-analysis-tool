# ui/sidebar.py
import streamlit as st

def render_sidebar(sentiment_available=False, vader_available=False, predictive_available=False):
    """Styled selectbox platform selector with blue theme"""
    
    with st.sidebar:
        # Custom CSS for blue-themed dropdown
        st.markdown("""
        <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: rgba(37, 99, 235, 0.1);
            border: 1px solid #2563EB;
            border-radius: 8px;
        }
        
        /* Dropdown menu styling */
        [data-baseweb="select"] {
            background: #1e293b;
        }
        
        /* Platform labels in dropdown */
        [data-baseweb="menu"] {
            background: #1e293b !important;
            border: 1px solid #2563EB;
        }
        
        [data-baseweb="menu"] li {
            background: #1e293b !important;
            color: #E2E8F0 !important;
        }
        
        [data-baseweb="menu"] li:hover {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div style="margin-bottom: 25px;">
            <h3 style="color: #E2E8F0; font-size: 20px; margin-bottom: 5px;">
                📊 Social Analytics Hub
            </h3>
            <p style="color: #94A3B8; font-size: 12px; margin: 0;">
                Multi-platform analytics dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Platform selector
        platform = st.selectbox(
            "Select Platform",
            ["🎥 YouTube", "🔴 Reddit", "💼 LinkedIn", "👻 Snapchat"],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Route based on selection
        if "YouTube" in platform:
            return render_youtube_config()
        elif "Reddit" in platform:
            return render_reddit_config()
        elif "LinkedIn" in platform:
            return render_linkedin_config()
        else:
            return render_snapchat_config()


# Alias
render_platform_selector = render_sidebar


def render_youtube_config():
    """YouTube configuration"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h4 style="color: #E2E8F0; font-size: 16px; margin-bottom: 15px;">
            ⚙️ Configuration
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        "YouTube API Key",
        type="password",
        key="yt_api_key",
        placeholder="Enter your API key"
    )
    
    channel_input = st.text_input(
        "Channel Identifier",
        placeholder="@channel or URL",
        key="yt_channel"
    )
    
    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    analyze_clicked = st.button(
        "🚀 Analyze Channel",
        use_container_width=True,
        type="primary"
    )
    
    return {
        "platform": "youtube",
        "api_key": api_key,
        "channel_input": channel_input,
        "analyze_clicked": analyze_clicked,
        "fetch_comments": False,
        "max_comments": 100,
        "num_videos_for_comments": 10,
        "enable_predictions": False
    }


def render_reddit_config():
    """Reddit configuration"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h4 style="color: #E2E8F0; font-size: 16px; margin-bottom: 15px;">
            ⚙️ Configuration
        </h4>
    </div>
    """, unsafe_allow_html=True)
    st.info("🚧 Reddit analytics coming soon!")
    return {"platform": "reddit", "analyze_clicked": False}


def render_linkedin_config():
    """LinkedIn configuration"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h4 style="color: #E2E8F0; font-size: 16px; margin-bottom: 15px;">
            ⚙️ Configuration
        </h4>
    </div>
    """, unsafe_allow_html=True)
    st.info("🚧 LinkedIn analytics coming soon!")
    return {"platform": "linkedin", "analyze_clicked": False}


def render_snapchat_config():
    """Snapchat configuration"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h4 style="color: #E2E8F0; font-size: 16px; margin-bottom: 15px;">
            ⚙️ Configuration
        </h4>
    </div>
    """, unsafe_allow_html=True)
    st.info("🚧 Snapchat analytics coming soon!")
    return {"platform": "snapchat", "analyze_clicked": False}
