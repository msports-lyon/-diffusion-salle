@echo off
title Régie Vidéo — Serveur Local
color 0A
echo.
echo  Démarrage du serveur de diffusion vidéo...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERREUR : Python n'est pas installé !
    echo  Téléchargez-le sur https://www.python.org/downloads/
    echo  Cochez bien "Add Python to PATH" lors de l'installation.
    pause
    exit /b 1
)

REM Lancer le serveur
python "%~dp0server.py"
pause
