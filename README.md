📊 YouTube Channel Data Analysis Tool
A comprehensive Python-based tool to extract, analyze, and visualize public data from any YouTube channel using the YouTube Data API v3 and Streamlit.

✨ Features
This tool provides a detailed report on a channel's performance, offering insights into content strategy, audience engagement, and overall growth trends.

📈 Channel Overview: Get a high-level snapshot including total subscribers, views, videos, and lifetime engagement rate.

🏆 Top Video Analysis: Instantly identify the top 10 performing videos sorted by views, likes, comments, or engagement rate.

🕒 Performance Over Time: Visualize video view counts over time to spot trends and viral hits.

📅 Upload Schedule Insights: Analyze which days of the week and hours of the day the channel prefers for uploading content.

📊 Engagement Analysis:

Scatter plot to analyze the correlation between video duration and view count.

Histogram showing the distribution of engagement rates across all videos.

📋 Raw Data View: View the entire processed dataset in a clean, sortable table.

📥 Data Export: Download the complete video dataset as a CSV file for further analysis.

🚀 Demo
Here's a look at the final application dashboard, showing the channel overview and top-performing videos.

🛠️ Setup & Installation
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.9 or higher

A YouTube Data API v3 Key. You can obtain one from the Google Cloud Console.

Step 1: Clone the Repository
Open your terminal or command prompt and clone this repository:

git clone <your-repository-url>
cd <repository-folder-name>

Step 2: Create a Virtual Environment
It's highly recommended to use a virtual environment to keep project dependencies isolated.

On Windows:

python -m venv venv
venv\Scripts\activate

On macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt

▶️ Running the Application
Once the setup is complete, you can launch the Streamlit application with a single command:

streamlit run main.py

Your web browser should automatically open with the application running.

For Windows Users:
A start.bat file is included for convenience. Simply double-click it to activate the virtual environment and run the app automatically.

⚙️ How to Use
Enter API Key: Paste your YouTube Data API v3 key into the first input box in the sidebar.

Enter Channel Identifier: Paste the URL, Channel ID, or Username of the YouTube channel you want to analyze.

Analyze: Click the "Analyze Channel" button and wait for the magic to happen!

📂 File Structure
The project is organized into two main Python files for clarity and separation of concerns:

youtube.py: The backend logic. This module handles all interactions with the YouTube Data API, including fetching, cleaning, and processing the data.

main.py: The Streamlit frontend. This module builds the user interface, creates the plots, and displays the final analysis.

Feel free to fork this repository, open issues, and submit pull requests. Contributions are welcome!# youtube-analysis-tool
Here you go. Short, sweet, and to the point. Slap this in the description box:  A data analysis tool built with Python and Streamlit that fetches and visualizes public data from any YouTube channel via the official API v3.
