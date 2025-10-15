@echo off
TITLE YouTube Analysis Tool Launcher

echo =========================================================
echo  Installing required packages. This might take a moment...
echo =========================================================
pip install -r requirements.txt

cls
echo =========================================================
echo  Launching the YouTube Analysis Tool...
echo =========================================================
echo.
echo  Your browser should open automatically.
echo  If it doesn't, open it and go to one of the URLs below.
echo.

python -m streamlit run main.py

echo.
echo =========================================================
echo  The application has been stopped.
echo =========================================================
pause

