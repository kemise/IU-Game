@echo off

rem check the python installation
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python ist nicht installiert. Installiere Python und füge es zum System-Pfad hinzu. Installieren sie: https://www.python.org/ftp/python/3.11.2/python-3.11.2-arm64.exe
    pause
    exit /b 1
)

rem check the requirements
pip install --no-cache-dir -r requirements.txt
if %errorlevel% neq 0 (
    echo Fehler beim Installieren der Anforderungen.
    pause
    exit /b 1
)

rem run main.py as a single window
start pythonw main.py

rem close the file
exit
