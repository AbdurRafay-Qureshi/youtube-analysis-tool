# main.py
# This file creates the Streamlit frontend for the YouTube Analysis Tool.

import streamlit as st
import pandas as pd
import plotly.express as px
from youtube import YouTubeChannelAnalyser

# --- Check for optional dependency for trendlines ---
try:
    import statsmodels
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False

# --- Helper Functions ---

def format_large_number(num):
    """Formats a large number into a more readable string (e.g., 1.2M)."""
    if num is None:
        return "N/A"
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def seconds_to_hms(seconds):
    """Converts seconds to a HH:MM:SS string format."""
    if seconds is None:
        return "N/A"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="YouTube Channel Analyzer", layout="wide", page_icon="📊")

st.title("📊 YouTube Channel Data Analysis Tool")
st.markdown("""
    Enter a YouTube Channel URL, ID, or Username along with your YouTube Data API v3 key 
    to get an in-depth analysis of the channel's performance.
""")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("⚙️ Inputs")
    api_key = st.text_input("Enter your YouTube Data API Key", type="password")
    channel_input = st.text_input("Enter YouTube Channel URL, ID, or Username")
    
    if st.button("Analyze Channel", type="primary"):
        if not api_key:
            st.error("🚨 Please enter your YouTube Data API Key.")
        elif not channel_input:
            st.error("🚨 Please enter a YouTube Channel identifier.")
        else:
            try:
                with st.spinner("🔍 Fetching and analyzing channel data... This may take a moment for large channels."):
                    analyzer = YouTubeChannelAnalyser(api_key=api_key)
                    # Store fetched data in session state to prevent re-fetching on widget interaction
                    st.session_state.channel_stats, st.session_state.video_df = analyzer.get_channel_data(channel_input)
            except Exception as e:
                st.session_state.clear() # Clear state on error
                st.error(f"An unexpected error occurred: {e}")

