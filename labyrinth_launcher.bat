@echo off
REM ============================================
REM Labyrinth Enterprise - Quick Launcher
REM Double-click this file to start Labyrinth
REM No terminal window needed!
REM ============================================

title Labyrinth Enterprise Launcher

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Launch Labyrinth (hidden console)
start /B pythonw labyrinth_enterprise.py

REM Exit immediately (don't keep console open)
exit