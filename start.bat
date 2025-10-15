@echo off
TITLE YouTube Channel Analyzer

echo Starting the YouTube Channel Analysis App...

REM Check if the virtual environment directory exists.
IF NOT EXIST venv (
    echo.
    echo [ERROR] The 'venv' virtual environment directory was not found.
    echo Please run the installation steps in the README.md file first to set it up.
    echo.
    pause
    exit /b
)

echo Activating the virtual environment...
call venv\Scripts\activate

echo Launching the Streamlit app...
echo You can close this window after the app has opened in your browser.
echo.

streamlit run main.py

pause