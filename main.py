# main.py
# YouTube Analytics Dashboard - FIXED VERSION (Accurate Stats + K/M Formatting)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from youtube import YouTubeChannelAnalyser
from engagement_calculator import EngagementCalculator

# UI layer
from ui.styles import css as ui_css, plotly_layout
from ui.components import kpi, chart_card, end_card, section, info_card
from ui.sidebar import render_sidebar

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
    page_title="YouTube Analytics",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)
st.markdown(ui_css(), unsafe_allow_html=True)

# --- Sidebar ---
config = render_sidebar(SENTIMENT_AVAILABLE, VADER_AVAILABLE, PREDICTIVE_AVAILABLE)

# --- Analyze action ---
if config["analyze_clicked"]:
    if not config["api_key"]:
        st.error("Please enter API key")
    elif not config["channel_input"]:
        st.error("Please enter channel identifier")
    else:
        try:
            with st.spinner("Analyzing..."):
                analyzer = YouTubeChannelAnalyser(api_key=config["api_key"])
                st.session_state.channel_stats, st.session_state.video_df = analyzer.get_channel_data(
                    config["channel_input"]
                )
                st.session_state.analyzer = analyzer
                st.session_state.api_key = config["api_key"]
                st.session_state.fetch_comments = config["fetch_comments"]
                st.session_state.max_comments = config["max_comments"]
                st.session_state.num_videos_for_comments = config["num_videos_for_comments"]
                st.session_state.enable_predictions = config["enable_predictions"]
                st.success("✅ Analysis Complete!")
                st.rerun()
        except Exception as e:
            st.session_state.clear()
            st.error(f"Error: {str(e)}")

