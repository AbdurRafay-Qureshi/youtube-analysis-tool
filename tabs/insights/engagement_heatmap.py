# tabs/insights/engagement_heatmap.py
import streamlit as st
import pandas as pd


def render_engagement_heatmap(insights):
    """Render boxy square Engagement Heatmap with hover insights"""
    
    st.markdown("""
        <style>
        .chart-card {
            background: linear-gradient(135deg, rgba(173, 216, 230, 0.15) 0%, rgba(6, 95, 212, 0.08) 100%);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .insight-box {
            background: linear-gradient(135deg, rgba(173, 216, 230, 0.4) 0%, rgba(6, 95, 212, 0.2) 100%);
            border-left: 4px solid #065FD4;
            border-radius: 8px;
            padding: 15px 20px;
            margin-top: 15px;
            font-size: 13px;
            color: #2c3e50;
        }
        .heatmap-wrapper {
            margin-top: 15px;
            margin-bottom: 15px;
        }
        .hour-labels {
            display: flex;
            gap: 5px;
            margin-left: 48px;
            margin-bottom: 8px;
            font-size: 9px;
            font-weight: 600;
            color: #5a6c7d;
            text-align: center;
        }
        .hour-label {
            width: 32px;
            flex-shrink: 0;
        }
        .heatmap-container {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .heatmap-row {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .day-label {
            font-size: 11px;
            font-weight: 700;
            color: #2c3e50;
            width: 40px;
            text-align: right;
            flex-shrink: 0;
        }
        .day-row {
            display: flex;
            gap: 5px;
        }
        .heatmap-cell {
            width: 32px;
            height: 32px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            cursor: pointer;
            position: relative;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            font-weight: 600;
            color: rgba(0, 0, 0, 0.2);
            flex-shrink: 0;
        }
        .heatmap-cell:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(6, 95, 212, 0.3);
            z-index: 10;
        }
        /* BLUE PALETTE */
        .cell-empty { background: #e8f4f8; }
        .cell-1 { background: #b3d9ec; }
        .cell-2 { background: #7ec8e3; }
        .cell-3 { background: #3fa9d8; }
        .cell-4 { background: #2e86de; }
        .cell-5 { background: #065fd4; }
        
        .tooltip-content {
            display: none;
            position: absolute;
            bottom: 120%;
            left: 50%;
            transform: translateX(-50%);
            background: #e8f4f8;
            border: 2px solid #065fd4;
            border-radius: 8px;
            padding: 12px;
            width: 220px;
            font-size: 11px;
            color: #2c3e50;
            z-index: 1000;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            white-space: normal;
            line-height: 1.5;
        }
        .tooltip-content::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -6px;
            border: 6px solid transparent;
            border-top-color: #065fd4;
        }
        .heatmap-cell:hover .tooltip-content {
            display: block;
        }
        .tooltip-title {
            font-weight: 700;
            color: #065fd4;
            margin-bottom: 6px;
            border-bottom: 1px solid #e8ecf1;
            padding-bottom: 6px;
        }
        .tooltip-stat {
            margin: 4px 0;
        }
        .tooltip-stat-label {
            color: #5a6c7d;
            font-size: 10px;
        }
        .tooltip-stat-value {
            color: #2c3e50;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("### 🔥 Engagement Heatmap")
    st.markdown("*See when your audience is most engaged (darker = better)*")
    
    try:
        df = insights.df.copy()
        
        # Extract hour and day
        df['upload_hour'] = pd.to_datetime(df['upload_date']).dt.hour
        df['upload_day'] = pd.to_datetime(df['upload_date']).dt.day_name()
        
        # Create detailed heatmap data
        heatmap_data = df.groupby(['upload_day', 'upload_hour']).agg({
            'engagement_rate': ['mean', 'std'],
            'view_count': 'mean',
            'title': 'count'
        }).reset_index()
        
        heatmap_data.columns = ['day', 'hour', 'engagement_mean', 'engagement_std', 'avg_views', 'video_count']
        heatmap_data['engagement_std'] = heatmap_data['engagement_std'].fillna(0)
        
        # Pivot for display
        heatmap_pivot = heatmap_data.pivot_table(
            index='day',
            columns='hour',
            values='engagement_mean',
            fill_value=0
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex([d for d in day_order if d in heatmap_pivot.index])
        
        # Calculate stats
        max_engagement = heatmap_data[heatmap_data['engagement_mean'] > 0]['engagement_mean'].max()
        peak_data = heatmap_data.loc[heatmap_data['engagement_mean'].idxmax()]
        
        # Function to get BLUE color class
        def get_color_class(value, max_val):
            if value == 0:
                return 'cell-empty'
            elif value < max_val * 0.2:
                return 'cell-1'
            elif value < max_val * 0.4:
                return 'cell-2'
            elif value < max_val * 0.6:
                return 'cell-3'
            elif value < max_val * 0.8:
                return 'cell-4'
            else:
                return 'cell-5'
        
        # Build HTML - BOX LAYOUT with hour labels
        html = '<div class="heatmap-wrapper">'
        
        # Hour labels row
        html += '<div class="hour-labels">'
        for hour in heatmap_pivot.columns:
            html += f'<div class="hour-label">{int(hour):02d}</div>'
        html += '</div>'
        
        # Heatmap rows
        html += '<div class="heatmap-container">'
        
        for day in heatmap_pivot.index:
            html += '<div class="heatmap-row">'
            html += f'<div class="day-label">{day[:3]}</div>'
            html += '<div class="day-row">'
            
            for hour in heatmap_pivot.columns:
                value = heatmap_pivot.loc[day, hour]
                color_class = get_color_class(value, max_engagement)
                
                # Get detailed data for tooltip
                cell_data = heatmap_data[(heatmap_data['day'] == day) & (heatmap_data['hour'] == hour)]
                
                if len(cell_data) > 0:
                    engagement = cell_data['engagement_mean'].values[0]
                    std = cell_data['engagement_std'].values[0]
                    views = cell_data['avg_views'].values[0]
                    count = int(cell_data['video_count'].values[0])
                    
                    tooltip = f"""
                        <div class="tooltip-title">{day[:3]} {hour:02d}:00 UTC</div>
                        <div class="tooltip-stat">
                            <div class="tooltip-stat-label">📊 Avg Engagement</div>
                            <div class="tooltip-stat-value">{engagement:.2f}% ± {std:.2f}%</div>
                        </div>
                        <div class="tooltip-stat">
                            <div class="tooltip-stat-label">👁️ Avg Views</div>
                            <div class="tooltip-stat-value">{views:,.0f}</div>
                        </div>
                        <div class="tooltip-stat">
                            <div class="tooltip-stat-label">📹 Videos Uploaded</div>
                            <div class="tooltip-stat-value">{count} video{"s" if count != 1 else ""}</div>
                        </div>
                        <div class="tooltip-stat" style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e8ecf1;">
                            <div class="tooltip-stat-label">💡 Insight</div>
                            <div class="tooltip-stat-value" style="font-size: 10px;">
                                {"✅ Strong time slot" if engagement > max_engagement * 0.7 else "⚠️ Average slot" if engagement > max_engagement * 0.3 else "❌ Weak slot"}
                            </div>
                        </div>
                    """
                else:
                    tooltip = f"<div class='tooltip-title'>{day[:3]} {hour:02d}:00 UTC</div><div class='tooltip-stat-label'>No data</div>"
                
                html += f'<div class="heatmap-cell {color_class}" title="{hour:02d}">'
                html += f'<div class="tooltip-content">{tooltip}</div>'
                html += '</div>'
            
            html += '</div>'
            html += '</div>'
        
        html += '</div>'
        html += '</div>'
        
        # Display heatmap
        st.markdown(html, unsafe_allow_html=True)
        
        # Insight box
        st.markdown(f"""
            <div class="insight-box">
                💡 <strong>Best Strategy:</strong> Upload on <strong>{peak_data['day']}</strong> around <strong>{int(peak_data['hour']):02d}:00 UTC</strong> for maximum engagement ({peak_data['engagement_mean']:.2f}%) with an average of <strong>{peak_data['avg_views']:,.0f} views</strong> per video
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
