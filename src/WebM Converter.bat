@echo off
:: Video to WebM Converter - Launcher
:: Double-click this file to start the application

:: Use pythonw to run without console window
:: Try pythonw first (no console), fallback to python if needed
start "" pythonw video-converter-gui.py 2>nul
if %errorlevel% neq 0 (
    start "" python video-converter-gui.py
)