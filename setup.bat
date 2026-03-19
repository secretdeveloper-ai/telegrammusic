@echo off
REM Quick Setup Script for Telegram Music Bot (Windows)

echo.
echo 🎵 Telegram Music Bot - Quick Setup
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Download from: https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Installation complete!
echo.
echo Next steps:
echo 1. Copy .env.example to .env (or use cmd: copy .env.example .env)
echo 2. Edit .env with your credentials
echo 3. Run: python main.py
echo.
echo For Railway deployment, see RAILWAY_DEPLOY.md
echo.
pause
