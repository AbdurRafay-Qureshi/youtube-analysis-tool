# tabs/data_table.py
import streamlit as st
import pandas as pd
from datetime import datetime


def seconds_to_hms(seconds):
    """Convert seconds to HH:MM:SS format"""
    if pd.isna(seconds):
        return "00:00:00"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def render_data_table(df, stats, channel_name="Analytics"):
    """Render premium modern data table"""
    
    st.markdown("""
        <style>
        .premium-card {
            background: linear-gradient(135deg, rgba(173, 216, 230, 0.12) 0%, rgba(6, 95, 212, 0.05) 100%);
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 20px;
            border: 1px solid rgba(179, 217, 236, 0.3);
        }
        .header-section {
            margin-bottom: 24px;
        }
        .title-main {
            font-size: 22px;
            font-weight: 800;
            color: #1a2332;
            margin: 0;
        }
        .title-sub {
            font-size: 12px;
            color: #6b7c93;
            margin-top: 4px;
            font-weight: 500;
            letter-spacing: 0.3px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .metric-card {
            background: white;
            border: 1px solid #e8ecf1;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        .metric-card:hover {
            border-color: #b3d9ec;
            box-shadow: 0 2px 8px rgba(179, 217, 236, 0.2);
        }
        .metric-value {
            font-size: 20px;
            font-weight: 700;
            color: #065fd4;
            margin-bottom: 4px;
        }
        .metric-label {
            font-size: 11px;
            color: #6b7c93;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }
        .dataframe-wrapper {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e8ecf1;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }
        .export-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .btn-modern {
            background: linear-gradient(135deg, #065fd4 0%, #053fa3 100%);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            font-weight: 600;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            flex: 1;
            min-width: 120px;
        }
        .btn-modern:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(6, 95, 212, 0.3);
        }
        .info-banner {
            background: linear-gradient(135deg, rgba(173, 216, 230, 0.3) 0%, rgba(6, 95, 212, 0.15) 100%);
            border-left: 3px solid #065fd4;
            border-radius: 6px;
            padding: 12px 14px;
            margin-top: 16px;
            font-size: 12px;
            color: #2c3e50;
        }
        </style>
    """, unsafe_allow_html=True)
    
    try:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        # Header
        st.markdown(f"""
            <div class="header-section">
                <p class="title-main">📊 {channel_name} Analytics</p>
                <p class="title-sub">Complete Video Dataset • {len(df)} videos • Updated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Prepare data
        df_clean = df.copy()
        df_clean['Duration'] = df_clean['duration_seconds'].apply(seconds_to_hms)
        df_clean['Upload Date'] = pd.to_datetime(df_clean['upload_date']).dt.strftime('%Y-%m-%d %H:%M')
        
        display_df = df_clean[[
            'title', 'Upload Date', 'view_count', 'like_count',
            'comment_count', 'engagement_rate', 'Duration'
        ]].copy()
        
        display_df.columns = ['Title', 'Date', 'Views', 'Likes', 'Comments', 'Engagement %', 'Duration']
        display_df = display_df.iloc[::-1].reset_index(drop=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(df):,}</div>
                    <div class="metric-label">Videos</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{df['view_count'].sum():,.0f}</div>
                    <div class="metric-label">Total Views</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{df['like_count'].sum():,.0f}</div>
                    <div class="metric-label">Total Likes</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{df['engagement_rate'].mean():.2f}%</div>
                    <div class="metric-label">Avg Engagement</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Format display dataframe
        display_df_styled = display_df.copy()
        display_df_styled['Views'] = display_df_styled['Views'].apply(lambda x: f"{int(x):,}")
        display_df_styled['Likes'] = display_df_styled['Likes'].apply(lambda x: f"{int(x):,}")
        display_df_styled['Comments'] = display_df_styled['Comments'].apply(lambda x: f"{int(x):,}")
        display_df_styled['Engagement %'] = display_df_styled['Engagement %'].apply(lambda x: f"{x:.2f}%")
        
        # Display table
        st.markdown('<div class="dataframe-wrapper">', unsafe_allow_html=True)
        st.dataframe(
            display_df_styled,
            use_container_width=True,
            hide_index=True,
            height=500
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export section
        st.markdown('<div class="export-buttons">', unsafe_allow_html=True)
        
        col_csv, col_excel = st.columns(2)
        
        with col_csv:
            csv_data = display_df_styled.to_csv(index=False)
            st.download_button(
                label="📥 CSV Export",
                data=csv_data,
                file_name=f"{channel_name}_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_excel:
            try:
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    display_df_styled.to_excel(writer, index=False, sheet_name='Data')
                buffer.seek(0)
                st.download_button(
                    label="📊 Excel Export",
                    data=buffer,
                    file_name=f"{channel_name}_analytics_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.info("⚠️ Install openpyxl: `pip install openpyxl`", icon="ℹ️")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Info banner
        st.markdown("""
            <div class="info-banner">
                💡 <strong>Pro Tip:</strong> Sort by clicking column headers. Search using the search box. Export data for offline analysis.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}", icon="❌")
