# YouTube Channel Data Analysis Tool 📊

A powerful Python and Streamlit-based tool to fetch and visualize public YouTube channel data using the official YouTube Data API v3. Gain deep insights into channel performance, audience engagement, and content strategy.

---

## ✨ Features

- **📈 Channel Overview**: Displays total subscribers, views, videos, and lifetime engagement rate.
- **🏆 Top Video Analysis**: Lists the top 10 videos sorted by views, likes, comments, or engagement rate.
- **🕒 Performance Over Time**: Visualizes view counts over time to identify trends and viral hits.
- **📅 Upload Schedule Insights**: Analyzes preferred days and hours for video uploads.
- **📊 Engagement Analysis**:
  - Scatter plot showing correlation between video duration and view count.
  - Histogram of engagement rate distribution across videos.
- **📋 Raw Data View**: Presents the processed dataset in a clean, sortable table.
- **📥 Data Export**: Download the complete video dataset as a CSV file.

---

## 🚀 Demo

*Drop a screenshot of your application dashboard here to showcase the channel overview and top-performing videos!*

---

## 🛠️ Getting Started

Follow these steps to set up and run the tool.

### Option A: Clone the Repository
The quickest way to get started:

```bash
git clone <this-repository-url>
cd youtube-channel-analysis-tool
```

Then, proceed to **Step 2: Create a Virtual Environment**.

### Option B: Set Up a New Repository
If you prefer creating a fresh project using GitHub Desktop:

1. **Create the Repo**: Complete the repository setup in GitHub Desktop.
2. **Add Files**: Copy `main.py`, `youtube.py`, `requirements.txt`, and `start.bat` into the repository's local folder.
3. **Commit Files**: In GitHub Desktop, write a commit message (e.g., "Initial commit") and click "Commit".
4. **Publish (Optional)**: Click "Publish repository" to share it on your GitHub profile.

Now, move to the setup steps below.

---

## ⚙️ Setup & Installation

### Step 1: Obtain a YouTube API Key
You’ll need a **YouTube Data API v3 Key** from the [Google Cloud Console](https://console.cloud.google.com/).

### Step 2: Create a Virtual Environment
Keep your Python environment clean by creating a virtual environment:

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
With the virtual environment active, install the required libraries:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Launch the app in one of two ways:

- **Command Line**: Run the following command to start the app on localhost:
  ```bash
  streamlit run main.py
  ```
  Your browser will open with the application ready to use.

- **Windows One-Click Start**: Double-click the `start.bat` file to automatically activate the virtual environment and launch the app on localhost.

---

## ⚙️ How to Use

1. **Enter API Key**: Paste your YouTube Data API v3 key into the sidebar.
2. **Enter Channel Identifier**: Input the channel URL, Channel ID, or Username.
3. **Analyze**: Click "Analyze Channel" to generate the report.

---

## 📂 File Structure

- `youtube.py`: Handles YouTube API communication and backend logic.
- `main.py`: Builds the Streamlit frontend and visualizations.
- `requirements.txt`: Lists all required Python libraries.
- `start.bat`: Convenience script for Windows users to run the app.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Fork this repository.
- Open issues for bugs or suggestions.
- Submit pull requests with improvements.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.