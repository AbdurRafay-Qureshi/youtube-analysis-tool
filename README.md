# 📊 YouTube Channel Data Analysis Tool

A powerful Python and Streamlit-based tool to fetch and visualize public YouTube channel data using the official YouTube Data API v3. Gain deep insights into channel performance, audience engagement, and content strategy.

## ✨ Features

- 📈 Channel Overview: Displays total subscribers, views, videos, and lifetime engagement rate.
- 🏆 Top Video Analysis: Lists the top 10 videos sorted by views, likes, comments, or engagement rate.
- 🕒 Performance Over Time: Visualizes view counts over time to identify trends and viral hits.
- 📅 Upload Schedule Insights: Analyzes preferred days and hours for video uploads.
- 📊 Engagement Analysis:
  - Scatter plot showing correlation between video duration and view count.
  - Histogram of engagement rate distribution across videos.
- 📋 Raw Data View: Presents the processed dataset in a clean, sortable table.
- 📥 Data Export: Download the complete video dataset as a CSV file.

## 🚀 Demo

Dro<img width="1918" height="1084" alt="Screenshot3" src="https://github.com/user-attachments/assets/acbf42f3-fb45-4a40-95f5-35daf00422d2" />
<img width="1920" height="1078" alt="Screenshot1" src="https://github.com/user-attachments/assets/400e6c46-1352-4807-94e5-9214c30574ee" />
<img width="1918" height="1081" alt="Screenshot2" src="https://github.com/user-attachments/assets/50acf800-ef7a-4b14-8e0d-4d578bf1f6ef" />
<img width="1912" height="1083" alt="ss4" src="https://github.com/user-attachments/assets/0568fa35-d4d5-48ff-ac68-70e20b7b2950" />


## 🛠️ Getting Started (The Easy Way)

No complex commands. Just a few clicks to get up and running.

### Step 1: Prerequisites

- Install Python: You need Python 3.9 or newer. If you don't have it, download it from the official Python website.
- **IMPORTANT**: During installation, you MUST check the box that says "Add Python to PATH". This is crucial for the start.bat script to work.
- Get a YouTube API Key: The app needs a key to talk to YouTube. You can get one for free from the Google Cloud Console.

### Step 2: Download the Tool

- Go to the main page of this repository.
- Click the green <> Code button.
- Click Download ZIP.
- Unzip the folder to a location you can easily access, like your Desktop.

### Step 3: Run the App

- Open the unzipped folder.
- Find the start.bat file.
- Double-click it.
- That's it! A command window will open, automatically install the required packages, and then launch the application in your web browser.

## ⚙️ How to Use

- Enter API Key: Paste your YouTube Data API v3 key into the sidebar.
- Enter Channel Identifier: Input the channel URL, Channel ID, or Username.
- Analyze: Click "Analyze Channel" to generate the report.

## 📂 File Structure

- youtube.py: Handles YouTube API communication and backend logic.
- main.py: Builds the Streamlit frontend and visualizations.
- requirements.txt: Lists all required Python libraries.
- start.bat: The one-click script for Windows users to install dependencies and run the app.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Fork this repository.
- Open issues for bugs or suggestions.
- Submit pull requests with improvements.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
