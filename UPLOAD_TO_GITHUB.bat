@echo off
REM Telegram Music Bot - Automated Upload Script
REM This script will upload your bot to GitHub

setlocal enabledelayedexpansion

cls
echo.
echo ================================================================================
echo         TELEGRAM MUSIC BOT - AUTOMATED GITHUB UPLOAD
echo ================================================================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH!
    echo.
    echo Install Git from: https://git-scm.com/download/win
    echo Then restart this script.
    echo.
    pause
    exit /b 1
)

echo [1/7] Checking Git setup...
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo.
    echo You need to setup Git first!
    echo.
    set /p username="Enter Git username: "
    set /p useremail="Enter Git email: "
    
    git config --global user.name "!username!"
    git config --global user.email "!useremail!"
    
    echo.
    echo ✓ Git configured!
)

echo.
echo [2/7] Initializing repository...
git init
echo ✓ Git initialized!

echo.
echo [3/7] Adding all files...
git add .
echo ✓ Files added!

echo.
echo [4/7] Creating commit...
git commit -m "Initial commit - Telegram Music Bot Ready for Deployment"
echo ✓ Committed!

echo.
echo ================================================================================
echo NEXT STEPS - YOU MUST DO THIS IN BROWSER:
echo ================================================================================
echo.
echo Step 1: Go to GitHub.com and create a new repository
echo   - Name: telegram-music-bot
echo   - Public
echo   - DO NOT initialize with README/license/gitignore
echo.
echo Step 2: After creating repo, GitHub will show you commands
echo   - Look for: git remote add origin https://github.com/YOUR_USERNAME/telegram-music-bot.git
echo   - Copy that URL
echo.
echo Step 3: Come back here and we'll finish the upload
echo.
pause

set /p github_url="Paste your GitHub repository URL (from step 2): "

if "!github_url!"=="" (
    echo ERROR: URL cannot be empty!
    pause
    exit /b 1
)

echo.
echo [5/7] Adding GitHub remote...
git remote add origin !github_url!
echo ✓ Remote added!

echo.
echo [6/7] Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed! You may need to:
    echo   1. Setup GitHub authentication
    echo   2. Use personal access token
    echo   3. Setup Git credentials
    echo.
    echo Visit: https://docs.github.com/en/authentication
    echo.
    pause
    exit /b 1
)

echo ✓ Pushed to GitHub!

echo.
echo [7/7] Done!
echo.
echo ================================================================================
echo SUCCESS! Your bot is now on GitHub!
echo ================================================================================
echo.
echo Next: Deploy on Railway
echo.
echo 1. Go to: https://railway.app
echo 2. Sign up with GitHub
echo 3. New Project → Deploy from GitHub
echo 4. Select your: telegram-music-bot repo
echo 5. Add variables from .env.example
echo 6. Deploy!
echo.
echo You're all set! 🎵
echo.
pause
