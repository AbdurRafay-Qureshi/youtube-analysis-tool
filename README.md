# 🎯 Social Analytics Hub - YouTube Analytics Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-2.0-orange.svg" alt="Version">
</p>

<p align="center">
  <strong>A professional, multi-platform analytics dashboard that provides accurate, real-time insights for YouTube channels using the official YouTube Data API v3.</strong>
</p>

<p align="center">
  Built with cutting-edge data science tools and a beautiful, intuitive interface.
</p>

---

## ✨ Features Overview

### 📊 **Channel Analytics**
- **Real subscriber count** with clean formatting
- **Total views** showing actual channel-wide statistics
- **Video count** with data coverage percentage
- **Engagement rate** calculated using 30-day rolling average
- **Official count badge** - verified against YouTube API

### 📈 **Performance Tracking**
- **Performance Over Time** - Interactive line chart tracking views across channel history
- **Real-time data updates** with hover tooltips showing:
  - Video title
  - Upload date
  - Views, likes, comments
  - Engagement rate
  - Video duration

### 💎 **Engagement Breakdown**
Beautiful gradient cards showing:
- **Views** (with % of channel total)
- **Likes** (with % of total engagement)
- **Comments** (with % of total engagement)

### 🎬 **Top Videos Analysis**
- Sort by:
  - View Count
  - Like Count
  - Comment Count
  - Engagement Rate
- **Top 10 videos** displayed as interactive horizontal bar chart
- Color-coded by engagement rate
- Detailed hover information

### 📅 **Upload Schedule Intelligence**
- **Uploads by Day** - Bar chart showing best days to upload
- **Uploads by Hour (UTC)** - Line chart revealing optimal posting times
- Discover patterns in your upload consistency

### 🔍 **Advanced Insights** (6 Analysis Tools)

<details>
<summary><b>View All 6 Insight Tools</b></summary>

#### 1. **Growth Timeline**
Track cumulative channel growth over time with dual-axis chart showing total views and video count.

#### 2. **Best Performing Days**
Analyze which days get the most engagement with data-driven scheduling recommendations.

#### 3. **Video Length Analysis**
Categorize videos by duration (Short, Medium, Long, Extra Long) and find your optimal video length.

#### 4. **Engagement Heatmap**
Visual heatmap showing engagement by day and hour to discover when your audience is most active.

#### 5. **Performance Matrix**
Scatter plot comparing views vs engagement to identify star performers and hidden gems.

#### 6. **Upload Consistency Score**
Track how consistent your upload schedule is with weekly variance analysis.

</details>

### 📋 **Data Table & Export**
- Complete dataset view with all video metrics
- **Scrollable table** with hover effects
- **PDF Report Download** - Export full analytics report
- Clean, professional formatting