# --- Main ---
if "channel_stats" in st.session_state and "video_df" in st.session_state:
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
        total_videos_channel = stats['total_videos']       # ← ACTUAL from API
        total_views_channel = stats['total_views']         # ← ACTUAL from API
        total_subscribers = stats['total_subscribers']     # ← ACTUAL from API
        
        # Calculate stats from FETCHED videos only (for engagement breakdown)
        total_likes_fetched = df_original['like_count'].sum()
        total_comments_fetched = df_original['comment_count'].sum()
        total_views_fetched = df_original['view_count'].sum()
        fetched_count = len(df_original)
        
        # Calculate ACCURATE engagement rate from fetched data
        if total_views_fetched > 0:
            engagement_rate_calculated = ((total_likes_fetched + total_comments_fetched) / total_views_fetched) * 100
        else:
            engagement_rate_calculated = 0.0
        
        # Get 30-day comparison using EngagementCalculator
        eng_calc = EngagementCalculator(df_original)
        engagement_comparison = eng_calc.get_engagement_comparison()
        
        engagement_change_text, engagement_is_positive = eng_calc.format_change(engagement_comparison['engagement_change'])
        views_change_text, views_is_positive = eng_calc.format_change(engagement_comparison['views_change'])
        videos_change_text, videos_is_positive = eng_calc.format_change(engagement_comparison['videos_change'])
        
        # Calculate data coverage
        coverage_percent = (fetched_count / total_videos_channel * 100) if total_videos_channel > 0 else 0
        
        # Show warning if coverage < 95%
        if coverage_percent < 95:
            st.warning(f"⚠️ Showing data for {fetched_count} of {total_videos_channel} videos ({coverage_percent:.1f}% coverage). Some older videos may not be included in analysis.")

        # KPIs - Use ACTUAL API stats with K/M formatting for subscribers
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi("Subscribers", format_subscribers(total_subscribers), "Official count")  # ← FORMATTED WITH K/M
        with c2:
            kpi("Total Views", f"{total_views_channel:,}", views_change_text, positive=views_is_positive)
        with c3:
            kpi("Total Videos", f"{total_videos_channel:,}", f"{fetched_count} analyzed")
        with c4:
            kpi("Engagement Rate", f"{engagement_rate_calculated:.2f}%", engagement_change_text, positive=engagement_is_positive)

        st.markdown("")

        # Prepare data for charts (using filtered df)
        if not df.empty:
            df["formatted_date"] = df["upload_date"].dt.strftime("%b %d, %Y")
            df["formatted_duration"] = df["duration_seconds"].apply(seconds_to_hms)

        # Charts row - ALIGNED WITH EQUAL WIDTH COLUMNS
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
                fig.update_layout(
                    **plotly_layout(), 
                    height=400, 
                    hovermode='closest'
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_trend")
            end_card()

        with right:
            cont = chart_card("Engagement Breakdown")
            with cont:
                # Use FETCHED video stats for engagement breakdown
                total_engagement = total_likes_fetched + total_comments_fetched
                
                # Views Card - Darkest Blue
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #033E6B 0%, #0D2956 100%); border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(3,62,107,0.25);">
                    <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">👁️ VIEWS</div>
                    <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{total_views_fetched:,}</div>
                    <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(total_views_fetched / total_views_channel * 100):.1f}% of channel total</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Likes Card - Medium Blue
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2587C8 0%, #156CA5 100%); border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(37,135,200,0.25);">
                    <div style="color: rgba(255,255,255,0.9); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">👍 LIKES</div>
                    <div style="color: white; font-size: 32px; font-weight: 700; margin-top: 10px; font-family: 'Inter', sans-serif;">{total_likes_fetched:,}</div>
                    <div style="color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px;">{(total_likes_fetched / total_engagement * 100):.1f}% of engagement</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Comments Card - Lightest Blue
                st.markdown(f"""
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
            cont = chart_card("Top 10 by Metric")
            sort_by = st.selectbox(
                "Sort by",
                ["view_count", "like_count", "comment_count", "engagement_rate"],
                format_func=lambda s: s.replace("_", " ").title(),
                key="sort_top",
            )
            top = df.nlargest(10, sort_by)
            
            fig = px.bar(
                top,
                y="title",
                x=sort_by,
                orientation="h",
                color="engagement_rate",
                color_continuous_scale="Blues",
                title=None,
            )
            
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br><br>' +
                              'Views: %{customdata[0]:,}<br>' +
                              'Likes: %{customdata[1]:,}<br>' +
                              'Comments: %{customdata[2]:,}<br>' +
                              'Engagement: %{customdata[3]:.2f}%' +
                              '<extra></extra>',
                customdata=top[['view_count', 'like_count', 'comment_count', 'engagement_rate']].values
            )
            
            fig.update_layout(**plotly_layout(), height=520)
            fig.update_yaxes(categoryorder="total ascending", tickfont=dict(size=10))
            st.plotly_chart(fig, use_container_width=True, key="chart_top10")
            end_card()

        with tab2:
            a, b = st.columns(2)
            with a:
                cont = chart_card("Uploads by Day")
                day_counts = df["publish_day"].value_counts().reindex(
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                )
                fig = px.bar(
                    day_counts, 
                    labels={"index": "Day", "value": "Uploads"}, 
                    color=day_counts.values,
                    color_continuous_scale="Blues"
                )
                fig.update_layout(**plotly_layout(), height=350)
                st.plotly_chart(fig, use_container_width=True, key="chart_day")
                end_card()
            with b:
                cont = chart_card("Uploads by Hour (UTC)")
                hour_counts = df["publish_hour"].value_counts().sort_index()
                fig = px.line(hour_counts, markers=True)
                fig.update_traces(line_color="#2563EB", line_width=2.5)
                fig.update_layout(**plotly_layout(), height=350)
                st.plotly_chart(fig, use_container_width=True, key="chart_hour")
                end_card()

        with tab3:
            if not df.empty:
                from insights import YouTubeInsights
                insights = YouTubeInsights(df, stats)
                
                chart_choice = st.selectbox(
                    "Choose Analysis", 
                    [
                        "Growth Timeline",
                        "Best Performing Days",
                        "Video Length Analysis",
                        "Engagement Heatmap",
                        "Performance Matrix",
                        "Upload Consistency"
                    ],
                    key="insights_choice"
                )
                
                cont = chart_card(chart_choice)
                with cont:
                    try:
                        if chart_choice == "Growth Timeline":
                            st.markdown("*Track your channel's cumulative growth over time*")
                            fig = insights.growth_timeline()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_{chart_choice}")
                        
                        elif chart_choice == "Best Performing Days":
                            st.markdown("*Discover which days get the best results*")
                            fig = insights.best_performing_timeframes()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_{chart_choice}")
                        
                        elif chart_choice == "Video Length Analysis":
                            st.markdown("*Find the optimal video duration for your audience*")
                            fig, df_bins = insights.video_length_performance()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_{chart_choice}")
                            
                            st.markdown("#### 📋 Video Length Breakdown")
                            length_table = df_bins[['title', 'duration_category', 'duration_seconds', 'view_count', 'engagement_rate']].copy()
                            length_table = length_table.sort_values('duration_seconds', ascending=False)
                            display_table = length_table[['title', 'duration_category', 'view_count', 'engagement_rate']].copy()
                            display_table['duration_category'] = display_table['duration_category'].astype(str)
                            display_table.columns = ['Video Title', 'Duration', 'Views', 'Engagement %']
                            
                            st.dataframe(
                                display_table,
                                use_container_width=True,
                                height=300,
                                hide_index=True,
                                column_config={
                                    "Video Title": st.column_config.TextColumn("Video Title", width="large"),
                                    "Duration": st.column_config.TextColumn("Duration", width="small"),
                                    "Views": st.column_config.NumberColumn("Views", format="%d"),
                                    "Engagement %": st.column_config.NumberColumn("Engagement %", format="%.2f%%")
                                }
                            )
                        
                        elif chart_choice == "Engagement Heatmap":
                            st.markdown("*See when your audience is most engaged (darker = better)*")
                            st.info("💡 Tip: Upload when squares are darker for better engagement!")
                            fig = insights.engagement_heatmap()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_{chart_choice}")
                        
                        elif chart_choice == "Performance Matrix":
                            st.markdown("*Identify your star videos and improvement opportunities*")
                            fig = insights.performance_matrix()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_{chart_choice}")
                        
                        else:
                            st.markdown("*Monitor your upload schedule consistency*")
                            st.info("💡 Tip: Lower and more consistent = better for algorithm")
                            fig = insights.consistency_score()
                            fig.update_layout(**plotly_layout())
                            st.plotly_chart(fig, use_container_width=True, key=f"insight_{chart_choice}")
                        
                    except Exception as e:
                        st.error(f"Error creating chart: {str(e)}")
                        st.exception(e)
                end_card()
            else:
                info_card("Insights", "Analyze your content with practical, actionable insights")

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

else:
    section("YouTube Analytics Dashboard", "Professional analytics platform for YouTube creators")
    x1, x2, x3 = st.columns(3)
    with x1:
        info_card("Get Started", "Enter your API key and channel identifier in the sidebar to begin analysis.")
    with x2:
        info_card("Analytics", "Explore KPIs, trends, upload cadence, and engagement breakdowns.")
    with x3:
        info_card("Predictions", "Train models to forecast performance and discover optimal upload times.")