# --- Main Page Display ---
# Only display the main content if data has been successfully fetched and stored in the session state.
if 'channel_stats' in st.session_state and 'video_df' in st.session_state:
    channel_stats = st.session_state.channel_stats
    video_df = st.session_state.video_df

    if channel_stats is None or video_df is None:
        st.error("❌ Could not retrieve data for the channel. Please check the identifier and your API key's quota.")
    else:
        st.success(f"✅ Analysis Complete for **{channel_stats['channel_name']}**!")

        # --- Channel Overview ---
        st.header("📈 Channel Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Subscribers", format_large_number(channel_stats['total_subscribers']))
        col2.metric("Total Views", format_large_number(channel_stats['total_views']))
        col3.metric("Total Videos", format_large_number(channel_stats['total_videos']))
        
        # Calculate overall engagement rate from fetched videos
        total_likes = video_df['like_count'].sum()
        total_comments = video_df['comment_count'].sum()
        total_public_views = video_df['view_count'].sum()
        if total_public_views > 0:
            total_engagement = ((total_likes + total_comments) / total_public_views) * 100
            col4.metric("Public Engagement", f"{total_engagement:.2f}%")
        else:
            col4.metric("Public Engagement", "0%")
        
        # Calculate average views per video
        avg_views = channel_stats['total_views'] / channel_stats['total_videos'] if channel_stats['total_videos'] > 0 else 0
        col5.metric("Avg Views/Video", format_large_number(avg_views))

        st.markdown(f"**Channel Description:** {channel_stats['description']}", unsafe_allow_html=True)

        # --- Tabs for Detailed Analysis ---
        tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Performing Videos", "🕒 Performance Over Time", "📊 Engagement Analysis", "📋 Raw Video Data"])

        if video_df.empty:
            st.warning("📊 Channel stats loaded, but no public videos were found to analyze.")
        else:
            # Create a formatted date column for cleaner tooltips
            video_df['formatted_date'] = video_df['upload_date'].dt.strftime('%b %d, %Y')
            
            with tab1:
                st.subheader("Top 10 Videos")
                
                # Use a function to format the options for the selectbox for better readability
                sort_options = ["view_count", "like_count", "comment_count", "engagement_rate"]
                sort_by = st.selectbox(
                    "Sort top videos by:", 
                    options=sort_options,
                    format_func=lambda x: x.replace('_', ' ').title(), # This makes the labels pretty
                    key="top10_sort"
                )
                
                top_10_videos = video_df.sort_values(by=sort_by, ascending=False).head(10)
                
                fig_top10 = px.bar(
                    top_10_videos,
                    x='title',
                    y=sort_by,
                    title=f'Top 10 Videos by {sort_by.replace("_", " ").title()}',
                    custom_data=['view_count', 'like_count', 'comment_count', 'formatted_date']
                )
                
                # Update hover template for a cleaner look
                fig_top10.update_traces(
                    hovertemplate="""
                    <b>%{x}</b><br><br>
                    Views: %{customdata[0]:,}<br>
                    Likes: %{customdata[1]:,}<br>
                    Comments: %{customdata[2]:,}<br>
                    Published: %{customdata[3]}
                    <extra></extra>
                    """
                )
                
                fig_top10.update_layout(
                    xaxis_title="Video Title",
                    yaxis_title=sort_by.replace('_', ' ').title(),
                    xaxis={'categoryorder':'total descending'}
                )
                st.plotly_chart(fig_top10, use_container_width=True)

            with tab2:
                st.subheader("Performance Trends")
                
                fig_views_time = px.line(
                    video_df.sort_values('upload_date'),
                    x='upload_date',
                    y='view_count',
                    title='Video Views Over Time',
                    custom_data=['title', 'like_count', 'comment_count']
                )

                # Update hover template for the line chart
                fig_views_time.update_traces(
                    hovertemplate="""
                    <b>%{customdata[0]}</b><br><br>
                    Views: %{y:,}<br>
                    Likes: %{customdata[1]:,}<br>
                    Comments: %{customdata[2]:,}<br>
                    Published: %{x|%b %d, %Y}
                    <extra></extra>
                    """
                )
                fig_views_time.update_layout(xaxis_title="Upload Date", yaxis_title="Views")
                st.plotly_chart(fig_views_time, use_container_width=True)
                
                st.subheader("Upload Schedule Analysis")
                col_day, col_hour = st.columns(2)
                
                day_counts = video_df['publish_day'].value_counts().reindex(
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                )
                fig_day = px.bar(day_counts, title="Uploads by Day of the Week", labels={'index': 'Day', 'value': 'Number of Videos'})
                col_day.plotly_chart(fig_day, use_container_width=True)
                
                hour_counts = video_df['publish_hour'].value_counts().sort_index()
                fig_hour = px.bar(hour_counts, title="Uploads by Hour of the Day (UTC)", labels={'index': 'Hour', 'value': 'Number of Videos'})
                col_hour.plotly_chart(fig_hour, use_container_width=True)

            with tab3:
                st.subheader("Engagement & Content Analysis")
                
                # Add formatted duration for tooltip
                video_df['formatted_duration'] = video_df['duration_seconds'].apply(seconds_to_hms)
                
                scatter_params = {
                    'data_frame': video_df,
                    'x': 'duration_seconds',
                    'y': 'view_count',
                    'title': 'Video Duration vs. View Count',
                    'labels': {'duration_seconds': 'Duration (seconds)', 'view_count': 'Views'},
                    'color': 'engagement_rate',
                    'color_continuous_scale': px.colors.sequential.Viridis,
                    'custom_data': ['title', 'formatted_duration', 'engagement_rate']
                }
                if STATSMODELS_AVAILABLE:
                    scatter_params['trendline'] = 'ols'
                else:
                    st.info("Note: The trendline feature requires the 'statsmodels' library. Please install it (`pip install statsmodels`) to see the trendline.", icon="ℹ️")

                fig_corr = px.scatter(**scatter_params)

                # Update hover template for the scatter plot
                fig_corr.update_traces(
                    hovertemplate="""
                    <b>%{customdata[0]}</b><br><br>
                    Views: %{y:,}<br>
                    Duration: %{customdata[1]}<br>
                    Engagement: %{customdata[2]:.2f}%
                    <extra></extra>
                    """
                )
                st.plotly_chart(fig_corr, use_container_width=True)
                
                fig_dist = px.histogram(
                    video_df, x='engagement_rate', title='Distribution of Engagement Rate Across Videos',
                    nbins=30, labels={'engagement_rate': 'Engagement Rate (%)'}
                )
                st.plotly_chart(fig_dist, use_container_width=True)

            with tab4:
                st.subheader("Complete Video Dataset")
                display_df = video_df.copy()
                display_df['duration'] = display_df['duration_seconds'].apply(seconds_to_hms)
                display_df['upload_date'] = display_df['upload_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
                display_df = display_df[['title', 'upload_date', 'view_count', 'like_count', 'comment_count', 'engagement_rate', 'duration']]
                st.dataframe(display_df, use_container_width=True)
                
                csv = video_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data as CSV",
                    data=csv,
                    file_name=f"{channel_stats.get('channel_name', 'channel')}_video_data.csv",
                    mime='text/csv',
                )

