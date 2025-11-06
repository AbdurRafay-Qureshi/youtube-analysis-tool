# main.py
# Multi-Platform Analytics Dashboard (YouTube + Reddit)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tabs import render_top_videos_tab, render_upload_schedule_tab
from tabs import render_top_videos_tab, render_upload_schedule_tab, render_insights_tab
from youtube import YouTubeChannelAnalyser
from engagement_calculator import EngagementCalculator

# UI layer
from ui.styles import css as ui_css, plotly_layout
from ui.components import kpi, chart_card, end_card, section, info_card
from ui.sidebar import render_sidebar

# Quota management
try:
    from config.quota_manager import quota_manager
    QUOTA_ENABLED = True
except ImportError:
    QUOTA_ENABLED = False
    print("⚠️ Running without quota limits")

# Optional modules
try:
    from advanced_visualizer import AdvancedVisualizer
    ADV_VIZ_AVAILABLE = True
except ImportError:
    ADV_VIZ_AVAILABLE = False

try:
    from sentiment_analyzer import SentimentAnalyzer
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False

try:
    from predictive_analytics import PredictiveAnalytics
    PREDICTIVE_AVAILABLE = True
except ImportError:
    PREDICTIVE_AVAILABLE = False

try:
    import statsmodels
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False


# --- Helpers ---
def format_large_number(num):
    if num is None:
        return "N/A"
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return f"{num:,}"


