@echo off
echo Installing required packages, this might take a moment...
pip install -r requirements.txt

echo.
echo Launching the YouTube Analysis Tool...
streamlit run main.py
