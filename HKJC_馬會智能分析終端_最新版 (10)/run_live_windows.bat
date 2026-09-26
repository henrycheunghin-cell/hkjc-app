@echo off
title HKJC Live Odds Terminal
cd /d "%~dp0"

echo ========================================================
echo  HKJC Racing Live Terminal - Launcher
echo ========================================================
echo.

echo [1/2] Checking Python environment...
set PYTHON_CMD=python
where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo [ERROR] Python is not installed or not in PATH.
        echo Please install Python from https://www.python.org/downloads/
        echo IMPORTANT: Check the box 'Add python.exe to PATH' during install!
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
)

echo [2/2] Checking and installing required packages...
%PYTHON_CMD% -m pip install streamlit pandas requests beautifulsoup4 -q

echo.
echo ========================================================
echo  Starting HKJC Terminal...
echo  Your web browser will open automatically at:
echo  Local PC: http://localhost:8501
echo.
echo  * For mobile access: Connect phone to the same Wi-Fi,
echo    then scan the QR Code shown in the left sidebar!
echo ========================================================
echo.
%PYTHON_CMD% -m streamlit run app_local_live.py

if errorlevel 1 (
    echo.
    echo [ERROR] App exited with an error. Please see details above.
)
pause