def format_subscribers(num):
    """Format subscriber count with K/M suffix"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.0f}K"
    else:
        return f"{num:,}"


def seconds_to_hms(seconds):
    if seconds is None:
        return "N/A"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# --- Page config & theme ---
st.set_page_config(
    page_title="Social Analytics Hub",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)
st.markdown(ui_css(), unsafe_allow_html=True)


# --- Sidebar ---
config = render_sidebar(SENTIMENT_AVAILABLE, VADER_AVAILABLE, PREDICTIVE_AVAILABLE)


# ==================== ANALYZE ACTION - PLATFORM-AWARE ====================
if config["analyze_clicked"]:
    # Check which platform
    if config["platform"] == "youtube":
        # YouTube analysis
        if not config["channel_input"]:
            st.error("⚠️ Please enter channel identifier")
        else:
            # Check quota
            if QUOTA_ENABLED and not quota_manager.can_make_request("youtube"):
                st.error("❌ Daily quota limit reached! Please try again tomorrow.")
                st.info("💡 Tip: The quota resets at midnight UTC (5:00 AM PKT)")
            else:
                try:
                    with st.spinner("🔄 Analyzing YouTube channel..."):
                        # Get API key from secrets
                        api_key = st.secrets["youtube"]["api_key"]
                        
                        # Create analyzer
                        analyzer = YouTubeChannelAnalyser(api_key=api_key)
                        
                        # Fetch data
                        st.session_state.channel_stats, st.session_state.video_df = analyzer.get_channel_data(
                            config["channel_input"]
                        )
                        
                        # Increment quota
                        if QUOTA_ENABLED:
                            quota_manager.increment_usage("youtube")
                        
                        # Store in session state
                        st.session_state.analyzer = analyzer
                        st.session_state.fetch_comments = config["fetch_comments"]
                        st.session_state.max_comments = config["max_comments"]
                        st.session_state.num_videos_for_comments = config["num_videos_for_comments"]
                        st.session_state.enable_predictions = config["enable_predictions"]
                        st.session_state.platform = "youtube"
                        
                        st.success("✅ Channel analyzed successfully!")
                        st.rerun()
                
                except Exception as e:
                    st.session_state.clear()
                    st.error(f"❌ Error: {str(e)}")
    
    elif config["platform"] == "reddit":
        # Reddit analysis
        if not config["identifier"]:
            st.error("⚠️ Please enter a subreddit or username")
        else:
            # Check quota
            if QUOTA_ENABLED and not quota_manager.can_make_request("reddit"):
                st.error("❌ Daily quota limit reached! Please try again tomorrow.")
                st.info("💡 Tip: The quota resets at midnight UTC (5:00 AM PKT)")
            else:
                try:
                    with st.spinner(f"🔄 Analyzing Reddit {config['identifier_type']}..."):
                        # Get credentials from secrets
                        client_id = st.secrets["reddit"]["client_id"]
                        client_secret = st.secrets["reddit"]["client_secret"]
                        user_agent = st.secrets["reddit"]["user_agent"]
                        
                        # Import reddit analyzer
                        from reddit import RedditAnalyser
                        
                        # Create analyzer
                        reddit_analyzer = RedditAnalyser(client_id, client_secret, user_agent)
                        
                        # Analyze based on type
                        if config["identifier_type"] == "subreddit":
                            reddit_data = reddit_analyzer.analyze_subreddit(
                                config["identifier"],
                                limit=config["post_limit"]
                            )
                        else:
                            reddit_data = reddit_analyzer.analyze_user(
                                config["identifier"],
                                limit=config["post_limit"]
                            )
                        
                        # Increment quota
                        if QUOTA_ENABLED:
                            quota_manager.increment_usage("reddit")
                        
                        # Store in session state
                        st.session_state.reddit_data = reddit_data
                        st.session_state.platform = "reddit"
                        
                        st.success(f"✅ {config['identifier_type'].title()} analyzed successfully!")
                        st.rerun()
                
                except ImportError:
                    st.error("❌ Reddit module not found. Please ensure reddit.py exists.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)


# ==================== DISPLAY: YOUTUBE ====================
if "channel_stats" in st.session_state and st.session_state.get("platform") == "youtube":
    stats = st.session_state.channel_stats
    df_original = st.session_state.video_df.copy()

    if stats is None or df_original is None:
        st.error("❌ Could not retrieve channel data")
    else:
        # Header
        section(
            "YouTube Analytics Dashboard",
            f"Professional analytics for {stats['channel_name']}",
        )

        # Filters - FUNCTIONAL
        d1, d2, d3, _ = st.columns([1, 1, 1, 2])
        with d1:
            start_date = st.date_input("Start Date", key="start_date", value=df_original["upload_date"].min().date())
        with d2:
            end_date = st.date_input("End Date", key="end_date", value=df_original["upload_date"].max().date())
        with d3:
            category_filter = st.selectbox(
                "Category", 
                ["All Categories", "Top Performing", "Recent"],
                key="category_filter"
            )
        
        # Apply filters to working dataframe
        df = df_original.copy()
        
        # Date filter
        if start_date and end_date:
            df = df[
                (df["upload_date"].dt.date >= start_date) & 
                (df["upload_date"].dt.date <= end_date)
            ]
        
        # Category filter
        if category_filter == "Top Performing":
            threshold = df["view_count"].quantile(0.75)
            df = df[df["view_count"] >= threshold]
        elif category_filter == "Recent":
            recent_date = df["upload_date"].max() - pd.Timedelta(days=30)
            df = df[df["upload_date"] >= recent_date]

        st.markdown("")

        # ============= FIXED: USE ACTUAL API STATS =============
        
        # Get ACTUAL channel stats from YouTube API
        total_videos_channel = stats['total_videos']
        total_views_channel = stats['total_views']
        total_subscribers = stats['total_subscribers']
        
        # Calculate stats from FETCHED videos only
        total_likes_fetched = df_original['like_count'].sum()
        total_comments_fetched = df_original['comment_count'].sum()
        total_views_fetched = df_original['view_count'].sum()
        fetched_count = len(df_original)
        
        # Calculate engagement rate
        if total_views_channel > 0:
            engagement_rate_calculated = ((total_likes_fetched + total_comments_fetched) / total_views_channel) * 100
        else:
            engagement_rate_calculated = 0.0
        
        # Get 30-day comparison
        eng_calc = EngagementCalculator(df_original)
        engagement_comparison = eng_calc.get_engagement_comparison()
        
        engagement_change_text, engagement_is_positive = eng_calc.format_change(engagement_comparison['engagement_change'])
        views_change_text, views_is_positive = eng_calc.format_change(engagement_comparison['views_change'])
        
        # Calculate coverage
        coverage_percent = (fetched_count / total_videos_channel * 100) if total_videos_channel > 0 else 0
        
        if coverage_percent < 95:
            st.warning(f"⚠️ Showing data for {fetched_count} of {total_videos_channel} videos ({coverage_percent:.1f}% coverage).")

        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi("Subscribers", format_subscribers(total_subscribers), "Official count")
        with c2:
            kpi("Total Views", f"{total_views_channel:,}", "Official channel total")
        with c3:
            kpi("Total Videos", f"{total_videos_channel:,}", f"{fetched_count} analyzed")
        with c4:
            kpi("Engagement Rate", f"{engagement_rate_calculated:.2f}%", f"From {fetched_count} videos")

        st.markdown("")

        # Prepare data for charts
        if not df.empty:
            df["formatted_date"] = df["upload_date"].dt.strftime("%b %d, %Y")
            df["formatted_duration"] = df["duration_seconds"].apply(seconds_to_hms)

        # Charts
        left, right = st.columns([1, 1])

        with left:
            cont = chart_card("Performance Over Time")
            with cont:
                dsort = df.sort_values("upload_date")
                
                hover_text = []
                for idx, row in dsort.iterrows():
                    hover_text.append(
                        f"<b>{row['title'][:60]}...</b><br>" +
                        f"<br>📅 Date: {row['formatted_date']}<br>" +
                        f"👁️ Views: {row['view_count']:,}<br>" +
                        f"👍 Likes: {row['like_count']:,}<br>" +
                        f"💬 Comments: {row['comment_count']:,}<br>" +
                        f"📊 Engagement: {row['engagement_rate']:.2f}%<br>" +
                        f"⏱️ Duration: {row['formatted_duration']}"
                    )
                
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=dsort["upload_date"],
                        y=dsort["view_count"],
                        mode="lines+markers",
                        name="Views",
                        line=dict(color="#2563EB", width=2.5),
                        marker=dict(size=6, color="#2563EB"),
                        text=hover_text,
                        hovertemplate='%{text}<extra></extra>',
                    )
                )
                fig.update_layout(**plotly_layout(), height=400, hovermode='closest')
                st.plotly_chart(fig, use_container_width=True, key="chart_trend")
            end_card()

        with right:
            cont = chart_card("Engagement Breakdown")
            with cont:
                total_engagement = total_likes_fetched + total_comments_fetched
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #033E6B 0%, #0D2956 100%); border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(3,62,107,0.25);">
                    <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">👁️ VIEWS</div>
                    <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{total_views_fetched:,}</div>
                    <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(total_views_fetched / total_views_channel * 100):.1f}% of channel total</div>
                </div>
                <div style="background: linear-gradient(135deg, #2587C8 0%, #156CA5 100%); border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(37,135,200,0.25);">
                    <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">👍 LIKES</div>
                    <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{total_likes_fetched:,}</div>
                    <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(total_likes_fetched / total_engagement * 100):.1f}% of engagement</div>
                </div>
                <div style="background: linear-gradient(135deg, #7CC0E0 0%, #B6DFF1 100%); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(124,192,224,0.25);">
                    <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">💬 COMMENTS</div>
                    <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{total_comments_fetched:,}</div>
                    <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(total_comments_fetched / total_engagement * 100):.1f}% of engagement</div>
                </div>
                """, unsafe_allow_html=True)
            end_card()

        st.markdown("")

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Top Videos", "Upload Schedule", "Insights", "Data Table"])

        with tab1:
            render_top_videos_tab(df)

        with tab2:
            render_upload_schedule_tab(df)

        with tab3:
            render_insights_tab(df, stats)

        with tab4:
            cont = chart_card("Dataset")
            
            tbl = df.copy()
            tbl["Duration"] = tbl["duration_seconds"].apply(seconds_to_hms)
            tbl["Upload Date"] = tbl["upload_date"].dt.strftime("%Y-%m-%d %H:%M")
            
            display_tbl = tbl[[
                "title", "Upload Date", "view_count", "like_count", 
                "comment_count", "engagement_rate", "Duration"
            ]].copy()
            
            display_tbl.columns = [
                "Title", "Upload Date", "Views", "Likes", 
                "Comments", "Engagement Rate", "Duration"
            ]
            
            html_table = """
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                <div style="max-height: 420px; overflow-y: auto;">
                    <table style="width: 100%; border-collapse: collapse; background: white;">
                        <thead style="background: #F3F4F6; position: sticky; top: 0; z-index: 10;">
                            <tr>
            """
            
            for col in display_tbl.columns:
                width = "30%" if col == "Title" else "10%"
                html_table += f'<th style="padding: 12px 8px; text-align: left; font-size: 13px; font-weight: 600; color: #1F2937; border-bottom: 2px solid #E5E7EB; width: {width};">{col}</th>'
            
            html_table += "</tr></thead><tbody style='background: white;'>"
            
            for idx, row in display_tbl.iterrows():
                html_table += "<tr style='border-bottom: 1px solid #F3F4F6; background: white;' onmouseover=\"this.style.background='#F9FAFB'\" onmouseout=\"this.style.background='white'\">"
                for col in display_tbl.columns:
                    value = row[col]
                    if col == "Engagement Rate":
                        value = f"{value:.2f}%"
                    elif col in ["Views", "Likes", "Comments"]:
                        value = f"{value:,}"
                    
                    text_align = "left" if col == "Title" else "right"
                    html_table += f'<td style="padding: 10px 8px; color: #1F2937; background: white; font-size: 12px; text-align: {text_align};">{value}</td>'
                html_table += "</tr>"
            
            html_table += "</tbody></table></div></div>"
            
            st.markdown(html_table, unsafe_allow_html=True)
            
            st.markdown("---")
            col_export, col_empty = st.columns([1, 3])
            with col_export:
                try:
                    from pdf_exporter import generate_pdf_report
                    
                    if st.button("📄 Download PDF Report", use_container_width=True):
                        with st.spinner("Generating PDF..."):
                            pdf_buffer = generate_pdf_report(df, stats)
                            st.download_button(
                                label="📥 Download PDF",
                                data=pdf_buffer,
                                file_name=f"{stats['channel_name']}_analytics_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                except ImportError:
                    st.info("Install reportlab to enable PDF export: `pip install reportlab`")
            
            end_card()


# ==================== DISPLAY: REDDIT ====================
elif "reddit_data" in st.session_state and st.session_state.get("platform") == "reddit":
    reddit_data = st.session_state.reddit_data
    stats = reddit_data['stats']
    
    # ✅ FIX COLUMN NAMES - Handle all variations
    posts_df = reddit_data['posts'].copy()
    
    # Map Reddit API column names to our expected names
    column_mapping = {
        'score': 'upvotes',
        'comments': 'num_comments'
    }
    
    for old_name, new_name in column_mapping.items():
        if old_name in posts_df.columns and new_name not in posts_df.columns:
            posts_df[new_name] = posts_df[old_name]
    
    # Ensure ALL required columns exist with safe defaults
    default_values = {
        'title': 'No Title',
        'author': 'Unknown',
        'upvotes': 0,
        'num_comments': 0,
        'engagement_rate': 0.0,
        'subreddit': 'Unknown',
        'created_utc': 0
    }
    
    for col, default in default_values.items():
        if col not in posts_df.columns:
            posts_df[col] = default
    
    # Header
    section(
        "Reddit Analytics Dashboard",
        f"Professional analytics for {reddit_data['type']}: r/{reddit_data['name']}" if reddit_data['type'] == 'subreddit' else f"Professional analytics for user: u/{reddit_data['name']}"
    )
    
    st.markdown("")
    
    # KPIs - Different for Subreddit vs User
    if reddit_data['type'] == 'subreddit':
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi("Members", f"{stats.get('members', 0):,}", "Total subscribers")
        with c2:
            kpi("Posts Analyzed", f"{stats.get('posts_analyzed', 0):,}", f"{stats.get('total_posts_fetched', 0)} fetched")
        with c3:
            kpi("Avg Upvotes", f"{stats.get('avg_upvotes', 0):,.1f}", "Per post")
        with c4:
            # ✅ FIX 1: USE CORRECT FIELD - total_engagement_rate
            engagement_display = stats.get('total_engagement_rate', stats.get('avg_engagement_rate', 0))
            kpi("Community Engagement", f"{engagement_display:.2f}%", "Overall activity rate")
    
    else:  # User
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi("Total Karma", f"{stats.get('total_karma', 0):,}", "Post + Comment")
        with c2:
            kpi("Posts", f"{stats.get('posts_analyzed', 0):,}", "Analyzed")
        with c3:
            kpi("Comments", f"{stats.get('comments_analyzed', 0):,}", "Analyzed")
        with c4:
            kpi("Avg Upvotes", f"{stats.get('avg_post_upvotes', 0):,.1f}", "Per post")
    
    st.markdown("")
    
    # Charts
    if not posts_df.empty:
        # Calculate stats
        total_upvotes = int(posts_df['upvotes'].sum())
        total_comments = int(posts_df['num_comments'].sum())
        avg_upvotes = round(posts_df['upvotes'].mean(), 1)
        avg_comments = round(posts_df['num_comments'].mean(), 1)
        top_post_upvotes = int(posts_df['upvotes'].max())
        avg_engagement = round(posts_df['engagement_rate'].mean(), 2)
        
        # TOP ROW: 3 Orange Gradient Cards (Dark to Light)
        top_row = st.columns(3)
        
        with top_row[0]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #C1440E 0%, #FF4500 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(193,68,14,0.3);">
                <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">⬆️ TOTAL UPVOTES</div>
                <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{total_upvotes:,}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Across {len(posts_df)} posts</div>
            </div>
            """, unsafe_allow_html=True)
        
        with top_row[1]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #E25822 0%, #FF6B3D 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(226,88,34,0.3);">
                <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📊 AVG UPVOTES</div>
                <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{avg_upvotes:,.1f}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Per post average</div>
            </div>
            """, unsafe_allow_html=True)
        
        with top_row[2]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FF7F50 0%, #FFA07A 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(255,127,80,0.3);">
                <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">🔥 TOP POST</div>
                <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{top_post_upvotes:,}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Highest upvotes</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        
        # BOTTOM ROW: 3 Blue Gradient Cards (Dark to Light)
        bottom_row = st.columns(3)
        
        with bottom_row[0]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(12,74,110,0.3);">
                <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">💬 TOTAL COMMENTS</div>
                <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{total_comments:,}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Community discussions</div>
            </div>
            """, unsafe_allow_html=True)
        
        with bottom_row[1]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(2,132,199,0.3);">
                <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📝 AVG COMMENTS</div>
                <div style="color: white; font-size: 40px; font-weight: 800; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{avg_comments:,.1f}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Per post average</div>
            </div>
            """, unsafe_allow_html=True)
        
        with bottom_row[2]:
            # Calculate posts per day
            if 'created_utc' in posts_df.columns:
                posts_df['created_date'] = pd.to_datetime(posts_df['created_utc'], unit='s', errors='coerce')
                date_range = (posts_df['created_date'].max() - posts_df['created_date'].min()).days
                posts_per_day = round(len(posts_df) / max(date_range, 1), 1)
            else:
                posts_per_day = 0
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #38BDF8 0%, #7DD3FC 100%); border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(56,189,248,0.3);">
                <div style="color: rgba(255,255,255,0.95); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📅 POSTS PER DAY</div>
                <div style="color: white; font-size: 40px; font-weight: 700; margin-bottom: 6px; font-family: 'Inter', sans-serif; line-height: 1;">{posts_per_day}</div>
                <div style="color: rgba(255,255,255,0.85); font-size: 13px;">Community activity level</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)
        
        # CHART BELOW: Top Posts by Upvotes (Full Width)
        cont = chart_card("Top 20 Posts by Upvotes")
        with cont:
            top_posts = posts_df.nlargest(20, 'upvotes')
            
            # Create color scale based on comments (engagement indicator)
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=top_posts['title'],
                x=top_posts['upvotes'],
                orientation='h',
                marker=dict(
                    color=top_posts['num_comments'],
                    colorscale='Oranges',
                    showscale=True,
                    colorbar=dict(
                        title="Comments",
                        thickness=15,
                        len=0.7
                    ),
                    line=dict(color='rgba(255,255,255,0.2)', width=1)
                ),
                hovertemplate='<b>%{y}</b><br>' +
                              'Upvotes: %{x:,}<br>' +
                              'Comments: %{marker.color:,}<br>' +
                              '<extra></extra>',
                text=top_posts['upvotes'],
                texttemplate='%{text:,}',
                textposition='outside',
                textfont=dict(size=11, color='#1F2937')
            ))
            
            fig.update_layout(
                **plotly_layout(),
                height=550,
                xaxis_title="Upvotes",
                yaxis_title="",
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=40)
            )
            
            fig.update_yaxes(
                categoryorder="total ascending",
                tickfont=dict(size=11),
                tickmode='linear'
            )
            
            fig.update_xaxes(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        end_card()

    
    st.markdown("")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Top Content", "Activity Analysis", "Insights", "Data Table"])
    
    with tab1:
        cont = chart_card("Top 20 Posts")
        with cont:
            posts_df_sorted = posts_df.sort_values('upvotes', ascending=False).head(20).reset_index(drop=True)
            
            # Add rank column
            posts_df_sorted.insert(0, 'Rank', range(1, len(posts_df_sorted) + 1))
            
            # Prepare display dataframe
            display_df = posts_df_sorted[['Rank', 'title', 'upvotes', 'num_comments', 'engagement_rate']].copy()
            display_df.columns = ['#', 'Post Title', 'Upvotes', 'Comments', 'Engagement %']
            
            # Truncate titles
            display_df['Post Title'] = display_df['Post Title'].apply(lambda x: x[:80] + "..." if len(str(x)) > 80 else x)
            
            # Display with styling
            st.dataframe(
                display_df,
                use_container_width=True,
                height=600,
                hide_index=True,
                column_config={
                    "#": st.column_config.NumberColumn(
                        "#",
                        width="small",
                        help="Rank"
                    ),
                    "Post Title": st.column_config.TextColumn(
                        "Post Title",
                        width="large",
                    ),
                    "Upvotes": st.column_config.NumberColumn(
                        "⬆️ Upvotes",
                        width="small",
                        format="%d"
                    ),
                    "Comments": st.column_config.NumberColumn(
                        "💬 Comments",
                        width="small",
                        format="%d"
                    ),
                    "Engagement %": st.column_config.NumberColumn(
                        "📊 Engagement %",
                        width="small",
                        format="%.4f%%"
                    ),
                }
            )
        end_card()
    
    with tab2:
        if reddit_data['type'] == 'subreddit':
            a, b = st.columns(2)
            with a:
                cont = chart_card("Posts by Hour")
                with cont:
                    if 'created_utc' in posts_df.columns:
                        posts_df['hour'] = pd.to_datetime(posts_df['created_utc'], unit='s', errors='coerce').dt.hour
                        hour_counts = posts_df['hour'].value_counts().sort_index()
                        fig = px.line(hour_counts, markers=True)
                        fig.update_traces(line_color="#FF4500", line_width=2.5)
                        fig.update_layout(**plotly_layout(), height=350)
                        st.plotly_chart(fig, use_container_width=True)
                end_card()
            
            with b:
                cont = chart_card("Posts by Day")
                with cont:
                    if 'created_utc' in posts_df.columns:
                        posts_df['day_name'] = pd.to_datetime(posts_df['created_utc'], unit='s', errors='coerce').dt.day_name()
                        day_counts = posts_df['day_name'].value_counts().reindex(
                            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                            fill_value=0
                        )
                        fig = px.bar(day_counts, color=day_counts.values, color_continuous_scale="Oranges")
                        fig.update_layout(**plotly_layout(), height=350)
                        st.plotly_chart(fig, use_container_width=True)
                end_card()
        
        else:  # User
            cont = chart_card("Activity Across Subreddits")
            with cont:
                if 'subreddit' in posts_df.columns:
                    subreddit_counts = posts_df['subreddit'].value_counts().head(10)
                    fig = px.bar(subreddit_counts, orientation='h')
                    fig.update_traces(marker_color="#FF4500")
                    fig.update_layout(**plotly_layout(), height=400)
                    st.plotly_chart(fig, use_container_width=True)
            end_card()
    
    with tab3:
        if not posts_df.empty:
            try:
                from reddit_insights import RedditInsights
                insights = RedditInsights(posts_df, stats)
                
                chart_choice = st.selectbox(
                    "Choose Analysis",
                    [
                        "Engagement Heatmap",
                        "Engagement Distribution",
                        "Posting Timeline",
                        "Top Subreddits" if reddit_data['type'] == 'user' else "Content Type Analysis"
                    ],
                    key="reddit_insights_choice"
                )
                
                cont = chart_card(chart_choice)
                with cont:
                    try:
                        if chart_choice == "Posting Timeline":
                            # ✅ FIX 2: Add warning about sample data
                            st.warning("⚠️ Note: This shows the sample of posts analyzed, not the entire subreddit history")
                            st.markdown("*Distribution of the most recent posts*")
                            fig = insights.posting_timeline()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True)
                        
                        
                        elif chart_choice == "Engagement Heatmap":
                            st.markdown("*See when posts perform best (darker = better)*")
                            # ✅ FIX 3: Add strategy tip
                            st.success("💡 **Strategy Tip:** Post during darker time slots to avoid competition and maximize engagement")
                            fig = insights.engagement_heatmap()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_choice == "Engagement Distribution":
                            st.markdown("*Distribution of upvotes across posts*")
                            fig = insights.engagement_distribution()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif chart_choice == "Top Subreddits":
                            st.markdown("*Your best performing subreddits*")
                            fig = insights.top_subreddits_performance()
                            if fig:
                                fig.update_layout(**plotly_layout())
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("Not enough data for this analysis")
                        
                        else:  # Content Type Analysis
                            st.markdown("*Compare self posts vs links/media*")
                            fig = insights.content_type_analysis()
                            if fig:
                                fig.update_layout(**plotly_layout())
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("Post type data not available")
                    
                    except Exception as e:
                        st.error(f"Error creating chart: {str(e)}")
                end_card()
            except ImportError:
                info_card("Insights", "reddit_insights.py module not found")
        else:
            info_card("Insights", "No data available for analysis")
    
    with tab4:
        cont = chart_card("Raw Data")
        
        # Safely select only existing columns
        if reddit_data['type'] == 'subreddit':
            available_cols = [col for col in ['title', 'author', 'upvotes', 'num_comments'] if col in posts_df.columns]
        else:
            available_cols = [col for col in ['title', 'subreddit', 'upvotes', 'num_comments'] if col in posts_df.columns]
        
        if available_cols:
            display_df = posts_df[available_cols].copy()
            
            # Rename for display
            column_rename_map = {
                'title': 'Title',
                'author': 'Author',
                'subreddit': 'Subreddit',
                'upvotes': 'Upvotes',
                'num_comments': 'Comments'
            }
            display_df.columns = [column_rename_map.get(col, col) for col in available_cols]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=500,
                hide_index=True
            )
        else:
            st.warning("No data columns available to display")
        
        end_card()


# ==================== DEFAULT VIEW ====================
else:
    section("Social Analytics Hub", "Multi-platform analytics for YouTube and Reddit")
    x1, x2, x3 = st.columns(3)
    with x1:
        info_card("🎥 YouTube", "Analyze channels with comprehensive metrics, insights, and performance tracking.")
    with x2:
        info_card("🔴 Reddit", "Track subreddits and users with engagement analytics and posting patterns.")
    with x3:
        info_card("🚀 Get Started", "Select a platform from the sidebar and enter an identifier to begin analysis.")
