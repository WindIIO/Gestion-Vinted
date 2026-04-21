@echo off
:: Vinted Stock Manager - Launcher
:: Double-cliquez ce fichier pour lancer l'application

cd /d "%~dp0"

echo.
echo ==========================================
echo   VINTED STOCK MANAGER - Demarrage
echo ==========================================
echo.

python vinted_app/main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible de lancer l'application
    echo Verifiez que Python est installe
    echo.
    pause
)
