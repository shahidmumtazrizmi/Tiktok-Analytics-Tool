@echo off
echo ========================================
echo TikTok Analytics + RAG Chatbot
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your OpenAI API key
    echo You can find it at: https://platform.openai.com/api-keys
    echo.
    pause
)

REM Start the application
echo.
echo Starting TikTok Analytics + RAG Chatbot...
echo.
echo Access URLs:
echo - Main App: http://localhost:8000
echo - Chatbot: http://localhost:8000/chatbot
echo - API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python start.py

pause 