### 🎨 **Professional UI/UX**
- **Dark sidebar** with multi-platform support
- **Gradient color scheme** - Professional blue gradients
- **Interactive charts** powered by Plotly
- **Responsive design** - Works on all screen sizes
- **Smooth animations** and hover effects
- **Data coverage warnings** - Know exactly how much data is analyzed

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- YouTube Data API v3 key from [Google Cloud Console](https://console.cloud.google.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbdurRafay-Qureshi/youtube-analysis-tool.git
   cd youtube-analysis-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```
   -or just hit start.bat, it will automatically open the web browser

4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - The dashboard will automatically launch

---

## 📝 Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable **YouTube Data API v3**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create credentials:
   - Go to "Credentials" → "Create Credentials" → "API Key"
   - Copy your API key
5. Paste it in the dashboard sidebar

> **💡 Note:** Free tier provides 10,000 quota units per day (enough for ~100 channel analyses)

---

## 🎯 Usage Guide

### 1. **Analyze a Channel**

**Sidebar Configuration:**
- Enter your YouTube API key
- Paste channel identifier (URL, @username, or channel ID)
- Click "Analyze Channel"

**Supported Input Formats:**
```
https://www.youtube.com/@channelname
https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxx
@channelname
UCxxxxxxxxxxxxxxxxxxxxxx (channel ID)
Channel Name (searches YouTube)
```

### 2. **Filter Data**

| Filter Type | Description |
|------------|-------------|
| **Date Range** | Filter videos by start and end date |
| **All Categories** | Show all videos |
| **Top Performing** | Videos in top 25% by views |
| **Recent** | Videos from last 30 days |

### 3. **Explore Insights**

Navigate through tabs:
- **Top Videos** - See your best-performing content
- **Upload Schedule** - Discover optimal posting times
- **Insights** - Deep dive into 6 analysis tools
- **Data Table** - View and export complete dataset

### 4. **Export Data**

**PDF Report:**
1. Navigate to "Data Table" tab
2. Click "Download PDF Report"
3. Includes all channel stats and video data

---

## 📊 Understanding the Metrics

| Metric | Description | Details |
|--------|-------------|---------|
| **Subscribers** | Official count from YouTube API | Displayed with K/M formatting (1.1M = 1,100,000) |
| **Total Views** | Actual channel-wide view count | Not just fetched videos - pulls from API |
| **Total Videos** | Correct count including all public videos | Shows "X analyzed" to indicate data coverage |
| **Engagement Rate** | `(Likes + Comments) / Views × 100` | Industry average: 3-5% • 7%+ = Excellent |
| **Data Coverage** | % of total videos analyzed | Warning if < 95% coverage |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **Streamlit** | Web framework & UI |
| **Pandas** | Data manipulation |
| **Plotly** | Interactive visualizations |
| **YouTube Data API v3** | Data source |
| **NumPy** | Numerical computations |
| **ReportLab** | PDF generation |

---

## 📂 Project Structure

```
social-analytics-hub/
├── main.py                      # Main application
├── youtube.py                   # YouTube API handler
├── engagement_calculator.py     # Engagement metrics & 30-day comparison
├── insights.py                  # 6 advanced analysis tools
├── pdf_exporter.py             # PDF report generation
├── ui/
│   ├── sidebar.py              # Sidebar components
│   ├── components.py           # Reusable UI components
│   ├── styles.py               # CSS styling
│   └── theme.py                # Color schemes & gradients
├── assets/
│   └── logos/                  # Platform logos (YouTube, Reddit, etc.)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

---

## 📸 Screenshots

<img width="1908" height="1062" alt="Screenshot (21)" src="https://github.com/user-attachments/assets/6d1443b5-89e4-4048-b683-31205aee9b74" />
<img width="1911" height="1064" alt="Screenshot (20)" src="https://github.com/user-attachments/assets/ad6c1322-01fd-42f6-aa6b-7230177caa6b" />
<img width="1911" height="1075" alt="Screenshot (25)" src="https://github.com/user-attachments/assets/ab6ca1a1-bac1-4f96-9daa-b647c8c32fef" />
<img width="1904" height="1064" alt="Screenshot (24)" src="https://github.com/user-attachments/assets/380f46e6-1bc1-4411-9aec-e0d2b691a067" />
<img width="1913" height="1064" alt="Screenshot (23)" src="https://github.com/user-attachments/assets/f8c39276-b177-4112-8a37-0ba4e16aec63" />
<img width="1899" height="1067" alt="Screenshot (22)" src="https://github.com/user-attachments/assets/5fe5c5dd-264d-45b7-8e32-8f9b002dc1a0" />



---

## 🔧 Advanced Features

### **API Optimization**
- Intelligent quota management
- Batch request processing
- Pagination for channels with 500+ videos
- Error handling with automatic retry

### **Data Validation**
- Cross-checks stats against official API
- Warns about missing data
- Coverage percentage calculation
- Private/unlisted video detection

### **Performance**
- Caches channel data in session
- Fast chart rendering with Plotly
- Lazy loading for large datasets
- Efficient memory usage

---

## 🐛 Known Issues & Solutions

<details>
<summary><b>View Troubleshooting Guide</b></summary>

### Issue: "Could not extract channel ID"
**Solution:** Use full channel URL or channel ID (UC...) instead of channel name

### Issue: "API quota exceeded"
**Solution:** YouTube API has daily limit of 10,000 units. Wait 24 hours or use different API key

### Issue: Subscriber count shows wrong stats
**Solution:** You're analyzing a "Topic" channel instead of official channel. Use direct channel URL or ChannelID

### Issue: Data coverage < 95%
**Solution:** Channel has > 500 videos. API limitation - shows warning with actual coverage %

</details>

---

## 🚧 Roadmap

### Coming Soon
- [ ] Multi-platform support (Reddit, LinkedIn, Instagram)
- [ ] Sentiment analysis for comments
- [ ] Predictive analytics (forecast future views)
- [ ] Competitor comparison
- [ ] Custom date range analysis
- [ ] Automated reporting (email PDF reports)
- [ ] Dark/Light theme toggle
- [ ] Export to CSV/Excel
- [ ] API rate limit indicator
- [ ] Channel comparison (vs mode)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create your feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contributing Guidelines
- ✅ Code follows PEP 8 style guidelines
- ✅ All features are tested
- ✅ Documentation is updated
- ✅ Commit messages are descriptive

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

### Under the conditions:
- ℹ️ License and copyright notice must be included
- ℹ️ No liability or warranty

---

## 🙏 Acknowledgments

- **YouTube Data API v3** - For providing comprehensive channel data
- **Streamlit Team** - For the amazing web framework
- **Plotly** - For beautiful, interactive visualizations
- **Python Community** - For excellent data science libraries

---

## 📧 Contact & Support

**Abdur Rafay Qureshi**

- 👤 GitHub: [@AbdurRafay-Qureshi](https://github.com/AbdurRafay-Qureshi)
- 🔗 Project: [youtube-analysis-tool](https://github.com/AbdurRafay-Qureshi/youtube-analysis-tool)
- 🐛 Issues: [Report a bug](https://github.com/AbdurRafay-Qureshi/youtube-analysis-tool/issues)

### For Support:
- Open an issue on GitHub
- Check existing issues for solutions
- Read the FAQ section below

---

## ❓ FAQ

<details>
<summary><b>Frequently Asked Questions</b></summary>

**Q: Do I need a paid YouTube API key?**  
A: No, the free tier provides 10,000 quota units/day (enough for ~100 analyses).

**Q: Can I analyze private channels?**  
A: No, only public channels accessible via YouTube Data API.

**Q: How often is data updated?**  
A: Data is fetched in real-time when you click "Analyze Channel".

**Q: Can I analyze multiple channels?**  
A: Yes, analyze one at a time. Future versions will support comparison mode.

**Q: Is my API key stored?**  
A: No, API key is only stored in your browser session (not on any server).

**Q: Why is my engagement rate different from YouTube Studio?**  
A: YouTube Studio uses different calculation methods and includes more metrics (shares, saves, etc.).

</details>

---

## 🌟 Support This Project

If you find this project useful, please consider:

- ⭐ Giving it a star on GitHub
- 📢 Sharing it with others
- 🤝 Contributing to the project
- 💬 Providing feedback

**Your support helps us improve and add more features!**

---

## 📝 Changelog

### v2.0 (October 2025)

#### ✨ What's New
- 🎨 Complete UI/UX overhaul with professional gradient design
- 📊 Added 6 advanced insight tools (Growth Timeline, Video Length Analysis, etc.)
- 📅 Upload Schedule analysis (by day and hour)
- 📋 Interactive data table with PDF export
- 🌐 Multi-platform sidebar (YouTube, Reddit, LinkedIn - coming soon)
- 🔢 K/M number formatting for clean display

#### 🎯 100% Accurate Data
- ✅ Fixed all statistics - now pulls actual counts from YouTube API v3
- ✅ Subscriber count accuracy with proper formatting
- ✅ Total views show actual channel-wide count
- ✅ Video count displays correct total
- ✅ Engagement rate based on 30-day rolling average

#### 🔧 Technical Improvements
- ⚡ Optimized API calls - reduced quota usage
- 📄 Better pagination - reliably fetches up to 500 videos
- ✅ Improved validation against official YouTube counts
- 🔍 Enhanced logging for debugging
- 🛡️ Better error handling

#### 🐛 Bug Fixes
- Fixed subscriber counts showing rounded values
- Fixed total views showing only fetched video views
- Fixed engagement rate calculation
- Fixed video count mismatch (private/unlisted handling)
- Fixed API pagination issues

### v1.0.0 (Initial Release)
- 🎉 Basic YouTube analytics dashboard
- 📹 Video fetching and simple analysis
- 📈 Basic visualizations

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://github.com/AbdurRafay-Qureshi">Abdur Rafay Qureshi</a></strong>
</p>

<p align="center">
  <em>© 2025 Social Analytics Hub • Empowering creators with data-driven insights</em>
</p>
