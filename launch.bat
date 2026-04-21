@echo off
:: Vinted Stock Manager - Launcher
:: Double-cliquez ce fichier pour lancer l'application

cd /d "%~dp0"

echo.
echo ==========================================
echo   VINTED STOCK MANAGER - Demarrage
echo ==========================================
echo.

:: Activer l'environnement virtuel
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✓ Environnement virtuel activé
) else (
    echo ⚠ Environnement virtuel non trouvé, lancement direct...
)

:: Lancer l'application
python -m vinted_app.main

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible de lancer l'application
    echo Verifiez que Python est installe et les dependances installees
    echo.
    pause
)
)
